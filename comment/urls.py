from django.urls import path
from .views import ListComment, ListDetailComment

urlpatterns = [
    path('comment/', ListComment.as_view()),
    path('comment/<int:pk>/', ListDetailComment.as_view()),
]
