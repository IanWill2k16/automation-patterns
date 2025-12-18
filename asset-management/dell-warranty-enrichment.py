import requests
import json
import pandas as pd
from datetime import date,datetime
import os

today = datetime.combine(date.today(), datetime.min.time())

# Retrieve access token
token_authority = os.getenv("DELL_TOKEN_AUTHORITY")
client_id = os.getenv("DELL_CLIENT_ID")
client_secret = os.getenv("ADELL_CLIENT_SECRET")

token_payload = {'client_id': client_id, "client_secret": client_secret, 'grant_type': 'client_credentials'}
token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

token_request = requests.post(token_authority, headers=token_headers, data=token_payload).json()
token = token_request['access_token']

servicetags = pd.read_csv("./data/devices.csv)

servicetags = servicetags.drop(columns=['RunspaceId', 'PSShowComputerName'])
servicetags['WarrantyStart']=''
servicetags['DeviceType']=''
servicetags['Age']=''

# Perform the query
rangeList = range(0,len(servicetags))
iterationCount = int(len(servicetags)/100) + 1
indexArray = []

begin = 0
end = 100
for loop in range(iterationCount):
    indexArray.append(rangeList[begin:end])
    begin = end
    end += 100

warranty_headers = {'Authorization': 'Bearer ' + token}
counter = 0
for j in indexArray:
    tags = []
    for i in j:
        tags.append(servicetags.loc[i]['SerialNumber'])
        servicetags.loc[i]['SerialNumber']
    tag = {'servicetags': tags}
    warranty_requests = requests.get('https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/asset-entitlements', headers=warranty_headers, params=tag).json()
    
    for i in j:
        currentRequestIndex = None
        for item in range(len(warranty_requests)):
            if servicetags.loc[i]['SerialNumber'] in warranty_requests[item]['serviceTag']:
                currentRequestIndex = item
        print(str(i) + " " + str(currentRequestIndex) + " " + str(counter))
        # print(servicetags.loc[i])
        try:
            warranty = warranty_requests[currentRequestIndex]['entitlements'][0]['startDate'].split("T")
            servicetags.loc[i, 'WarrantyStart'] = (warranty[0])
            servicetags.loc[i, 'DeviceType'] = (warranty_requests[currentRequestIndex]['productLineDescription'])
            date_string = datetime.strptime(warranty[0],'%Y-%m-%d')        
            servicetags.loc[i, 'Age'] = round((((today - date_string).days)/365), 2)
        except:
            if len(servicetags.loc[i]['SerialNumber']) > 7:
                servicetags.loc[i, 'DeviceType'] = 'Not Dell'
                servicetags.loc[i, 'WarrantyStart'] = 'Unknown'
                servicetags.loc[i, 'Age'] = 'Unknown'           
            else:
                servicetags.loc[i, 'DeviceType'] = 'Missing'
                servicetags.loc[i, 'WarrantyStart'] = 'Missing'
                servicetags.loc[i, 'Age'] = 'Missing'
    counter += 100

servicetags.to_csv('./output/warrantyinfo.csv', index=False)
