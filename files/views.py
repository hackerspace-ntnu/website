from django.shortcuts import render
from .models import Image
from .forms import ImageForm
from .templatetags.render_single_image import render_image
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

class ImageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Image
    success_url = '/files/images'
    permission_required = "files.delete_image"

class ImageListView(PermissionRequiredMixin, ListView):
    model = Image
    template_name = 'files/images.html'
    permission_required = "files.view_image"


@login_required()
def imageUpload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, prefix='img')
        if form.is_valid():
            image = form.save(commit = False)
            image.save()
            return ajax_return_last_image(request)
        else:
            return HttpResponse(form.errors)
    else:
        return HttpResponseRedirect('/')

@login_required()
def imageDelete(request, id):
    if request.method == 'POST':
        image = Image.objects.get(id=id)
        image.delete()

    else:
        return HttpResponseRedirect('/')

def ajax_return_last_image(request):
    last_image = Image.objects.order_by('-time')[0]
    return render(request, 'files/single-image.html', {'image':last_image})


@login_required()
def imageView(request, image_id):
    try:
        image = Image.objects.get(pk=image_id)
        return HttpResponseRedirect('/media/'+str(image.file))
    except Image.DoesNotExist:
        return HttpResponseRedirect('/')

@login_required()
def modalpicker(request):
    images = Image.objects.order_by('-time')
    return images
