from django.db.models import Q
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from article.serializers import ArticleSerializer, ArticleCreateSerializer, TagSerializer, CategorySerializer
from core.models import Article, Tag, Category


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author')
    serializer_class = ArticleSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Article.objects.all()

        return Article.objects.filter(
            Q(is_public=True) | Q(author=user)
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateSerializer
        return super().get_serializer_class()


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
