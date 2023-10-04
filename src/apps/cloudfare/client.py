import httpx
from dataclasses import dataclass
import json

from django.conf import settings

from apps.cloudfare.exceptions import HTTPError

import http.client
import mimetypes
from codecs import encode


class CloudfareImageResizingClient:

    def fetch_direct_links(self):
        """
        I use this stupid implementation cause I didn't find solve to error:
        ERROR 5415: Images must be uploaded as a form, not as raw image data. Please use multipart/form-data format
        """

        conn = http.client.HTTPSConnection("api.cloudflare.com")
        dataList = []
        boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=requireSignedURLs;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("true"))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=metadata;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))

        dataList.append(encode("{\"key\":\"value\"}"))
        dataList.append(encode('--'+boundary+'--'))
        dataList.append(encode(''))

        body = b'\r\n'.join(dataList)
        payload = body

        headers = {
        'Authorization': f'Bearer {settings.CLOUDFARE_API_TOKEN}',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("POST", f"/client/v4/accounts/{settings.CLOUDFARE_ACCOUNT_ID}/images/v2/direct_upload", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))        
