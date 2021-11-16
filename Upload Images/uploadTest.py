import requests
from requests.auth import HTTPBasicAuth
import cv2
import os
import time
import base64
payload = HTTPBasicAuth('admin', 'admin')

img = cv2.imread('../media/Image_34.png')
url = 'http://127.0.0.1:8000/upload/'

starttime = time.time()
# p = cv2.imwrite('./temp.jpg', img)
# f = open('./temp.jpg','rb' )
retval, buffer = cv2.imencode('.jpg', img)
# jpg_as_text = base64.b64encode(buffer)
jpg_as_text = buffer.tostring()

# response = requests.post(url, auth=payload , files= {'image':buffer})
response = requests.post(url, auth=payload ,data={'image_encoded' : jpg_as_text})
# f.close()

print(response.text)
print( time.time() - starttime)