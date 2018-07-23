from django import template
from files.forms import ImageForm
from files.views import images

register = template.Library()


@register.inclusion_tag('files/image-upload-modal.html')
def UploadModal(request):
    if request.method == 'POST':
        return {'UploadForm': ImageForm(request.POST, request.FILES)}
    else:
        form = ImageForm()
    return {'UploadForm': ImageForm()}
