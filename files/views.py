from django.shortcuts import render
from .models import Image
from .forms import ImageForm
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

class ImageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Image
    success_url = '/files/images'
    permission_required = "files.delete_image"

class ImageListView(PermissionRequiredMixin, ListView):
    queryset = Image.objects.order_by('-time')
    template_name = 'files/images.html'
    permission_required = "files.view_image"


class ImageView(PermissionRequiredMixin, View):
    permission_required = "files.view_image"
    def get(self, request, *args, **kwargs):
        image = get_object_or_404(Image, pk=kwargs['pk'])
        return HttpResponseRedirect('/media/'+str(image.file))

@login_required()
def imageUpload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, prefix='img')
        if form.is_valid():
            image = form.save(commit = False)
            image.save()
            return render(request, 'files/single-image.html', {'image':image})
        else:
            return HttpResponse(form.errors)
    else:
        return HttpResponseRedirect('/')
