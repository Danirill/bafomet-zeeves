from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import GetImageById, GetImageByUUID, NFTRetrieveView, NFTCreateView#, NFTNativeCreateView

urlpatterns = [
    path('images/<uuid:image_uuid>', GetImageByUUID.as_view()),
    path('images/<int:image_id>', GetImageById.as_view()),
    path('nft/create', NFTCreateView.as_view()),
    # path('nft/create/native', NFTNativeCreateView.as_view()),
    path('nft/<int:pk>', NFTRetrieveView.as_view()),
]
