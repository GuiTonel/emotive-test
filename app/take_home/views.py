from rest_framework import viewsets


class BaseViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        serializer = getattr(self, self.action + "_serializer_class", None)
        if not serializer:
            serializer = getattr(self, "serializer_class")
        return serializer
