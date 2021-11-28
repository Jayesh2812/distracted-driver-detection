import cv2
import base64
import requests
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth('admin', 'admin')
img = cv2.imread('./__pycache__/img_100003.jpg')
base64_str = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()

response = requests.post(
        url="http://localhost:8000/upload-encoded/",
        data={"image" : base64_str}, 
        auth = auth
    )
print(response.json())

  