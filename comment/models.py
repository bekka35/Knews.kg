from django.db import models

from articles.models import News
from category.models import NewsCategory


class Comment(models.Model):
    author = models.CharField(max_length=50)
    body = models.TextField()
    articles = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.body

