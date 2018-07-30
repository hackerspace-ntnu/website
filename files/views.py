from django.shortcuts import render
from .models import Image
from .forms import ImageForm
from .templatetags.render_single_image import render_image
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from authentication.templatetags import check_user_group as groups

@login_required()
def images(request):
    if groups.has_group(request.user, 'member'):
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit = False)
                image.save()
        else:
            form = ImageForm()

        images = Image.objects.order_by('-time')
        searchText = ''
        context = {
            'images': images,
            'UploadForm': form,
            'searchText': searchText,
        }
        return render(request, 'files/images.html', context)
    return HttpResponseRedirect("/")

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
