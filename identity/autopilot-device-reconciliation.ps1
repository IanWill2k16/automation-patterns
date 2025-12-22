function Get-DomainCredential {
    throw "Credential retrieval intentionally omitted in sanitized version."
}

# Placeholder for secure credential retrieval
$creds = Get-DomainCredential

# NOTE:
# In production, these values were retrieved from a secure secret store.
# They are represented here as placeholders for demonstration purposes.

$tenantId = '<TENANT_ID>'
$clientId = '<CLIENT_ID>'
$clientSecret = '<CLIENT_SECRET>'

$devices = get-adcomputer -searchbase "DC=contoso,DC=com" -filter *

$authority = 'https://login.microsoftonline.com/{0}/oauth2/v2.0/token' -f $tenantId

# Request a token
$tokenHeader = @{'Content-Type' = 'application/x-www-form-urlencoded' }

$tokenBody = @{
    client_id = $clientId
    scope = 'https://graph.microsoft.com/.default'
    client_secret = $clientSecret
    grant_type = 'client_credentials'
}

$token = Invoke-WebRequest -Method 'POST' -Uri $authority -Headers $tokenHeader -Body $tokenBody -UseBasicParsing
$tokenObj = ConvertFrom-Json $token

# Prepare the request
$deviceRequestURL = "https://graph.microsoft.com/v1.0/deviceManagement/windowsAutopilotDeviceIdentities"
$deviceRequestHeaders = @{
    Authorization = "Bearer $($tokenObj.access_token)"
}

$deviceList = @()

while ($deviceRequestURL) {
    $response = Invoke-WebRequest -Uri $deviceRequestURL -Headers $deviceRequestHeaders -UseBasicParsing
    $data = ConvertFrom-Json $response
    $deviceList += $data.value
    
    try {
        $deviceRequestURL = $data.'@odata.nextLink'
    } catch {
        $deviceRequestURL = $null
    }
}

$devices | ForEach-Object {
    $name = $_.Name
    if ($name -like "Autopilot*") {
        if (Test-Connection $name -Count 1 -Quiet) {
            try {
                Write-Output "Now Serving $name."
                $deviceInfo = Invoke-Command -ComputerName $name -ScriptBlock {Get-CimInstance -class Win32_BIOS | Select-Object PSComputerName, SerialNumber}
                $deviceName = ($deviceList | Where-Object {$_.serialNumber -eq $deviceInfo.SerialNumber}).displayName
                if ($deviceName -ne $null) {
                    # Rename and reboot only after successful serial match and connectivity checks
                    $rename = Rename-Computer -ComputerName $name -NewName $deviceName -DomainCredential $creds -PassThru
                    if ($rename.HasSucceeded) {
                        Write-Output "$name will now be restarted."
                        Restart-Computer -ComputerName $name -Force
                    }
                }
            }
            catch {
                $null
            }
        }
    }
}
