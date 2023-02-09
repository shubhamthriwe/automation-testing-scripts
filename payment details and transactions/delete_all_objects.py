import json
import requests

header = {
        "X-Parse-Application-Id" : "APPLICATION_ID",
        "X-Parse-Master-Key" : "MASTER_KEY",
        "Content-Type": "application/json",
        "X-Transactions-Server" : "1"
    }
parseClass = "paymentDetails"
limit = 100000
url = f'https://dev.ext-api.thriwe.com/parse/classes/{parseClass}?limit={limit}'
batchUrl = 'https://dev.ext-api.thriwe.com/parse/batch'
batchList = []
req_payload = {
    "objectId" : ""
}
batchPath = f"/parse/classes/{parseClass}/"
batch = {
        "method": "DELETE",
        "path": ""
    }

count = 0
response = requests.request("GET", url, headers = header)
responseObj = response.json()
result = responseObj.get('results')

for i in result[:]:
    count += 1
    objectId = i.get('objectId')
    batch["path"] = batchPath + objectId 
    batchList.append(batch.copy())
print(count)
# print(*batchList)

for i in range(0,count,50):
    batchObj = json.dumps({
            "requests" : batchList[i:i+50]
        })
    res = requests.request("POST", batchUrl, headers = header, data = batchObj).json()
    print(res)


header = {
        "X-Parse-Application-Id" : "APPLICATION_ID",
        "X-Parse-Master-Key" : "MASTER_KEY",
        "Content-Type": "application/json",
        "X-Transactions-Server" : "1"
    }
parseClass = "paymentTransactions"
limit = 100000
url = f'https://dev.ext-api.thriwe.com/parse/classes/{parseClass}?limit={limit}'
batchUrl = 'https://dev.ext-api.thriwe.com/parse/batch'
batchList = []
req_payload = {
    "objectId" : ""
}
batchPath = f"/parse/classes/{parseClass}/"
batch = {
        "method": "DELETE",
        "path": ""
    }

count = 0
response = requests.request("GET", url, headers = header)
responseObj = response.json()
result = responseObj.get('results')

for i in result[:]:
    count += 1
    objectId = i.get('objectId')
    batch["path"] = batchPath + objectId 
    batchList.append(batch.copy())
print(count)
# print(*batchList)

for i in range(0,count,50):
    batchObj = json.dumps({
            "requests" : batchList[i:i+50]
        })
    res = requests.request("POST", batchUrl, headers = header, data = batchObj).json()
    print(res)