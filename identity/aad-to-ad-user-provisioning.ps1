Connect-MgGraph

# Change the username to match their AAD account
$usersToCreate = "user1@example.com", "user2@example.com"

# This is org specific, whether the user is Shop or Office
$shopOffice = "Office"
$password = Read-Host -AsSecureString

Class Attributes {
    $AAD = $string
    $AD = $string
}

$attributeMap = @(
    [Attributes]@{AAD = "OfficeLocation"; AD = "Office"},
    [Attributes]@{AAD = "JobTitle"; AD = "Title"},
    [Attributes]@{AAD = "Department"; AD = "Department"},
    [Attributes]@{AAD = "CompanyName"; AD = "Company"},
    [Attributes]@{AAD = "BusinessPhones"; AD = "OfficePhone"},
    [Attributes]@{AAD = "DisplayName"; AD = "DisplayName"},
    [Attributes]@{AAD = "GivenName"; AD = "GivenName"},
    [Attributes]@{AAD = "Surname"; AD = "Surname"},
    [Attributes]@{AAD = "UserPrincipalName"; AD = "UserPrincipalName"},
    [Attributes]@{AAD = "DisplayName"; AD = "Name"}
)

foreach ($user in $usersToCreate) {
    Write-Host "`nNow serving:"$user"`n"

    try {
        $AADUser = Get-MgUser -UserId $user -Property OfficeLocation, JobTitle, Department, CompanyName, BusinessPhones, DisplayName, GivenName, Surname, UserPrincipalName, ProxyAddresses -ExpandProperty Manager
    }
    catch {
        $AADUser = $null
    }

    $passwd = ConvertTo-SecureString -String $password -AsPlainText -Force
    $username = $AADuser.UserPrincipalName.Split("@")
    try {
        $samAccountName = $username[0].Substring(0, 20)
    }
    catch {
        $samAccountName = $username[0]
    }
    

    if($AADUser) {
        $params = @{
            SamAccountName = $samAccountName
            Path = "DC=contoso,DC=com"
            AccountPassword = $passwd
            ChangePasswordAtLogon = $true
            Country = "US"
            Enabled = $true
            HomeDrive = "H:"
            HomeDirectory = "\\fileserver\users\$samAccountName"
        }
        try {
            $currentManager = (Get-aduser $user.manager).UserPrincipalName
        }
        catch {
            $currentManager = $null
        }
        try {
            $AADManager = (Get-MgUser -UserId $AADuser.manager.Id).UserPrincipalName
            $manager = $AADManager.split("@")
        }
        catch {
            $AADManager = $null
            $manager = $null
        }
        if ($AADManager -ne $currentManager) {
            $params += @{Manager = $manager[0]}
            write-host "USER: "$user.UserPrincipalName"ATTRIBUTE: Manager updating to"$manager[0]
        }
        
        foreach ($line in $attributeMap) {
            $ladAtrName = $line.AD
            $aadAtrName = $line.AAD
            if(($user.$ladAtrName -ne $AADUser.$aadAtrName) -and ($null -ne $AADUser.$aadAtrName)) {
                if ($user.$ladAtrName -eq "BusinessPhones") {
                    write-host "USER:"$user.UserPrincipalName "ATTRIBUTE: $ladAtrName updating from " $user.$ladAtrName "to" $AADUser.$aadAtrName[0]
                    $AADval = $AADUser.$aadAtrName[0].trim()
                    $params += @{$ladAtrName = $AADVal} 
                }
                else{
                    write-host "USER:"$user.UserPrincipalName "ATTRIBUTE: $ladAtrName updating from " $user.$ladAtrName "to" $AADUser.$aadAtrName
                    $AADval = $AADUser.$aadAtrName.trim()
                    $params += @{$ladAtrName = $AADVal}
                }
            }
        }

        New-ADUser @params 
        Set-ADUser $samAccountName -add @{ProxyAddresses = $AADUser.proxyaddresses -split ","; extensionAttribute1 = "$shopOffice"}

    } else {
        Write-Host -BackgroundColor Red -ForegroundColor Cyan "USER:" $locADUser.UserPrincipalName "does not exist in AzureAD"
    }
}
