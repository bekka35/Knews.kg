from rest_framework import viewsets
from .models import NewsCategory
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = CategorySerializer

