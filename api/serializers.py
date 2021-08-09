from rest_framework_json_api import serializers

from .models import Question, BlogPost, Choice, Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'image']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    tags = ChoiceSerializer(many=True, read_only=True)

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
    author_name = serializers.CharField(source='author.username', read_only=True)

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
