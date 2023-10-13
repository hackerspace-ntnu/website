from rest_framework import viewsets

from news.models import Upload
from news.serializers.upload import UploadSerializer


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
