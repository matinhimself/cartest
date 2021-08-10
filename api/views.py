import rest_framework.parsers
import rest_framework.renderers
import rest_framework_json_api.parsers
import rest_framework_json_api.renderers
from django.contrib import auth
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from rest_framework_json_api.views import ModelViewSet

from .models import Question, BlogPost, Category
from .permissions import IsAuthorOrReadOnly, IsSuperUserOrReadOnly
from .serializers import QuestionSerializer, BlogQuerySetSerializer, TagSerializer


class JsonApiViewSet(ModelViewSet):
    pagination_class = JsonApiPageNumberPagination
    parser_classes = [
        rest_framework_json_api.parsers.JSONParser,
        rest_framework.parsers.FormParser,
        rest_framework.parsers.MultiPartParser,
    ]
    renderer_classes = [
        rest_framework_json_api.renderers.JSONRenderer,
        rest_framework.renderers.BrowsableAPIRenderer,
    ]


def get_user(request):
    return  auth.get_user(request)
    # if not hasattr(request, '_cached_user'):
    #     request._cached_user = auth.get_user(request)
    # return request._cached_user


class TagRetrieveView(ListAPIView):
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        title = self.kwargs.get('title')
        if is_subscribed(self.request.user):
            return Question.objects.filter(tags__title=title)
        else:
            return Question.objects.filter(tags__title=title, visibility='p')


class TagListView(ListAPIView):
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = TagSerializer
    queryset = Category.objects.all()


class QuestionRetrieve(RetrieveAPIView):
    pagination_class = JsonApiPageNumberPagination
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)

    def get_queryset(self):
        if is_subscribed(self.request.user):
            return Question.objects.all()
        else:
            return Question.objects.filter(visibility='p')

    serializer_class = QuestionSerializer


class QuestionListView(ListAPIView):
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        if is_subscribed(self.request.user):
            return Question.objects.all()
        else:
            return Question.objects.filter(visibility='p')


# class BlogVewSet(JsonApiViewSet):
#     http_method_names = ['get', 'head', 'options']
#     permission_classes = (IsStaffOrReadOnly,)
#
#     def head(self, *args, **kwargs):
#         last_book = self.get_queryset().latest('publication_date')
#         response = HttpResponse()
#         response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
#
#         return response
#
#     serializer_class = BlogQuerySetSerializer
#     queryset = BlogPost.objects.filter(status__exact='p')


class BlogPostListView(ListAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = BlogQuerySetSerializer
    pagination_class = JsonApiPageNumberPagination
    model = BlogPost
    queryset = BlogPost.objects.filter(status='p')

    def get_queryset(self):
        if is_subscribed(self.request.user):
            return BlogPost.objects.filter(status='p')
        else:
            return BlogPost.objects.filter(status='p', visibility='p')

    context_object_name = 'blog_posts'


def is_subscribed(user):
    if user and user.is_authenticated and user.is_subscribed():
        return True
    return False


class BlogPostDetailView(RetrieveAPIView):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthorOrReadOnly,)
    lookup_field = 'slug'
    queryset = BlogPost.objects.filter(status='p')
    serializer_class = BlogQuerySetSerializer
