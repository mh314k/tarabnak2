from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from tinymce.models import HTMLField
from django.urls import reverse

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.Author.id, filename)

class Category(models.Model):
    Name = models.CharField(
        max_length=200,
        verbose_name="نام دسته"
    )
    Slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='نشانک دسته'
    )
    Parent = models.ForeignKey(
        'self',
        related_name='CHILDS',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='دسته والد'
    )
    class Meta:
        verbose_name = "دسته"
        verbose_name_plural = 'دسته ها'
        ordering = ['Name','id']

    def get_absolute_url(self):
        return reverse(
            "blog:categories",
            kwargs={
                'slug': str(self.Slug)
        })

    def __str__(self):
        if self.Parent == None:
            return "{} ".format(self.Name)
        else:
            return "{} --> {} ".format(self.Parent.__str__(),
                                  self.Name)


class Post(models.Model):
    stsChoice = (
        ('P', 'منتشر شده'),
        ('D', 'پیشنویس'),
    )
    Title = models.CharField(
        max_length=200,
        verbose_name='عنوان پست'
    )
    Slug = models.SlugField(
        unique_for_date="PublishTime",
        verbose_name='نشانک پست'
    )
    Body = HTMLField(
        verbose_name='متن پست'
    )
    Author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Posts',
        verbose_name='نویسنده پست',
        null=True
    )
    PublishTime = models.DateTimeField(
        verbose_name='تاریخ انتشار'
    )
    CreateTime = models.DateTimeField(
        auto_now_add=True
    )
    LastEditTime = models.DateTimeField(
        auto_now=True
    )
    Status = models.CharField(
        max_length=1,
        choices=stsChoice,
        verbose_name='وضعیت انتشار',
        default='d'
    )
    Tags = TaggableManager(
        verbose_name='برچسب های پست',
        help_text='تگ ها را با علامت کاما جدا کنید.',
        blank=True
    )
    Image = models.ImageField(
        verbose_name='تصویر پست',
        upload_to=user_directory_path,
        null=True,
        blank=True
    )
    Categories = models.ManyToManyField(
        Category,
        related_name='POSTS',
        blank=True,
        verbose_name='دسته ها'
    )

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = 'پست ها'
        ordering = ['-PublishTime']

    def get_absolute_url(self):
        return reverse(
            "blog:post",
            kwargs={
                "year": int(self.PublishTime.year),
                "month": int(self.PublishTime.month),
                "day": int(self.PublishTime.day),
                'slug': str(self.Slug)
        })


    def __str__(self):
        return "{} نوشته شده توسط {} {}({})".format(self.Title, self.Author.first_name, self.Author.last_name,
                                                    self.Author.username)





class Comment(models.Model):
    acptChoices = (('A', 'تایید شده'),
                   ('N', 'تایید نشده'),
                   ('D', 'رد شده'))
    CommentStatus = models.CharField(
        max_length=1,
        verbose_name='وضعیت نظر',
        choices=acptChoices,
        default='N'
    )
    PostTo = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='COMMENTS',
        verbose_name='پست مورد نظر',
        null=True,
        blank=True
    )
    CommentTo = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='REPLIES',
        null=True,
        blank=True
    )
    CommenterUser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='کاربر نظردهنده',
        null=True,
        blank=True
    )
    CommenterName = models.CharField(
        max_length=200,
        verbose_name='نام نظردهنده',
        default='کاربر ناشناس'
    )
    CommentBody = models.TextField(
        max_length=1000,
        verbose_name='متن نظر',
        blank=False
    )
    CommentTime = models.DateTimeField(
        verbose_name='زمان نظر دادن',
        auto_created=True
    )

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = 'نظرها'
        ordering = ['-CommentTime']

    def __str__(self):
        return "نظر توسط {} برای {}".format(self.CommenterName, self.PostTo.Title)


