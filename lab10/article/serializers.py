import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Article, Painters


# class ArticleModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    photo = serializers.ImageField(read_only=True)
    time_create = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    style_id = serializers.IntegerField()
    painter_id = serializers.IntegerField()
    slug = serializers.SlugField()

    def create(self, validated_data):
        article = Article.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            style_id=validated_data['style_id'],
            painter_id=validated_data['painter_id'],
            slug=validated_data['slug']
        )
        return article

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.photo = validated_data.get("photo", instance.photo)
        instance.time_create = validated_data.get("time_create", instance.time_create)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.style_id = validated_data.get("style_id", instance.style_id)
        instance.painter_id = validated_data.get("painter_id", instance.painter_id)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.save()
        return instance


# def encode():
#     model = ArticleModel('Zvezd', 'Content: qwerty')
#     model_sr = ArticleSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Zvezd","content":"Content: qwerty"}')
#     data = JSONParser().parse(stream)
#     serializer = ArticleSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)


class PainterSerializer(serializers.Serializer):
    painter_name = serializers.CharField(max_length=255)
    painter_content = serializers.CharField()
    painter_photo = serializers.ImageField(read_only=True)
    slug = serializers.SlugField()

    def create(self, validated_data):
        painter = Painters.objects.create(
            painter_name=validated_data['painter_name'],
            painter_content=validated_data['painter_content'],
            slug=validated_data['slug']
        )
        return painter

    def update(self, instance, validated_data):
        instance.painter_name = validated_data.get("painter_name", instance.painter_name)
        instance.painter_content = validated_data.get("painter_content", instance.painter_content)
        instance.painter_photo = validated_data.get("painter_photo", instance.painter_photo)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.save()
        return instance

