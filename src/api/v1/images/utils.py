from django.core.files.storage import FileSystemStorage

from api.v1.images.models import Image


def upload_image(request):
    f = request.FILES['image']
    fs = FileSystemStorage()
    filename = str(f).split('.')[0]
    file = fs.save(filename, f)
    return Image.objects.create(image=file)
