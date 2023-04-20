from rest_framework import serializers

from category.models import NewsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = '__all__'

