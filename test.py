import urllib
import json 


select item_group_id, count where user_id = ''
user_id='1'
grp_id='202034034'
cnt='2'


data =  {

        "Inputs": {

                "input1":
                {
                    "ColumnNames": ["user_id", "item_group_id", "count"],
                    "Values": [ [ user_id, grp_id, cnt ], ]
                },        },
            "GlobalParameters": {
}
    }

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/449a9beb4cd9463cb93b54b0815a6cf4/services/4bece0ff30304c3eb30e22e97c910460/execute?api-version=2.0&details=true'
api_key = 'x2v11VZSYsvp0OFKsaLmLl9P9hHgaH4ANvh4/0T3OO3T37zoOVL125Pf2pesVqDoGaDL3oaBfZvbxGub5Ga1Ew==' 
# Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'method':'POST'}

req = urllib.request.Request(url, body, headers) 

response = urllib.request.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

result = response.read()
encoding = response.info().get_content_charset('utf8')  # JSON default
obj = json.loads(result.decode(encoding))
recomm = obj['Results']['output1']['value']['Values']

for rec in recomm:
    print(rec)
