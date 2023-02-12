from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photo/%Y/%m/%d")
    time_create = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)



class Styles(models.Model):
    style_name = models.CharField(max_length=255, db_index=True)

class Users(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="photos/avatars/%Y/%m/%d/")
    role = models.ForeignKey("Roles", on_delete=models.PROTECT)

class Roles(models.Model):
    role_name = models.CharField(max_length=30, db_index=True)

class Comments(models.Model):
    comment_text = models.TextField(db_index=True)
    article = models.ForeignKey("Article", on_delete=models.PROTECT)
    user = models.ForeignKey("Users", on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("Comments", on_delete=models.PROTE