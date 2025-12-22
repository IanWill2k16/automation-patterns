# Automation Patterns

This repository is a curated collection of small, production-inspired automation scripts.

The goal of this repo is not to present a single deployable system, but to demonstrate:

* How real operational problems are translated into automation
* Clear separation of concerns (identity, assets, networking)
* Safe handling of configuration and credentials
* Practical scripting that replaces manual, error-prone work

All scripts are sanitized versions of real tools used in enterprise environments. Any credentials, tenant details, domains, or internal identifiers have been removed or replaced with placeholders.

---

## Repository Structure

```
automation-patterns/
├── asset-management/
│   ├── dell-warranty-enrichment.py
│   └── README.md
├── identity/
│   ├── aad-to-ad-user-provisioning.ps1
│   ├── graph-mfa-report.py
│   └── README.md
├── network-automation/
│   ├── mac-address-trace.py
│   └── README.md
```

Each directory is self-contained and documented independently.

---

# Asset Management

## Overview

The scripts in this directory focus on asset lifecycle visibility by enriching incomplete device data by pulling authoritative information from vendor or inventory sources.

These patterns are common in environments where:

* Asset data is fragmented across systems
* Procurement and IT operations need better visibility
* Manual lookups do not scale

---

## `dell-warranty-enrichment.py`

### Problem

Device inventories often contain only basic identifiers (e.g., service tags), while warranty status and entitlement data live in separate systems.

Manually checking warranty status for large device fleets is time-consuming and error-prone.

### Solution

This script:

* Reads a list of device identifiers from an input file
* Queries an external warranty information source (API integration abstracted)
* Enriches the original dataset with warranty and entitlement details
* Outputs a consolidated report suitable for operations or procurement teams

### Key Concepts Demonstrated

* External API integration patterns
* Batch processing of asset data
* Defensive handling of incomplete or missing records

### Notes

* All vendor credentials and endpoints have been removed
* The script is structured to make API substitution straightforward

---

# Identity Automation

## Overview

Identity-related tasks are some of the most automation-friendly, and risk-prone, operations in IT.

The scripts in this directory demonstrate controlled, auditable identity automation focused on reporting and provisioning.

---

# Autopilot Device Renaming Automation

## Overview

This script automates the reconciliation of **on-prem Active Directory computer names** with **Microsoft Intune / Windows Autopilot device identities**.

In hybrid environments, devices are often provisioned with temporary or generic hostnames during imaging, while the authoritative device name is defined later in Intune. Manually reconciling these names is time-consuming and error-prone at scale.

This automation safely aligns on-prem computer names with their corresponding Autopilot identities using Microsoft Graph.

---

## Problem

In hybrid AD / Entra ID environments:

- Devices may initially join the domain with placeholder names
- Intune / Autopilot maintains the authoritative device identity
- Manual renaming requires:
  - Looking up serial numbers
  - Matching devices across systems
  - Performing privileged rename + reboot operations
- This process does not scale and introduces risk when done manually

---

## Solution

This script:

1. Queries on-prem Active Directory for computer objects
2. Authenticates to Microsoft Graph using an application identity
3. Retrieves all Windows Autopilot device identities (with pagination)
4. Matches devices by **hardware serial number**
5. Safely renames computers only when:
   - The device is reachable
   - A serial number match is found
   - A valid target name exists
6. Reboots devices only after a successful rename

All actions are gated behind validation checks to minimize operational risk.

---

## Key Concepts Demonstrated

- Hybrid identity automation (AD + Entra ID)
- Microsoft Graph API usage
- OAuth2 client credentials flow
- Defensive automation patterns
- Idempotent, conditional execution
- Separation of secrets from code
- Safe handling of privileged operations

---

## Security Notes

- **No credentials are stored in source control**
- Tenant IDs, client IDs, and secrets are represented as placeholders
- In production, secrets were retrieved from a secure secret store
- Domain credentials are abstracted behind a placeholder function
- Script logic is read-only until all validation checks pass

This repository contains a **sanitized version** suitable for demonstration and review.

---

## Script Flow

1. Retrieve domain computer objects
2. Acquire Microsoft Graph access token
3. Enumerate Autopilot devices (handling pagination)
4. For each eligible computer:
   - Verify network reachability
   - Retrieve BIOS serial number remotely
   - Match against Autopilot inventory
   - Rename computer if a valid match is found
   - Reboot only after successful rename

---

## Intended Use

This script is intended as a **reference automation pattern**, not a drop-in production tool.

It demonstrates how operational identity problems can be translated into:
- Safe
- Auditable
- Maintainable automation

---

## Why This Matters

This automation replaces a brittle, manual process with a controlled workflow that:

- Reduces technician effort
- Prevents naming inconsistencies
- Improves endpoint lifecycle hygiene
- Scales cleanly across large environments

It reflects real-world tenant administration challenges and the automation patterns used to solve them.

---

## `aad-to-ad-user-provisioning.ps1`

### Problem

Hybrid identity environments frequently require:

* Creating on-prem Active Directory users based on Azure AD records
* Maintaining consistent attributes across systems
* Reducing manual account creation errors

### Solution

This PowerShell script:

* Reads user data from Azure AD
* Applies transformation and validation logic
* Provisions corresponding on-prem AD accounts
* Supports idempotent execution to avoid duplication

### Key Concepts Demonstrated

* Hybrid identity workflows
* PowerShell automation for Active Directory
* Attribute mapping and validation
* Safe defaults for identity provisioning

### Notes

* Authentication details and tenant identifiers are intentionally omitted
* Script structure emphasizes clarity and auditability

---

## `graph-mfa-report.py`

### Problem

Security and compliance teams often need visibility into MFA enforcement and adoption.

Native dashboards may not provide the exact breakdown required for audits or leadership reporting.

### Solution

This script:

* Queries Microsoft Graph for user authentication methods
* Aggregates MFA status across the tenant
* Outputs a structured report suitable for further analysis

### Key Concepts Demonstrated

* Microsoft Graph API usage
* Data aggregation and reporting
* Security posture visibility through automation

### Notes

* API authentication and scopes are abstracted
* Output format can be adapted for CSV, JSON, or dashboards

---

# Network Automation

## Overview

Network troubleshooting often involves correlating information across multiple systems under time pressure.

The scripts in this directory demonstrate automation patterns that reduce mean-time-to-resolution (MTTR).

---

## `mac-address-trace.py`

### Problem

Tracing a device by MAC address across switches, logs, or inventory systems is traditionally a manual, multi-step process.

### Solution

This script:

* Accepts a MAC address as input
* Queries network data sources to locate the device
* Outputs a clear trace path for troubleshooting

### Key Concepts Demonstrated

* Network-focused automation
* Data normalization (MAC formats)
* Iterative lookup patterns
* Read-only automation for safe operations

### Notes

* Network endpoints and credentials are removed
* Script is intentionally non-intrusive and read-only

---

## Final Notes

This repository is intentionally focused on clarity and intent, not completeness.

The emphasis is on maintainable, understandable automation that can be safely adapted to real environments.
