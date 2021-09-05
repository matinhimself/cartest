from rest_framework_json_api import serializers

from users.models import CustomUser
from .models import Question, BlogPost, Choice, Category, Exam, QuestionSet


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class QSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSet
        fields = ['name', 'questions', 'author']


class QSetUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'first_name', 'last_name', ]
        extra_kwargs = {
            'view_name': 'users__profile'
        }


class QSetListSerializer(serializers.ModelSerializer):
    user = QSetUserSerializer(source="author", read_only=True)

    class Meta:
        model = QuestionSet
        fields = ['name', 'user']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'image']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'visibility'
            , 'text'
            # , 'hints'
            , 'choices'
            , 'tags'
            # , 'votes'
            , 'answer'
            # , 'publish'
        )


#
# class UserModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ['username']


class BlogQuerySetSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.first_name', read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "created_at",
            "author_name",
            "visibility",
            "thumbnail",
            "description",
        ]
