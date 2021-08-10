from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.db.models import Count
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.models.fields import ArrayField

from .models import  Question, Category, BlogPost, Choice

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


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    # pass

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = ['image', 'text']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('id', 'visibility', 'get_tags', 'votes', 'text', 'answer')
    list_filter = ('visibility', 'tags')
    search_fields = ('text',)
    filter_horizontal = ('tags',)
    ordering = ['id', 'visibility', 'publish']
    inlines = [ChoiceInline]

    def get_tags(self, obj):
        """Tags"""
        return ", ".join([q.title for q in obj.tags.all()])

    get_tags.short_description = "Tags"

    class Meta:
        model = Question

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "api_choice":
            kwargs["queryset"] = []
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
