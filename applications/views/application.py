from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from applications.models import Application
from applications.serializers.application import (
    ApplicationListSerializer,
    ApplicationRetrieveSerializer,
)


class ApplicationModelViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return ApplicationListSerializer
        return ApplicationRetrieveSerializer
