from django.contrib import admin
from .models import Post,Comment, Category
import datetime


def make_published(modeladmin, request, queryset):
    queryset.update(Status='P')


make_published.short_description = "منتشر کردن پستهای انتخاب شده"


def make_draft(modeladmin, request, queryset):
    queryset.update(Status='D')


make_draft.short_description = "پیشنویس کردن پست های انتخاب شده"


def do_duplicate(modeladmin, request, queryset):
    object: Post
    for object in queryset:
        object.Tags.add("red", "green", "delicious")
        object.id = None
        object.PublishTime = datetime.datetime.now()
        object.Slug+='(dup)'
        object.save()
do_duplicate.short_description = "تکثیر پست های انتخاب شده"


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Author',
                    'Slug', 'PublishTime',
                    'Status','Image')
    list_filter = (
        'Author', 'Tags',
        'Status','Categories'
    )
    prepopulated_fields = {"Slug": ("Title",)}
    date_hierarchy = 'PublishTime'
    actions = [ make_draft,
                make_published,
                do_duplicate]


admin.site.register([Comment,Category])
