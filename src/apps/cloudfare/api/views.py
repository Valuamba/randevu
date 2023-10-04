from apps.cloudfare.client import CloudfareImageResizingClient

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from randevu.errors import safe_run


class RetrieveUniqueCloudfareImageResizingLinks(APIView):
    @safe_run()
    def get(self, request, count):
        links = []
        count = int(count)
        if count == 0:
            raise Exception('Count of links cannot be equal to zero.')

        for i in range(count):
            client = CloudfareImageResizingClient()
            result = client.fetch_direct_links()
            links.append(result['result']['uploadURL'])

        return Response(data=links, status=status.HTTP_200_OK)
