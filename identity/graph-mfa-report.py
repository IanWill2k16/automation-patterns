import requests
import csv
import pandas as pd

# Modify the UPN Suffix for the location that will be queried
upnSuffix = 'contoso.com'

# Define secrets
tenantId = os.getenv("AZURE_TENANT_ID")
clientId = os.getenv("AZURE_CLIENT_ID")
clientSecret = os.getenv("AZURE_CLIENT_SECRET")

authority = f'https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token'

# Request a token
tokenHeader = {'Content-Type': 'application/x-www-form-urlencoded' }
tokenBody = {
    'client_id':clientId,
    'scope':'https://graph.microsoft.com/.default',
    'client_secret':clientSecret,
    'grant_type':'client_credentials'
}

token = requests.post(authority, headers=tokenHeader, data=tokenBody).json()

# Prepare the request
userRequestURL = f"https://graph.microsoft.com/v1.0/users?$top=999&$count=true&ConsistencyLevel=eventual&$select=signInActivity&$filter=endsWith(userPrincipalName,'{upnSuffix}')"
userRequestHeaders = {'Authorization':token['access_token'], 'Content-type': 'application/json'}

userList = []

while userRequestURL != None:
    response = requests.get(userRequestURL, headers=userRequestHeaders)
    data = response.json()
    userList += data['value']
    
    try:
        userRequestURL = data['@odata.nextLink']
    except:
        userRequestURL = None

# Grab the MFA Portion
MFAList = []

MFARequestUrl = "https://graph.microsoft.com/v1.0/reports/authenticationMethods/userRegistrationDetails?`$select=isMfaRegistered,userPrincipalName"
MFARequestHeaders = userRequestHeaders = {'Authorization':token['access_token'], 'Content-type': 'application/json'}


while MFARequestUrl != None:
    MFAresponse = requests.get(MFARequestUrl, headers=MFARequestHeaders)
    MFAdata = MFAresponse.json()
    MFAList += MFAdata['value']
    
    try: 
        MFARequestUrl = MFAdata['@odata.nextLink']
    except:
        MFARequestUrl = None
    
MFAdf = pd.DataFrame(MFAList)

# Iterate over user objects
userData = []

for i in range(len(userList)):
    useradd = {}
    useradd.update({"Displayname": userList[i]['displayName']})
    useradd.update({"UserPrincipalName": userList[i]['userPrincipalName']})
    
    if 'signInActivity' in userList[i]:
        useradd.update({"Last Logon" : userList[i]['signInActivity']['lastSignInDateTime']})
    else:
        useradd.update({"Last Logon" : ""})

    useradd.update({"MFARegistered": (MFAdf.loc[MFAdf['userPrincipalName'] == userList[i]['userPrincipalName']]['isMfaRegistered']).to_string(index=False)})
    userData.append(useradd)

# Convert and Output to CSV
with open('data.csv', 'w', newline='', encoding="utf-8") as f:
    headers = ["Displayname","UserPrincipalName","LastLogon","MFARegistered"]
    writer = csv.writer(f, delimiter=',')
    writer.writerow(headers)
    for user in userData: 
        entry = [user['Displayname'],user["UserPrincipalName"],user['Last Logon'],user['MFARegistered']]  
        writer.writerow(entry)

f.close()
