from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField

from users.models import CustomUser


class BaseModel(models.Model):
    """
    Base Model
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


VIS_CHOICES = (
    ('l', "Limited"),
    ('p', "Public"),
)

STATUS_CHOICES = (
    ('d', "Draft"),
    ('p', "Publish"),
    ('r', "Removed")
)


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    is_important = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)
        verbose_name = 'tag'

    def __str__(self):
        return self.title


class Question(BaseModel):
    text = RichTextUploadingField()
    visibility = models.CharField(max_length=1, choices=VIS_CHOICES, default='l')

    hints = ArrayField(
        models.TextField(),
        default=list,
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        Category,
        blank=True,
        related_query_name="tags"
    )

    answer = models.PositiveSmallIntegerField(default=0, blank=True)
    publish = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, 'likes')

    def __str__(self):
        return self.text


class Exam(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='exams')
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(auto_now=True)
    finished = models.BooleanField(default=False, blank=True)


class QuestionSet(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    questions = models.ManyToManyField(Question, related_name='questions', blank=True)
    visibility = models.CharField(max_length=1, choices=VIS_CHOICES, default='l')
    is_private = models.BooleanField()
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(CustomUser, related_name='setlikes')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class ExamResults(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    score = models.Count


class Choice(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = RichTextUploadingField(blank=False, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.text


class BlogPostQueryset(models.QuerySet):

    def published(self):
        return self.filter(status='p')

    def draft(self):
        return self.filter(status='d')

    def removed(self):
        return self.filter(status='r')


class BlogPost(BaseModel):
    title = models.CharField(max_length=200)
    visibility = models.CharField(max_length=1, choices=VIS_CHOICES, default='l')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
    thumbnail = models.ImageField('blog thumbnail', upload_to="images/blog", blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = RichTextUploadingField()

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    objects = BlogPostQueryset.as_manager()

    class Meta:
        verbose_name = "blog post"

    def __str__(self):
        return self.title
