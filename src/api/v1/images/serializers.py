from rest_framework import serializers

from api.v1.images.models import Image, NFTRequest
from api.v1.images.tasks import generate_nft #,generate_nft_native


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ['id', 'image_url', 'uuid']

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
        IMAGE_COUNT = 3
        model = self.Meta.model.objects.create(**validated_data)
        model.save()
        for i in range(0, IMAGE_COUNT):
            generate_nft.apply_async(
                args=[model.id])
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