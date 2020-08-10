from .models import News
from rest_framework import permissions
from .serializers import NewsSerializer
from rest_framework import authentication
from rest_framework import viewsets, mixins


class NewsViewSets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
