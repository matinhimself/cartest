from django.urls import path, include

from .views import QuestionRetrieve, QuestionListView, TagRetrieveView, BlogPostListView, BlogPostDetailView, \
    TagListView, QuestionLike, QuestionSetsListView, SetLike, QuestionSetRetrieve

app_name = "api"

urlpatterns = [
    path(r"q", QuestionListView.as_view(), name="q_list"),
    path(r"q/<int:pk>", QuestionRetrieve.as_view(), name="q_retrieve"),
    path(r"set/<int:pk>", QuestionSetRetrieve.as_view()),
    path(r"q/like/<int:pk>", QuestionLike.as_view(), name="q_retrieve"),
    path(r"tag/<str:title>", TagRetrieveView.as_view(), name="tag_retrieve"),
    path(r"tag", TagListView.as_view(), name="tag_list"),
    path(r'blog/', BlogPostListView.as_view(), name='list'),
    path(r'blog/<slug>', BlogPostDetailView.as_view(), name='detail'),
    path(r'set', QuestionSetsListView.as_view()),
    path(r'set/like/<int:pk>', SetLike.as_view()),
]
