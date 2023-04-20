from django.shortcuts import render
from rest_framework import generics

from comment.models import Comment
from comment.serializers import CommentSerializer


class ListComment(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ListDetailComment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

