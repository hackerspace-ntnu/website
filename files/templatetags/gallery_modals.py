from django import template

from files.forms import ImageForm
from files.models import FileCategory, Image

register = template.Library()


@register.inclusion_tag("files/images-modal.html")
def ImagePickModal(request):
    images = Image.objects.all()
    categorized = {}

    for category in FileCategory.objects.all().order_by("name"):
        category_images = Image.objects.filter(img_category=category).order_by("-time")
        if category_images:
            categorized[category.name] = category_images

    return {"categories": categorized}


@register.inclusion_tag("files/_upload_modal.html")
def ImageUploadModal(request):
    return {"UploadForm": ImageForm(prefix="img")}
