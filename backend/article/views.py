from rest_framework import viewsets, filters

from article.permissions import IsAdminUserOrReadOnly
from article.models import Article, Category, Tag, Avatar
from article.serializers import (
    ArticleSerializer,
    CategorySerializer,
    CategoryDetailSerializer,
    TagSerializer,
    ArticleDetailSerializer,
    AvatarSerializer,
)


class AvatarViewSet(viewsets.ModelViewSet):
    """
    文章标题图视图集
    """
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    """
    标签视图集
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None


class CategoryViewSet(viewsets.ModelViewSet):
    """
    分类视图集
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    文章视图集
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer
    