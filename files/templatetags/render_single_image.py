from django import template
register = template.Library()

''' This returns HTML for use with Ajax to append image picker after uploading '''
@register.inclusion_tag('files/single-image.html')
def render_image(image):
    context_image = {'image': image}
    return context_image
