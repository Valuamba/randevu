from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.locales.x_codes import ERROR_LOCALES
# Create your views here.


class GetLocalesAPIView(APIView):
    def get(self, request):
        return Response(data=ERROR_LOCALES, status=status.HTTP_200_OK)
