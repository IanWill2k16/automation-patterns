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

## `autopilot-device-reconciliation.ps1`

### Problem

In hybrid AD / Entra ID environments, devices are often provisioned with temporary or generic hostnames during imaging, while the authoritative device identity is defined later in Intune / Autopilot.

Reconciling these names manually requires:

* Cross-referencing serial numbers
* Matching devices across multiple systems
* Performing privileged rename and reboot operations

This process is time-consuming, error-prone, and difficult to scale.

### Solution

This script:

* Queries on-prem Active Directory for computer objects
* Authenticates to Microsoft Graph using an application identity
* Enumerates Windows Autopilot device identities (handling pagination)
* Matches devices by hardware serial number
* Renames computers only when all validation checks pass
* Reboots devices only after a successful rename

The automation is designed to be defensive and idempotent, minimizing operational risk.

### Key Concepts Demonstrated

* Hybrid identity automation (AD + Entra ID)
* Microsoft Graph API integration
* OAuth2 client credentials flow
* Hardware-based identity correlation
* Safe handling of privileged operations

### Notes

* Tenant IDs, client IDs, and secrets are represented as placeholders
* In production, secrets were retrieved from a secure secret store
* Script logic avoids destructive actions unless all prerequisites are met

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
