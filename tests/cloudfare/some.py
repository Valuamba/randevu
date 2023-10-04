import requests

url = "https://api.cloudflare.com/client/v4/accounts/ef569a6027f9282b19b4116ce6427f5c/images/v2/direct_upload"

payload={'requireSignedURLs': 'true',
'metadata': '{"key":"value"}'}
files=[

]
headers = {
  'Authorization': 'Bearer FKXf70GMrsVO1TC56nxJgBaDtHQc_rcQFNdR78qm',
  'Cookie': '__cflb=0H28vgHxwvgAQtjUGU56Rb8iNWZVUvXhv6YQLZ2fj5w; __cfruid=c716050d35d7c6382f2a43db1fda0ecc185b7896-1670228052'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
