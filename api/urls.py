from django.urls import path, include

from .views import QuestionRetrieve, QuestionListView, TagRetrieveView, BlogPostListView, BlogPostDetailView, \
    TagListView

app_name = "api"

urlpatterns = [
    path(r"q", QuestionListView.as_view(), name="q_list"),
    path(r"q/<int:pk>", QuestionRetrieve.as_view(), name="q_retrieve"),
    path(r"tags/<str:title>", TagRetrieveView.as_view(), name="tag_retrieve"),
    path(r"tags", TagListView.as_view(), name="tag_list"),
    path(r'blog/', BlogPostListView.as_view(), name='list'),
    path(r'blog/<slug>', BlogPostDetailView.as_view(), name='detail'),
]
