from django.db import transaction
from rest_framework import serializers

from core.models import Article, Tag, Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ArticleSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='author.nickname')
    tags = TagSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Article
        fields = [
            'author_nickname',
            'title',
            'excerpt',
            'source_url',
            'image_main',
            'slug',
            'content',
            'tags',
            'categories',
        ]


class ArticleCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Article
        fields = [
            'author',
            'title',
            'excerpt',
            'source_url',
            'image_main',
            'content',
            'tags',
            'categories',
        ]
        extra_kwargs = {'author': {'read_only': True}}

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        categories_data = validated_data.pop('categories', [])

        with transaction.atomic():
            article = Article.objects.create(**validated_data)

            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(**tag_data)
                article.tags.add(tag)

            for category_data in categories_data:
                category, _ = Category.objects.get_or_create(**category_data)
                article.categories.add(category)

        return article

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        categories_data = validated_data.pop('categories', None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if tags_data is not None:
                instance.tags.clear()
                for tag_data in tags_data:
                    tag = Tag.objects.get_or_create(**tag_data)
                    instance.tags.add(tag)

            if categories_data is not None:
                instance.categories.clear()
                for category_data in categories_data:
                    category = Category.objects.get_or_create(**category_data)
                    instance.categories.add(category)

        return instance
