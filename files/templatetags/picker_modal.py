from django import template
from files.views import modalpicker

register = template.Library()

@register.inclusion_tag('files/images-modal.html')
def ImagePickModal(request):
    return {'images': modalpicker(request)}

