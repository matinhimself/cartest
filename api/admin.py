from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.db.models import Count
from django.forms import BaseInlineFormSet
from django.template.defaultfilters import truncatechars, escape_filter, striptags, truncatewords
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.models.fields import ArrayField

from .models import Question, Category, BlogPost, Choice, QuestionSet

admin.site.site_header = 'Cartest'
admin.site.site_title = 'Admin panel'


@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    ordering = ('-created_at', 'status')
    list_display = ('title', 'created_at', 'status', 'visibility')
    list_filter = ('status', 'visibility')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'questions_count')

    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        return qs.annotate(count=Count('tags'))

    def questions_count(self, inst):
        return inst.count


class MyWidget(ArrayField):
    def __init__(self, *args, **kwargs):
        kwargs['subwidget_form'] = CKEditorUploadingWidget
        super().__init__(*args, **kwargs)


@admin.register(QuestionSet)
class QSetAdmin(admin.ModelAdmin):
    def questions_count(self, obj):
        return obj.questions.all().count()

    def like_count(self, obj):
        return obj.likes.all().count()

    questions_count.short_description = "Questions"
    list_display = ('name', 'is_private', 'visibility', 'author', 'questions_count', 'like_count')
    list_filter = ('is_private',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = ['image', 'text']
    extra = 4


class ChildInlineFormSet(BaseInlineFormSet):

    def get_queryset(self):
        qs = super(ChildInlineFormSet, self).get_queryset()
        return qs.filter(questionset__is_private=False)


class ExamInline(admin.StackedInline):
    model = QuestionSet.questions.through
    extra = 1
    formset = ChildInlineFormSet

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(db_field.name)
        if db_field.name == "questionset":
            kwargs["queryset"] = QuestionSet.objects.filter(is_private=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin, DynamicArrayMixin):
    @admin.action(description='Make Public')
    def make_public(self, _, queryset):
        queryset.update(visibility='p')

    @admin.action(description='Make Limited')
    def make_limited(self, _, queryset):
        queryset.update(visibility='l')

    def like_count(self, obj):
        return obj.likes.all().count()

    exclude = ('likes',)
    like_count.short_description = "likes"
    list_display = ('id', 'visibility', 'get_tags', 'get_sets', 'like_count', 'text_shortener')
    list_filter = ('visibility', 'tags')
    search_fields = ('text',)
    filter_horizontal = ('tags',)
    ordering = ['id', 'visibility', 'publish']
    inlines = [ChoiceInline, ExamInline]
    actions = ('make_public', 'make_limited')

    def text_shortener(self, obj):
        return truncatewords(striptags(obj.text), 5)

    def get_tags(self, obj):
        return truncatechars(",".join([q.title for q in obj.tags.all()[:5]]), 35)

    def get_sets(self, obj):
        return truncatechars(",".join([q.title for q in obj.tags.all()[:5]]), 35)

    text_shortener.short_description = "text"
    get_tags.short_description = "Tags"
    get_sets.short_description = "Sets"

    class Meta:
        model = Question

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(db_field.name)
        if db_field.name == "api_choice":
            kwargs["queryset"] = []
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
