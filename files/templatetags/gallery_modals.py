from django import template
from files.models import Image
from files.forms import ImageForm

register = template.Library()

@register.inclusion_tag('files/images-modal.html')
def ImagePickModal(request):
    images = Image.objects.order_by('img_category', '-time')

    return {'images': images}

@register.inclusion_tag('files/_upload_modal.html')
def ImageUploadModal(request):
    return {'UploadForm': ImageForm(prefix="img")}