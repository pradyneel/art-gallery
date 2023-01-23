# import requests
import json

# url = "https://api.beaconstac.com/api/2.0/qrcodes/1469111/download/?size=1024&error_correction_level=5&canvas_type=png"

# payload={}
# headers = {
#   'Authorization': 'Token bd2149fd3ad6748f72ebae26c7ceed035af67084'
# }

# response = requests.request("GET", url, headers=headers, data=payload)
# dictResponse = json.loads(response.text)

# image_id = dictResponse['urls']['png']
# image_name = dictResponse['name']
# print(image_name)
# print(image_id)


import requests

url = "https://api.beaconstac.com/api/2.0/qrcodes/"

payload={}
headers = {
  'Authorization': 'Token bd2149fd3ad6748f72ebae26c7ceed035af67084'
}

response = requests.request("GET", url, headers=headers, data=payload)
dictResponse = json.loads(response.text)

# print(dictResponse['results'])

for dict in dictResponse['results']:
  if(dict['state'] == 'A'):
    print(dict['id'],dict['state'])