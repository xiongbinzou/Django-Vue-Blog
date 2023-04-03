from rest_framework import serializers
from article.models import Article, Category, Tag, Avatar
from user_info.serializers import UserDescSerializer
from comment.serializers import CommentSerializer


class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """
    标签序列化器
    """
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    分类序列化器
    """
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    """
    文章序列化器父类
    """
    id = serializers.IntegerField(read_only=True)
    author = UserDescSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), many=True, required=False, slug_field='text')
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    
    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exits.',
        'incorrect_category_id': 'Category with id {value} not exits.',
        'default': 'No more message here...'
    }

    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message, None):
            message = 'default'
        
        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    def validate_category_id(self, value):
        self.check_obj_exists_or_fail(model=Category, value=value, message='incorrect_category_id')
        return value
    
    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(model=Avatar, value=value, message='incorrect_avatar_id')
        return value
    
    def to_internal_value(self, data):
        tags_data = data.get('tags')
        
        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        validated_data['category'] = Category.objects.get(id=category_id)
        tags = Tag.objects.filter(text__in=validated_data['tags'])
        validated_data.pop('tags')
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article


class ArticleSerializer(ArticleBaseSerializer):
    """
    文章列表序列化器
    """

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'body': {'write_only': True}}


class ArticleDetailSerializer(ArticleBaseSerializer):
    """
    文章详情序列化器
    """
    id = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    body_html = serializers.SerializerMethodField()
    toc_html = serializers.SerializerMethodField()

    def get_body_html(self, obj):
        return obj.get_md()[0]
    
    def get_toc_html(self, obj):
        return obj.get_md()[1]
    
    class Meta:
        model = Article
        fields = '__all__'


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """
    给分类详情的文章嵌套序列化器
    """
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Category
        fields = [
            'url',
            'title',
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    分类详情
    """
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles',
        ]