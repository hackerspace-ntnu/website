from django import template
from files.models import Image
from files.forms import ImageForm

register = template.Library()

@register.inclusion_tag('files/images-modal.html')
def ImagePickModal(request):
    images = Image.objects.order_by('tags', '-time')

    return {'UploadForm': ImageForm(prefix="img"), 'images': images}
