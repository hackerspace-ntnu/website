from django import template
register = template.Library()

@register.inclusion_tag('files/single-image.html')
def render_image(image):
    context_image = {'image': image}
    return context_image
