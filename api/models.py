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


# class UserModel(AbstractUser):
#     last_subscription = models.DateTimeField(default=None, blank=True, null=True)
#     duration_subscription = models.DurationField(default=datetime.timedelta(days=0))
#
#     def is_subscribed(self):
#         if self.is_superuser or self.is_staff:
#             return True
#         if bool(
#                 self.last_subscription and self.duration_subscription and
#                 (self.last_subscription + self.duration_subscription < timezone.now())
#         ):
#             return True
#         return False


class Question(BaseModel):
    visibility = models.CharField(max_length=1, choices=VIS_CHOICES, default='l')
    text = RichTextUploadingField()

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

    votes = models.PositiveSmallIntegerField(default=0)
    answer = models.PositiveSmallIntegerField(default=0, blank=True)

    publish = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('votes',)

    def __str__(self):
        return self.text


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
