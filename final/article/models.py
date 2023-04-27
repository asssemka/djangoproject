from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from mysite import settings


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photo/%Y/%m/%d")
    time_create = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    style = models.ForeignKey("Styles", on_delete=models.PROTECT)
    painter = models.ForeignKey("Painters", on_delete=models.PROTECT)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)


def __str__(self):
    return self.title


class Styles(models.Model):
    style_name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.style_name

    def get_absolute_url(self):
        return reverse('style', kwargs={'style_slug': self.slug})


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="photos/avatars/%Y/%m/%d/")
    # role = models.ForeignKey("Roles", on_delete=models.PROTECT)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user', kwargs={'username': self.username})




class Roles(models.Model):
    role_name = models.CharField(max_length=30, db_index=True)


class Comments(models.Model):
    comment_text = models.TextField(db_index=True)
    article = models.ForeignKey("Article", on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    # parent_comment = models.ForeignKey("Comments", on_delete=models.PROTECT)


    def __str__(self):
        return self.comment_text


class Painters(models.Model):
    painter_name = models.TextField(db_index=True)
    painter_content = models.TextField(db_index=True)
    painter_photo = models.ImageField(upload_to="photo/%Y/%m/%d")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.painter_name


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)