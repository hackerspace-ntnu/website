from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from .forms import ImageForm
from .models import FileCategory, Image


class ImageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Image
    success_url = "/files/images"
    permission_required = "files.delete_image"


class ImageListView(PermissionRequiredMixin, ListView):
    queryset = Image.objects.order_by("img_category", "-time")
    template_name = "files/images.html"
    permission_required = "files.view_image"
    context_object_name = "categories"

    def get_queryset(self):
        images = Image.objects.all()
        categorized = {}

        for category in FileCategory.objects.all().order_by("name"):
            category_images = Image.objects.filter(img_category=category).order_by(
                "-time"
            )
            if category_images:
                categorized[category.name] = category_images
        return categorized


class ImageView(PermissionRequiredMixin, View):
    permission_required = "files.view_image"

    def get(self, request, *args, **kwargs):
        image = get_object_or_404(Image, pk=kwargs["pk"])
        return HttpResponseRedirect("/media/" + str(image.file))


@login_required()
def imageUpload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, prefix="img")
        if form.is_valid():
            image = form.save(commit=False)
            image.save()
            return render(request, "files/single-image.html", {"image": image})
        else:
            return HttpResponse(form.errors)
    else:
        return HttpResponseRedirect("/")
