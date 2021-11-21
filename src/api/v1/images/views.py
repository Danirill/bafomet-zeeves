import django_filters
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import requires_csrf_token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
import django_filters.rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView
import random

from WellbeApi import settings
from api.v1.images.models import Image, NFTRequest
from api.v1.images.serializers import ImageSerializer, NFTRequestSerializer
from utils.utils import parse_int

class GetImageById(APIView):
    def get(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
            return Response(ImageSerializer(image, context={'request': request}).data, status.HTTP_200_OK)
        except:
            return Response({}, status.HTTP_404_NOT_FOUND)


class GetImageByUUID(APIView):
    def get(self, request, image_uuid):
        try:
            image = Image.objects.get(uuid=image_uuid)
            return Response(ImageSerializer(image, context={'request': request}).data, status.HTTP_200_OK)
        except:
            return Response({}, status.HTTP_404_NOT_FOUND)


class NFTCreateView(generics.CreateAPIView):
    queryset = NFTRequest.objects.all()
    serializer_class = NFTRequestSerializer


# class NFTNativeCreateView(generics.CreateAPIView):
#     queryset = NFTRequest.objects.all()
#     serializer_class = NativeNFTRequestSerializer


class NFTRetrieveView(APIView):
    # serializer_class = NFTRequestSerializer
    def get(self, request, pk):
        try:
            nft_request = NFTRequest.objects.get(id=pk)
        except NFTRequest.DoesNotExist:
            return Response({}, status.HTTP_404_NOT_FOUND)

        result_count = nft_request.result.count().real

        if result_count >= 2:
            return Response(NFTRequestSerializer(nft_request, context={"request": request}).data, status.HTTP_200_OK)
        elif result_count == 0:
            return Response(NFTRequestSerializer(nft_request, context={"request": request}).data, status.HTTP_204_NO_CONTENT)
        else:
            return Response(NFTRequestSerializer(nft_request, context={"request": request}).data, status.HTTP_201_CREATED)


class NFTRequestFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = NFTRequest
        fields = ['owner']


class NFTRequestListView(generics.ListAPIView):
    queryset = NFTRequest.objects.all()
    serializer_class = NFTRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NFTRequestFilter


class ImageFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Image
        fields = ['owner']


class ImageFilterListView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ImageFilter

