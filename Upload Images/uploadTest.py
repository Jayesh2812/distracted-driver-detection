import requests
from requests.auth import HTTPBasicAuth

payload = HTTPBasicAuth('admin', 'admin')

f = open('download (1).jpg','rb' )

url = 'http://127.0.0.1:8000/upload/'

response = requests.post(url, auth=payload , files= {'image':f})

print(response.text)