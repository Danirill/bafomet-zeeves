from datetime import datetime, timedelta, timezone

from django.db.models import Count
from rest_framework import serializers

from api.v1.images.models import Image, NFTRequest, BlockedKey
from api.v1.images.tasks import generate_nft #,generate_nft_native


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    blocked = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ['id', 'image_url', 'uuid', 'owner', 'text', 'created_at', 'blocked']

    def get_blocked(self, image):
        try:
            BlockedKey.objects.get(key=image.text)
            return True
        except BlockedKey.DoesNotExist:
            return False

    def get_image_url(self, image):
        request = self.context.get('request')
        if image.url:
            return image.url
        photo_url = image.image.url
        return request.build_absolute_uri(photo_url)


class NFTRequestSerializer(serializers.ModelSerializer):
    result = ImageSerializer(read_only=True, allow_null=True, many=True)
    data = serializers.JSONField(allow_null=True, required=False)
    owner = serializers.JSONField(allow_null=True, required=False)

    class Meta:
        model = NFTRequest
        fields = '__all__'

    def create(self, validated_data):
        IMAGE_COUNT = 2
        model = self.Meta.model.objects.create(**validated_data)
        model.save()
        active_requests = NFTRequest.objects.exclude(broken=True).annotate(images_count=Count('result')).exclude(images_count__gte=IMAGE_COUNT).order_by('-created_at')
        if active_requests:
            latest_request = active_requests[0]
            if datetime.now(timezone.utc) - latest_request.created_at <= timedelta(minutes=10):
                for i in range(0, IMAGE_COUNT):
                    generate_nft.apply_async(
                        args=[model.id], eta=datetime.now(timezone.utc) + (datetime.now(timezone.utc) - latest_request.created_at) + timedelta(minutes=2, seconds=30)*i)
        else:
            for i in range(0, IMAGE_COUNT):
                generate_nft.apply_async(
                    args=[model.id], eta=datetime.now(timezone.utc) + timedelta(minutes=2, seconds=30)*i)
        return model

# class NativeNFTRequestSerializer(serializers.ModelSerializer):
#     result = ImageSerializer(read_only=True, allow_null=True, many=True)
#     data = serializers.JSONField(allow_null=True, required=False)
#
#     class Meta:
#         model = NFTRequest
#         fields = '__all__'
#
#     def create(self, validated_data):
#         IMAGE_COUNT = 1
#         model = self.Meta.model.objects.create(**validated_data)
#         model.save()
#         for i in range(0, IMAGE_COUNT):
#             generate_nft_native.apply_async(
#                 args=[model.id])
#         return model