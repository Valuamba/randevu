
import httpx

TOKEN = 'SSMVU7ozgtywe2BnHfou2T4e7lVctfMH0pkIf2Ob'

files = {'file': file}

open('cat2.jpg', 'rb') as f:


response = httpx.post(url='', headers={
        'Authorization': 'Bearer SSMVU7ozgtywe2BnHfou2T4e7lVctfMH0pkIf2Ob'
    },
    files=

)

# def generateImageUploadURL():
#     headers = {"Content-Type":"application/json",
#     "Authorization":"Bearer "+api_token}    
#     reponse = requests.post("https://api.cloudflare.com/client/v4/accounts/"+cf_images_id+"/images/v1/direct_upload", headers=headers)
#     response_data = json.loads(reponse.text)
#     upload_url = response_data["result"]["uploadURL"]
#     return upload_url