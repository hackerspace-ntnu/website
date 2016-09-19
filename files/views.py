from django.shortcuts import render
from .models import Image
from .forms import ImageUpload, ImageSearch, ImageEdit
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
#from x import admin_history
import os
from django.conf import settings
from news.templatetags import check_user_group as groups

def findId(title):
    number = 1
    for element in Image.objects.order_by('-time'):
        savename = element.title.lower()
        while ' ' in savename:
            savename = savename.replace(' ', '_')
        if title.lower() == savename:
            return element.number + 1
    return number

def fileExt(name):
    return name.split('.')[-1:][0]

def saveImage(file, title, description, tags):
    savename = title.lower()
    while " " in savename:
        savename = savename.replace(' ', '_')
    number = findId(savename)
    if number > 1:
        file.name = savename + '_'+str(number) + '.' + fileExt(file.name)
    else:
        file.name = savename + '.' + fileExt(file.name)
    instance = Image(file=file, title=title, description=description, tags=tags, time=timezone.now(), number=number)
    instance.save()
    return instance

def renameImage(instance, title):
    savename = title.lower()
    while ' ' in savename:
        savename = savename.replace(' ', '_')
    instance.number = findId(title)
    oldpath = instance.file.name
    directory = settings.MEDIA_ROOT
    if instance.number > 1:
        instance.file.name = 'images/'+savename+'_'+str(instance.number)+'.'+fileExt(instance.file.name)
    else:
        instance.file.name = 'images/'+savename+'.'+fileExt(instance.file.name)
    #try:
    os.rename(directory+'/'+oldpath, directory+'/'+instance.file.name)
    #except FileNotFoundError:
    #    pass
    instance.save()
    return instance

def imageUpload(request):
    if groups.has_group(request.user, 'member'):
        if request.method == 'POST':
            form = ImageUpload(request.POST, request.FILES)
            if form.is_valid():
                img = saveImage(request.FILES['file'], form.cleaned_data['title'], form.cleaned_data['description'], form.cleaned_data['tags'])
                context = {
                    'src': img.file.name,
                }
                return render(request, 'image_upload_done.html', context)
        else:
            form = ImageUpload(initial={
                'description': '',
                'title': '',
                'tags': '',
            })

        context = {
            'form': form,
        }
        return render(request, 'image_upload.html', context)
    else:
        return HttpResponseRedirect('/authentication/login')

def images(request):
    if groups.has_group(request.user, 'member'):
        searchText = ''
        if request.method == 'POST':
            form = ImageSearch(request.POST)
            images = []
            if form.is_valid():
                searchText = form.cleaned_data['search']
                search = searchText.lower()
                for image in Image.objects.order_by('-time'):
                    if search in image.title.lower() or search in image.tags.lower():
                        images.append(image)
            else:
                images = Image.objects.order_by('-time')
        else:
            images = Image.objects.order_by('-time')
        form = ImageSearch()
        context = {
            'images': images,
            'form': form,
            'searchText': searchText,
        }
        return render(request, 'images.html', context)
    else:
        return HttpResponseRedirect('/authentication/login')

def imageDelete(request, image_id):
    if groups.has_group(request.user, 'member'):
        try:
            image = Image.objects.get(pk=image_id)
            image.delete()
            #admin_history.log_deletion(request, image)
        except Image.DoesNotExist:
            pass
        return HttpResponseRedirect('/files/images')
    else:
        return HttpResponseRedirect('/authentication/login')

def imageView(request, image_id):
    try:
        image = Image.objects.get(pk=image_id)
        return HttpResponseRedirect('/media/'+str(image.file))
    except Image.DoesNotExist:
        return HttpResponseRedirect('/')

def imageEdit(request, image_id):
    if groups.has_group(request.user, 'member'):
        if request.method == 'POST':
            form = ImageEdit(request.POST)
            if form.is_valid():
                try:
                    image = Image.objects.get(pk=image_id)
                    title = form.cleaned_data['title']
                    if title != image.title:
                        image = renameImage(image, title)
                    image.title = title
                    image.description = form.cleaned_data['description']
                    image.tags = form.cleaned_data['tags']
                    image.save()
                    #admin_history.log_change(request, image)
                except Image.DoesNotExist:
                    pass
                return HttpResponseRedirect('/files/images')
        else:
            try:
                image = Image.objects.get(pk=image_id)
            except Image.DoesNotExist:
                return HttpResponseRedirect('/files/images')

            form = ImageEdit(initial={
                'title': image.title,
                'description': image.description,
                'tags': image.tags,
                'file': image.file,
            })
        context = {
            'form': form,
        }

        return render(request, 'image_edit.html', context)
    else:
        return HttpResponseRedirect('/authentication/login')
