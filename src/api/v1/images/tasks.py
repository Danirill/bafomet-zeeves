import io
from http.client import RemoteDisconnected

from django.core.files import File

from WellbeApi.celery import app
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

import requests
import WellbeApi.settings as Settings
from api.v1.images.models import NFTRequest, Image
from api.v1.variables.models import Variable
# from utils.image_generator.main import generate
from utils.utils import get_token

headers = {
    "Content-Type": "application/json",
}


@app.task
def generate_nft(nft_request_id):
    try:
        nft_request = NFTRequest.objects.get(id=nft_request_id)
    except NFTRequest.DoesNotExist:
        return
    BASE_URL = Variable.objects.get(key='RUDALLE_URL').value
    print(BASE_URL)
    url = f"{BASE_URL}?message={nft_request.key}"

    response = requests.request("GET", url, headers=headers, timeout=60*10)
    try:
        response.raise_for_status()
        print(response)
        in_memory_file = io.BytesIO(response.content)
        image = Image.objects.create(owner=nft_request.owner, text=nft_request.key)
        image.image.save(
            get_token(10),
            File(in_memory_file, 'rb'))
        image.save()
        nft_request.result.add(image)
        nft_request.save()
        print("SAVING IMAGE!")
    except RemoteDisconnected:
        pass
    except requests.exceptions.HTTPError as e:
        nft_request.broken = True
        nft_request.save()
        print(e)

# @app.task
# def generate_nft_native(nft_request_id):
#     try:
#         nft_request = NFTRequest.objects.get(id=nft_request_id)
#     except NFTRequest.DoesNotExist:
#         return
#
#     in_memory_file = generate(nft_request.key)
#     image = Image.objects.create()
#     image.image.save(
#         get_token(10),
#         File(in_memory_file, 'rb'))
#     image.save()
#     nft_request.result.add(image)
#     nft_request.save()

