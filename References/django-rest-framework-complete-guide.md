# Django REST Framework (DRF) Complete Guide

## Table of Contents
1. [Introduction to DRF](#introduction-to-drf)
2. [Installation & Setup](#installation--setup)
3. [Serializers](#serializers)
4. [Views & ViewSets](#views--viewsets)
5. [Routers & URL Configuration](#routers--url-configuration)
6. [Authentication](#authentication)
7. [Permissions](#permissions)
8. [Throttling](#throttling)
9. [Filtering, Searching & Ordering](#filtering-searching--ordering)
10. [Pagination](#pagination)
11. [Versioning](#versioning)
12. [Content Negotiation](#content-negotiation)
13. [Parsers & Renderers](#parsers--renderers)
14. [Validation](#validation)
15. [Relationships & Nested Serializers](#relationships--nested-serializers)
16. [File Uploads](#file-uploads)
17. [Testing DRF APIs](#testing-drf-apis)
18. [Performance Optimization](#performance-optimization)
19. [Best Practices](#best-practices)
20. [Common Patterns](#common-patterns)
21. [Interview Questions (3 YOE)](#interview-questions-3-years-experience)

---

## Introduction to DRF

### What is Django REST Framework?
- **Powerful toolkit** for building Web APIs in Django
- **Most popular** REST API framework for Django
- Built on top of Django's class-based views
- Provides browsable API for testing
- Extensive authentication and permission support
- Automatic API documentation (with extensions)

### Key Features
- **Serialization** - Convert complex data to JSON/XML
- **Authentication** - Token, JWT, OAuth, Session
- **Permissions** - Fine-grained access control
- **Throttling** - Rate limiting
- **Filtering** - Advanced query filtering
- **Pagination** - Multiple pagination styles
- **Versioning** - API version management
- **Content Negotiation** - Multiple formats (JSON, XML, etc.)
- **Browsable API** - Interactive web interface
- **Validation** - Field and object-level validation
- **ViewSets & Routers** - Automatic URL routing
- **Caching** - Response caching support

### Why Use DRF?
- Rapid API development
- Clean, maintainable code
- Extensive documentation
- Large community support
- Battle-tested (used by Mozilla, Red Hat, Heroku)
- Flexible and customizable
- Production-ready features out of the box

---

## Installation & Setup

### Installation

```bash
# Install DRF
pip install djangorestframework

# Install additional packages (optional but recommended)
pip install markdown  # Markdown support for browsable API
pip install django-filter  # Filtering support
pip install djangorestframework-simplejwt  # JWT authentication
pip install drf-spectacular  # OpenAPI 3.0 schema generation
pip install django-cors-headers  # CORS support
```

### Basic Configuration

```python
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',  # Token authentication
    'django_filters',  # Filtering
    'corsheaders',  # CORS
    
    # Your apps
    'myapp',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this before CommonMiddleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# DRF Settings
REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    # Permissions
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    # Filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Throttling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
    
    # Rendering
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    
    # Parsing
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    
    # Versioning
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    
    # Schema
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # Error handling
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    
    # Date/Time formats
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
}

# CORS Settings (if using CORS)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
]

# Or allow all (development only!)
CORS_ALLOW_ALL_ORIGINS = True  # Don't use in production!
```

### Project Structure

```
project/
├── api/
│   ├── __init__.py
│   ├── serializers.py      # Serializer classes
│   ├── views.py            # API views
│   ├── viewsets.py         # ViewSets
│   ├── urls.py             # API URLs
│   ├── permissions.py      # Custom permissions
│   ├── throttles.py        # Custom throttles
│   ├── pagination.py       # Custom pagination
│   ├── filters.py          # Custom filters
│   └── tests.py            # API tests
├── myapp/
│   ├── models.py
│   └── ...
└── manage.py
```

---

## Serializers

Serializers convert complex data types (Django models, querysets) to Python data types that can be rendered into JSON, XML, etc.

### Basic Serializer

```python
# serializers.py
from rest_framework import serializers
from myapp.models import Post, Author, Category, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    """Manual serializer (not recommended for models)"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
```

### ModelSerializer (Recommended)

```python
class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'post_count']
        read_only_fields = ['id']
    
    def get_post_count(self, obj):
        """Calculate post count"""
        return obj.posts.filter(status='published').count()


class AuthorSerializer(serializers.ModelSerializer):
    """Author serializer"""
    full_name = serializers.SerializerMethodField()
    post_count = serializers.IntegerField(source='posts.count', read_only=True)
    recent_posts = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'full_name', 
                  'post_count', 'recent_posts', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'email': {'write_only': True},  # Don't expose email in responses
        }
    
    def get_full_name(self, obj):
        """Get full name"""
        return obj.name.title()
    
    def get_recent_posts(self, obj):
        """Get 5 most recent posts"""
        posts = obj.posts.filter(status='published').order_by('-created_at')[:5]
        return PostMinimalSerializer(posts, many=True).data


class PostMinimalSerializer(serializers.ModelSerializer):
    """Minimal post serializer (for nested data)"""
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug']


class PostListSerializer(serializers.ModelSerializer):
    """Post list serializer (optimized for list view)"""
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        source='categories',
        write_only=True
    )
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'author_id',
            'categories', 'category_ids', 'status', 'views',
            'excerpt', 'comment_count', 'featured_image',
            'published_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'views', 'created_at', 'updated_at']
    
    def get_excerpt(self, obj):
        """Get content excerpt"""
        return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content


class PostDetailSerializer(serializers.ModelSerializer):
    """Post detail serializer (with full content)"""
    author = AuthorSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    related_posts = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'categories',
            'content', 'status', 'views', 'featured_image',
            'published_date', 'created_at', 'updated_at',
            'comments', 'related_posts'
        ]
        read_only_fields = ['id', 'views', 'created_at', 'updated_at']
    
    def get_comments(self, obj):
        """Get approved comments"""
        comments = obj.comments.filter(is_approved=True).select_related('user')
        return CommentSerializer(comments, many=True).data
    
    def get_related_posts(self, obj):
        """Get related posts by categories"""
        related = Post.objects.filter(
            categories__in=obj.categories.all(),
            status='published'
        ).exclude(id=obj.id).distinct()[:5]
        return PostMinimalSerializer(related, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer"""
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    post_title = serializers.CharField(source='post.title', read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'user', 'user_id',
            'content', 'parent', 'replies', 'created_at', 'is_approved'
        ]
        read_only_fields = ['id', 'created_at', 'is_approved']
    
    def get_replies(self, obj):
        """Get nested replies"""
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating posts"""
    
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'content', 'categories',
            'status', 'featured_image', 'published_date'
        ]
    
    def validate_slug(self, value):
        """Validate slug uniqueness"""
        if self.instance:
            # Update: exclude current instance
            if Post.objects.filter(slug=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This slug is already in use.")
        else:
            # Create: check if exists
            if Post.objects.filter(slug=value).exists():
                raise serializers.ValidationError("This slug is already in use.")
        return value
    
    def validate_title(self, value):
        """Validate title"""
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        if data.get('status') == 'published' and not data.get('published_date'):
            raise serializers.ValidationError({
                'published_date': 'Published date is required for published posts.'
            })
        return data
```

### Serializer Fields

```python
# Common field types
class ExampleSerializer(serializers.Serializer):
    # Basic fields
    char_field = serializers.CharField(max_length=100)
    email_field = serializers.EmailField()
    integer_field = serializers.IntegerField()
    float_field = serializers.FloatField()
    decimal_field = serializers.DecimalField(max_digits=10, decimal_places=2)
    boolean_field = serializers.BooleanField()
    datetime_field = serializers.DateTimeField()
    date_field = serializers.DateField()
    time_field = serializers.TimeField()
    url_field = serializers.URLField()
    uuid_field = serializers.UUIDField()
    json_field = serializers.JSONField()
    
    # Choice field
    status = serializers.ChoiceField(choices=['draft', 'published'])
    
    # File fields
    file_field = serializers.FileField()
    image_field = serializers.ImageField()
    
    # Relationship fields
    foreign_key = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    many_to_many = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )
    
    # String representation
    author_name = serializers.StringRelatedField()
    
    # Hyperlink
    url = serializers.HyperlinkedIdentityField(view_name='post-detail')
    author_url = serializers.HyperlinkedRelatedField(
        view_name='author-detail',
        read_only=True
    )
    
    # Slug field
    slug_field = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    
    # Method field (custom logic)
    custom_field = serializers.SerializerMethodField()
    
    def get_custom_field(self, obj):
        return "Custom value"
    
    # Read-only field
    read_only = serializers.CharField(read_only=True)
    
    # Write-only field
    write_only = serializers.CharField(write_only=True)
    
    # Field with validators
    validated_field = serializers.CharField(
        validators=[validators.MaxLengthValidator(100)]
    )
```

### Field Options

```python
field = serializers.CharField(
    max_length=100,           # Maximum length
    min_length=5,             # Minimum length
    allow_blank=False,        # Allow empty strings
    allow_null=False,         # Allow None
    required=True,            # Required in input
    default='default',        # Default value
    initial='initial',        # Initial form value
    source='model_field',     # Source field name
    read_only=False,          # Read-only field
    write_only=False,         # Write-only field
    label='Field Label',      # Human-readable label
    help_text='Help text',    # Help text
    style={'input_type': 'password'},  # Widget style
    error_messages={'required': 'Custom error'},  # Custom errors
    validators=[custom_validator],  # Custom validators
    allow_empty=True,         # For lists
    child=serializers.IntegerField(),  # For lists
)
```

---

## Views & ViewSets

### Function-Based Views (with @api_view)

```python
# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer

@api_view(['GET', 'POST'])
def post_list(request):
    """
    List all posts or create a new post.
    GET /api/posts/
    POST /api/posts/
    """
    if request.method == 'GET':
        posts = Post.objects.filter(status='published').select_related('author')
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user.author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    """
    Retrieve, update or delete a post.
    GET /api/posts/1/
    PUT /api/posts/1/
    PATCH /api/posts/1/
    DELETE /api/posts/1/
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        # Check if user owns the post
        if post.author.user != request.user:
            return Response(
                {'error': 'You do not have permission to edit this post'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        partial = request.method == 'PATCH'
        serializer = PostCreateUpdateSerializer(post, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if post.author.user != request.user:
            return Response(
                {'error': 'You do not have permission to delete this post'},
                status=status.HTTP_403_FORBIDDEN
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### Class-Based Views (APIView)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PostListAPIView(APIView):
    """
    List all posts or create a new post.
    """
    
    def get(self, request, format=None):
        """List all posts"""
        posts = Post.objects.filter(status='published').select_related('author')
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """Create a new post"""
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user.author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    """
    Retrieve, update or delete a post.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        """Get post object"""
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None
    
    def get(self, request, pk, format=None):
        """Retrieve a post"""
        post = self.get_object(pk)
        if post is None:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """Update a post"""
        post = self.get_object(pk)
        if post is None:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if post.author.user != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PostCreateUpdateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """Delete a post"""
        post = self.get_object(pk)
        if post is None:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if post.author.user != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### Generic Views

```python
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostListCreateView(generics.ListCreateAPIView):
    """List posts or create new post"""
    queryset = Post.objects.filter(status='published').select_related('author')
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """Set author when creating"""
        serializer.save(author=self.request.user.author)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete post"""
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """Use different serializer for update"""
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer


# Other generic views:
# - ListAPIView (read-only list)
# - CreateAPIView (create only)
# - RetrieveAPIView (read-only single)
# - UpdateAPIView (update only)
# - DestroyAPIView (delete only)
# - RetrieveUpdateAPIView (read and update)
```

### ViewSets (Most Powerful)

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model.
    Provides: list, create, retrieve, update, partial_update, destroy
    """
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'author', 'categories']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Customize queryset based on action"""
        queryset = super().get_queryset()
        
        if self.action == 'list':
            # Optimize for list view
            queryset = queryset.select_related('author').prefetch_related('categories')
        elif self.action == 'retrieve':
            # Optimize for detail view
            queryset = queryset.select_related('author').prefetch_related(
                'categories', 'comments__user'
            )
        
        # Filter by authenticated user's posts
        if self.action in ['update', 'partial_update', 'destroy']:
            if not self.request.user.is_staff:
                queryset = queryset.filter(author__user=self.request.user)
        
        return queryset
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def perform_create(self, serializer):
        """Set author when creating post"""
        serializer.save(author=self.request.user.author)
    
    def perform_update(self, serializer):
        """Custom logic when updating"""
        serializer.save()
    
    def perform_destroy(self, instance):
        """Custom logic when deleting"""
        # Soft delete instead of hard delete
        instance.status = 'deleted'
        instance.save()
    
    # Custom actions
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Custom action to publish a post.
        POST /api/posts/{id}/publish/
        """
        post = self.get_object()
        if post.author.user != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.status = 'published'
        post.published_date = timezone.now()
        post.save()
        
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """
        Unpublish a post.
        POST /api/posts/{id}/unpublish/
        """
        post = self.get_object()
        if post.author.user != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.status = 'draft'
        post.save()
        
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured posts (collection action).
        GET /api/posts/featured/
        """
        posts = self.get_queryset().filter(
            status='published',
            views__gte=100
        ).order_by('-views')[:10]
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """
        Get current user's posts.
        GET /api/posts/my_posts/
        """
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        posts = self.get_queryset().filter(author__user=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get comments for a post.
        GET /api/posts/{id}/comments/
        """
        post = self.get_object()
        comments = post.comments.filter(is_approved=True).select_related('user')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly ViewSet for categories.
    Provides only: list, retrieve
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for comments"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter by post if provided"""
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset.filter(is_approved=True).select_related('user', 'post')
    
    def perform_create(self, serializer):
        """Set user when creating comment"""
        serializer.save(user=self.request.user)
```

---

## Routers & URL Configuration

### Automatic URL Routing

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .viewsets import PostViewSet, CategoryViewSet, CommentViewSet

# Create router
router = DefaultRouter()  # Includes API root view
# or
# router = SimpleRouter()  # No API root view

# Register viewsets
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'comments', CommentViewSet, basename='comment')

# URLs generated by router:
# GET    /api/posts/                  -> list
# POST   /api/posts/                  -> create
# GET    /api/posts/{id}/             -> retrieve
# PUT    /api/posts/{id}/             -> update
# PATCH  /api/posts/{id}/             -> partial_update
# DELETE /api/posts/{id}/             -> destroy
# GET    /api/posts/featured/         -> custom action (list)
# POST   /api/posts/{id}/publish/     -> custom action (detail)

urlpatterns = [
    path('api/', include(router.urls)),
]

# Or with namespace
app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
```

### Manual URL Configuration

```python
# urls.py
from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    PostListAPIView,
    PostDetailAPIView,
)

urlpatterns = [
    # Generic views
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # APIView
    path('posts-api/', PostListAPIView.as_view(), name='post-list-api'),
    path('posts-api/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail-api'),
    
    # Function-based views
    path('posts-fbv/', post_list, name='post-list-fbv'),
    path('posts-fbv/<int:pk>/', post_detail, name='post-detail-fbv'),
]
```

### Nested Routers

```python
# Install: pip install drf-nested-routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

posts_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

# URLs generated:
# /api/posts/{post_pk}/comments/
# /api/posts/{post_pk}/comments/{id}/

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(posts_router.urls)),
]
```

---

## Authentication

### Token Authentication

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Run migration
# python manage.py migrate

# Generate tokens
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create token for user
user = User.objects.get(username='john')
token = Token.objects.create(user=user)
print(token.key)  # 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# Or get or create
token, created = Token.objects.get_or_create(user=user)

# Login view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/login/', obtain_auth_token, name='api-login'),
]

# Custom login view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_400_BAD_REQUEST
    )

# Use token in API requests
# Header: Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### JWT Authentication (Recommended)

```python
# Install
# pip install djangorestframework-simplejwt

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Custom JWT claims
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Use in API requests
# Header: Authorization: Bearer <access_token>
```

### Session Authentication

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Useful for browsable API and same-origin requests
# Uses Django's session framework
# CSRF token required for unsafe methods (POST, PUT, DELETE)
```

### OAuth2 Authentication

```python
# Install: pip install django-oauth-toolkit
# Install: pip install djangorestframework-oauth

# settings.py
INSTALLED_APPS = [
    'oauth2_provider',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
}

# Configure OAuth2 provider
# See django-oauth-toolkit documentation for detailed setup
```

### Custom Authentication

```python
# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class CustomAuthentication(BaseAuthentication):
    """Custom authentication using API key"""
    
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return None  # No authentication attempted
        
        try:
            user = User.objects.get(profile__api_key=api_key)
            return (user, None)  # (user, auth)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
    
    def authenticate_header(self, request):
        """Return authentication header for 401 responses"""
        return 'X-API-Key'

# Use in views
from rest_framework.permissions import IsAuthenticated

class MyView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Authenticated!'})
```

---

## Permissions

### Built-in Permissions

```python
from rest_framework.permissions import (
    AllowAny,               # Allow anyone (authenticated or not)
    IsAuthenticated,        # Require authentication
    IsAdminUser,            # Require admin/staff user
    IsAuthenticatedOrReadOnly,  # Read for all, write for authenticated
    DjangoModelPermissions,     # Use Django's model permissions
    DjangoObjectPermissions,    # Use Django's object-level permissions
)

# Usage in views
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Or per-action
from rest_framework.decorators import action

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:  # update, partial_update, destroy
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
```

### Custom Permissions

```python
# permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: object owner can edit, others can only read.
    """
    
    def has_permission(self, request, view):
        """View-level permission check"""
        # Allow GET, HEAD, OPTIONS (safe methods) to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require authentication
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Object-level permission check"""
        # Read permissions allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        return obj.author.user == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Only post author can edit"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Only admin can edit"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CanPublishPost(permissions.BasePermission):
    """Check if user has permission to publish posts"""
    
    def has_permission(self, request, view):
        return request.user.has_perm('myapp.can_publish')


class IsStaffOrOwner(permissions.BasePermission):
    """Staff can access all, users can only access their own"""
    
    def has_object_permission(self, request, view, obj):
        # Staff can do anything
        if request.user.is_staff:
            return True
        
        # Regular users can only access their own objects
        return obj.author.user == request.user


# Usage
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]


# Combining multiple permissions (all must pass)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
```

### Permission Shortcuts

```python
# Check permission in view logic
from rest_framework.exceptions import PermissionDenied

class PostViewSet(viewsets.ModelViewSet):
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        
        # Check permission manually
        if not request.user.has_perm('myapp.can_publish'):
            raise PermissionDenied('You cannot publish posts')
        
        post.status = 'published'
        post.save()
        return Response({'status': 'post published'})
```

---

## Throttling

### Built-in Throttle Classes

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  # Anonymous users
        'rest_framework.throttling.UserRateThrottle',  # Authenticated users
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',      # 100 requests per day for anonymous
        'user': '1000/day',     # 1000 requests per day for authenticated
    }
}

# Rate format: {number}/{period}
# Periods: second, minute, hour, day
# Examples: '10/second', '100/minute', '1000/hour', '5000/day'

# Per-view throttling
from rest_framework.throttling import UserRateThrottle

class PostViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'posts'  # Custom scope

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'posts': '50/hour',  # Custom scope
    }
}
```

### Custom Throttle Classes

```python
# throttles.py
from rest_framework.throttling import SimpleRateThrottle

class BurstRateThrottle(SimpleRateThrottle):
    """Burst rate throttle: 5 requests per minute"""
    scope = 'burst'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class SustainedRateThrottle(SimpleRateThrottle):
    """Sustained rate throttle: 1000 requests per day"""
    scope = 'sustained'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class PremiumUserRateThrottle(UserRateThrottle):
    """Higher rate limit for premium users"""
    
    def allow_request(self, request, view):
        # Premium users get unlimited access
        if hasattr(request.user, 'profile') and request.user.profile.is_premium:
            return True
        
        return super().allow_request(request, view)


# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'burst': '5/minute',
        'sustained': '1000/day',
    }
}

# Usage
class PostViewSet(viewsets.ModelViewSet):
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
```

---

## Filtering, Searching & Ordering

### Django Filter Backend

```python
# Install: pip install django-filter

# settings.py
INSTALLED_APPS = [
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# Simple filtering
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_fields = ['status', 'author', 'categories']

# URLs:
# /api/posts/?status=published
# /api/posts/?author=1
# /api/posts/?categories=2&categories=3

# Advanced filtering with FilterSet
from django_filters import rest_framework as filters

class PostFilter(filters.FilterSet):
    """Custom filter for posts"""
    title = filters.CharFilter(lookup_expr='icontains')
    min_views = filters.NumberFilter(field_name='views', lookup_expr='gte')
    max_views = filters.NumberFilter(field_name='views', lookup_expr='lte')
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    author_name = filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    
    class Meta:
        model = Post
        fields = {
            'status': ['exact'],
            'views': ['exact', 'gte', 'lte'],
            'created_at': ['exact', 'gte', 'lte'],
        }

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter

# URLs:
# /api/posts/?title__icontains=django
# /api/posts/?min_views=100&max_views=1000
# /api/posts/?created_after=2024-01-01
# /api/posts/?author_name=john
```

### Search Filter

```python
from rest_framework.filters import SearchFilter

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content', 'author__name']

# URL: /api/posts/?search=django
# Searches in title, content, and author name

# Search field prefixes:
# '^' - Starts-with search
# '=' - Exact matches
# '@' - Full-text search (PostgreSQL only)
# '$' - Regex search

search_fields = [
    '^title',           # Title starts with
    '=author__name',    # Author name exact match
    'content',          # Content contains (default)
]
```

### Ordering Filter

```python
from rest_framework.filters import OrderingFilter

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'views', 'title']
    ordering = ['-created_at']  # Default ordering

# URLs:
# /api/posts/?ordering=views
# /api/posts/?ordering=-views (descending)
# /api/posts/?ordering=created_at,views (multiple fields)
```

### Combining Filters

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views']
    ordering = ['-created_at']

# URL: /api/posts/?status=published&search=django&ordering=-views
```

---

## Pagination

### Built-in Pagination Classes

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# 1. PageNumberPagination (default)
# URL: /api/posts/?page=2
# Response:
# {
#     "count": 100,
#     "next": "http://api.example.com/posts/?page=3",
#     "previous": "http://api.example.com/posts/?page=1",
#     "results": [...]
# }

# 2. LimitOffsetPagination
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}
# URL: /api/posts/?limit=10&offset=20

# 3. CursorPagination (best for large datasets)
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 10,
}
# URL: /api/posts/?cursor=cD0yMDIx
```

### Custom Pagination

```python
# pagination.py
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Maximum page size
    page_query_param = 'page'


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100


class CustomCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'  # Must specify ordering
    cursor_query_param = 'cursor'


# Usage in ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination


# Disable pagination for specific view
class NoPaginationViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = None
```

### Custom Response Format

```python
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class CustomPagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total_count', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('page_size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))

# Response:
# {
#     "total_count": 100,
#     "total_pages": 10,
#     "current_page": 2,
#     "page_size": 10,
#     "next": "...",
#     "previous": "...",
#     "data": [...]
# }
```

---

## Versioning

### URL Path Versioning

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}

# urls.py
urlpatterns = [
    path('api/v1/', include('myapp.api.v1.urls')),
    path('api/v2/', include('myapp.api.v2.urls')),
]

# URL: /api/v1/posts/
# URL: /api/v2/posts/
```

### Query Parameter Versioning

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
}

# URL: /api/posts/?version=v1
```

### Header Versioning

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
}

# Header: Accept: application/json; version=v1
```

### Namespace Versioning

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}

# urls.py
urlpatterns = [
    path('v1/', include('myapp.urls', namespace='v1')),
    path('v2/', include('myapp.urls', namespace='v2')),
]
```

### Using Versioning in Views

```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        """Use different serializers for different versions"""
        if self.request.version == 'v1':
            return PostSerializerV1
        elif self.request.version == 'v2':
            return PostSerializerV2
        return PostSerializerV2  # Default to latest
    
    def list(self, request, *args, **kwargs):
        """Custom logic based on version"""
        version = request.version
        
        if version == 'v1':
            # V1 logic
            queryset = self.get_queryset()
        elif version == 'v2':
            # V2 logic with additional filtering
            queryset = self.get_queryset().filter(status='published')
        
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
```

---

## Content Negotiation

### Renderers

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # JSON format
        'rest_framework.renderers.BrowsableAPIRenderer',  # Browsable API
    ],
}

# Additional renderers:
# - XMLRenderer (install: pip install djangorestframework-xml)
# - YAMLRenderer (install: pip install djangorestframework-yaml)
# - JSONPRenderer
# - TemplateHTMLRenderer

# Per-view renderer
from rest_framework.renderers import JSONRenderer, XMLRenderer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [JSONRenderer, XMLRenderer]

# Client specifies format:
# Header: Accept: application/json
# Header: Accept: application/xml
# Or URL: /api/posts/?format=json
```

### Custom Renderer

```python
# renderers.py
from rest_framework.renderers import BaseRenderer
import csv
from io import StringIO

class CSVRenderer(BaseRenderer):
    """Custom CSV renderer"""
    media_type = 'text/csv'
    format = 'csv'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Render data as CSV"""
        if not isinstance(data, list):
            data = [data]
        
        if not data:
            return ''
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        return output.getvalue()

# Usage
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [JSONRenderer, CSVRenderer]

# URL: /api/posts/?format=csv
```

---

## Parsers & Renderers

### Parsers (Request Data)

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # application/json
        'rest_framework.parsers.FormParser',  # application/x-www-form-urlencoded
        'rest_framework.parsers.MultiPartParser',  # multipart/form-data
    ],
}

# Additional parsers:
# - FileUploadParser - Raw file upload
# - XMLParser (install: djangorestframework-xml)
# - YAMLParser (install: djangorestframework-yaml)

# Per-view parser
from rest_framework.parsers import JSONParser, FileUploadParser

class FileUploadView(APIView):
    parser_classes = [FileUploadParser]
    
    def post(self, request, filename):
        file_obj = request.data['file']
        # Process file
        return Response(status=status.HTTP_201_CREATED)
```

### Custom Parser

```python
# parsers.py
from rest_framework.parsers import BaseParser
import yaml

class YAMLParser(BaseParser):
    """Custom YAML parser"""
    media_type = 'application/yaml'
    
    def parse(self, stream, media_type=None, parser_context=None):
        """Parse YAML data"""
        return yaml.safe_load(stream)

# Usage
class PostViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, YAMLParser]
```

---

## Validation

### Field-Level Validation

```python
class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'
    
    def validate_title(self, value):
        """Validate title field"""
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters.")
        
        if 'spam' in value.lower():
            raise serializers.ValidationError("Title contains spam words.")
        
        return value
    
    def validate_slug(self, value):
        """Validate slug uniqueness"""
        if self.instance:
            # Update: exclude current instance
            if Post.objects.filter(slug=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This slug is already taken.")
        else:
            # Create: check if exists
            if Post.objects.filter(slug=value).exists():
                raise serializers.ValidationError("This slug is already taken.")
        
        return value
```

### Object-Level Validation

```python
class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'
    
    def validate(self, data):
        """Cross-field validation"""
        
        # Check if published post has published_date
        if data.get('status') == 'published' and not data.get('published_date'):
            raise serializers.ValidationError({
                'published_date': 'Published posts must have a published date.'
            })
        
        # Check if title and slug match
        if data.get('title') and data.get('slug'):
            expected_slug = slugify(data['title'])
            if data['slug'] != expected_slug:
                raise serializers.ValidationError({
                    'slug': f'Slug should be "{expected_slug}" based on title.'
                })
        
        # Check minimum content length
        if data.get('content') and len(data['content']) < 100:
            raise serializers.ValidationError({
                'content': 'Content must be at least 100 characters.'
            })
        
        return data
```

### Custom Validators

```python
# validators.py
from rest_framework import serializers
import re

def validate_no_special_chars(value):
    """Validate that value contains no special characters"""
    if not re.match(r'^[a-zA-Z0-9\s]+$', value):
        raise serializers.ValidationError(
            'Field can only contain letters, numbers, and spaces.'
        )

def validate_min_words(min_count):
    """Validate minimum word count"""
    def validator(value):
        word_count = len(value.split())
        if word_count < min_count:
            raise serializers.ValidationError(
                f'Must contain at least {min_count} words.'
            )
    return validator

def validate_file_size(max_size_mb):
    """Validate file size"""
    def validator(file):
        max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
        if file.size > max_size:
            raise serializers.ValidationError(
                f'File size cannot exceed {max_size_mb}MB.'
            )
    return validator

# Usage in serializer
class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_no_special_chars])
    content = serializers.CharField(validators=[validate_min_words(50)])
    featured_image = serializers.ImageField(validators=[validate_file_size(5)])
    
    class Meta:
        model = Post
        fields = '__all__'
```

### Validation in Views

```python
class PostViewSet(viewsets.ModelViewSet):
    
    def create(self, request, *args, **kwargs):
        """Custom validation in view"""
        serializer = self.get_serializer(data=request.data)
        
        # Standard validation
        serializer.is_valid(raise_exception=True)
        
        # Additional business logic validation
        if not request.user.has_perm('myapp.can_create_post'):
            return Response(
                {'error': 'You do not have permission to create posts.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check user's post limit
        user_post_count = Post.objects.filter(author__user=request.user).count()
        if user_post_count >= 10:
            return Response(
                {'error': 'You have reached your post limit.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

---

## Relationships & Nested Serializers

### ForeignKey Relationships

```python
# Primary Key (default)
class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author']

# Response: {"id": 1, "title": "...", "author": 1}


# String Representation
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Uses __str__ method
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author']

# Response: {"id": 1, "title": "...", "author": "John Doe"}


# Nested Serializer (Read)
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author']

# Response: {"id": 1, "title": "...", "author": {"id": 1, "name": "John", "email": "..."}}


# Nested with Write Support
class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_id']

# Request: {"title": "...", "author_id": 1}
# Response: {"id": 1, "title": "...", "author": {"id": 1, "name": "..."}}


# Hyperlinked
class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail',
        queryset=Author.objects.all()
    )
    
    class Meta:
        model = Post
        fields = ['url', 'title', 'author']

# Response: {"url": "...", "title": "...", "author": "http://api.../authors/1/"}
```

### ManyToMany Relationships

```python
# Primary Keys
class PostSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'categories']

# Response: {"id": 1, "title": "...", "categories": [1, 2, 3]}


# Nested Serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        source='categories',
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'categories', 'category_ids']

# Request: {"title": "...", "category_ids": [1, 2, 3]}
# Response: {
#     "id": 1,
#     "title": "...",
#     "categories": [
#         {"id": 1, "name": "Python", "slug": "python"},
#         {"id": 2, "name": "Django", "slug": "django"}
#     ]
# }
```

### Reverse Relationships

```python
# Author -> Posts (reverse ForeignKey)
class PostMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug']

class AuthorSerializer(serializers.ModelSerializer):
    posts = PostMinimalSerializer(many=True, read_only=True)
    post_count = serializers.IntegerField(source='posts.count', read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'posts', 'post_count']

# Response: {
#     "id": 1,
#     "name": "John Doe",
#     "email": "...",
#     "post_count": 5,
#     "posts": [
#         {"id": 1, "title": "...", "slug": "..."},
#         {"id": 2, "title": "...", "slug": "..."}
#     ]
# }
```

### Nested Writes

```python
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'comments']
    
    def create(self, validated_data):
        """Handle nested writes"""
        comments_data = validated_data.pop('comments', [])
        post = Post.objects.create(**validated_data)
        
        for comment_data in comments_data:
            Comment.objects.create(post=post, **comment_data)
        
        return post
    
    def update(self, instance, validated_data):
        """Handle nested updates"""
        comments_data = validated_data.pop('comments', [])
        
        # Update post fields
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        
        # Update comments
        instance.comments.all().delete()  # Clear existing
        for comment_data in comments_data:
            Comment.objects.create(post=instance, **comment_data)
        
        return instance
```

---

## File Uploads

### Basic File Upload

```python
# models.py
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# serializers.py
class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'file', 'file_url', 'file_size', 'uploaded_at']
        read_only_fields = ['uploaded_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_file_size(self, obj):
        if obj.file:
            return obj.file.size
        return 0

# views.py
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request, *args, **kwargs):
        """Handle file upload"""
        file_serializer = DocumentSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Image Upload with Validation

```python
# validators.py
from rest_framework import serializers
from PIL import Image

def validate_image_file(image):
    """Validate image file"""
    # Check file size (max 5MB)
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise serializers.ValidationError('Image size cannot exceed 5MB.')
    
    # Check file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise serializers.ValidationError(
            f'Invalid file extension. Allowed: {", ".join(valid_extensions)}'
        )
    
    # Check image dimensions
    try:
        img = Image.open(image)
        width, height = img.size
        if width < 100 or height < 100:
            raise serializers.ValidationError('Image must be at least 100x100 pixels.')
        if width > 4000 or height > 4000:
            raise serializers.ValidationError('Image cannot exceed 4000x4000 pixels.')
    except Exception as e:
        raise serializers.ValidationError('Invalid image file.')

# serializers.py
class PostSerializer(serializers.ModelSerializer):
    featured_image = serializers.ImageField(
        validators=[validate_image_file],
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'featured_image']
```

### Multiple File Upload

```python
# views.py
class MultipleFileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        """Upload multiple files"""
        files = request.FILES.getlist('files')
        
        if not files:
            return Response(
                {'error': 'No files provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_files = []
        for file in files:
            document = Document.objects.create(file=file)
            serializer = DocumentSerializer(document, context={'request': request})
            uploaded_files.append(serializer.data)
        
        return Response(
            {'files': uploaded_files},
            status=status.HTTP_201_CREATED
        )
```

---

## Testing DRF APIs

### Basic API Tests

```python
# tests.py
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Author

class PostAPITestCase(APITestCase):
    """Test Post API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test author
        self.author = Author.objects.create(
            name='Test Author',
            email='test@example.com'
        )
        
        # Create test posts
        self.post1 = Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            content='Test content 1',
            author=self.author,
            status='published'
        )
        
        self.post2 = Post.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            content='Test content 2',
            author=self.author,
            status='draft'
        )
    
    def test_list_posts(self):
        """Test listing posts"""
        url = reverse('post-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_post(self):
        """Test retrieving single post"""
        url = reverse('post-detail', kwargs={'pk': self.post1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post 1')
        self.assertEqual(response.data['slug'], 'test-post-1')
    
    def test_create_post_authenticated(self):
        """Test creating post when authenticated"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'slug': 'new-post',
            'content': 'New content',
            'author_id': self.author.id,
            'status': 'draft'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Post')
    
    def test_create_post_unauthenticated(self):
        """Test creating post when not authenticated"""
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'slug': 'new-post',
            'content': 'New content'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_post(self):
        """Test updating post"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('post-detail', kwargs={'pk': self.post1.pk})
        data = {
            'title': 'Updated Title',
            'slug': 'test-post-1',
            'content': 'Updated content',
            'status': 'published'
        }
        
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Title')
    
    def test_partial_update_post(self):
        """Test partial update (PATCH)"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('post-detail', kwargs={'pk': self.post1.pk})
        data = {'title': 'Partially Updated'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Partially Updated')
        self.assertEqual(self.post1.content, 'Test content 1')  # Unchanged
    
    def test_delete_post(self):
        """Test deleting post"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('post-detail', kwargs={'pk': self.post1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
    
    def test_filter_posts(self):
        """Test filtering posts"""
        url = reverse('post-list')
        response = self.client.get(url, {'status': 'published'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_search_posts(self):
        """Test searching posts"""
        url = reverse('post-list')
        response = self.client.get(url, {'search': 'Post 1'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_pagination(self):
        """Test pagination"""
        # Create more posts
        for i in range(20):
            Post.objects.create(
                title=f'Post {i}',
                slug=f'post-{i}',
                content=f'Content {i}',
                author=self.author,
                status='published'
            )
        
        url = reverse('post-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)


class AuthenticationTestCase(APITestCase):
    """Test authentication"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_obtain_token(self):
        """Test obtaining JWT token"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_invalid_credentials(self):
        """Test with invalid credentials"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test myapp.tests

# Run specific test class
python manage.py test myapp.tests.PostAPITestCase

# Run specific test method
python manage.py test myapp.tests.PostAPITestCase.test_list_posts

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

---

## Performance Optimization

### Query Optimization

```python
class PostViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        """Optimize queries"""
        queryset = Post.objects.all()
        
        # Use select_related for ForeignKey
        queryset = queryset.select_related('author')
        
        # Use prefetch_related for ManyToMany
        queryset = queryset.prefetch_related('categories')
        
        # Only fetch needed fields
        if self.action == 'list':
            queryset = queryset.only(
                'id', 'title', 'slug', 'status', 'created_at'
            )
        
        return queryset
```

### Caching

```python
# View-level caching
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class PostViewSet(viewsets.ModelViewSet):
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# Low-level caching
from django.core.cache import cache

class PostViewSet(viewsets.ModelViewSet):
    
    def list(self, request, *args, **kwargs):
        cache_key = 'post_list'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60 * 15)  # 15 minutes
        
        return response
```

### Pagination for Large Datasets

```python
from rest_framework.pagination import CursorPagination

class PostCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'
    cursor_query_param = 'cursor'

class PostViewSet(viewsets.ModelViewSet):
    pagination_class = PostCursorPagination
```

---

## Best Practices

### 1. Project Structure
```
api/
├── v1/
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── post.py
│   │   ├── author.py
│   │   └── comment.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── post.py
│   │   └── author.py
│   ├── permissions.py
│   ├── pagination.py
│   ├── filters.py
│   └── urls.py
└── v2/
    └── ...
```

### 2. Serializer Best Practices
- Use `ModelSerializer` when possible
- Create separate serializers for list/detail/create/update
- Use `SerializerMethodField` for computed fields
- Implement proper validation (field and object-level)
- Use `read_only_fields` and `write_only` fields appropriately

### 3. View Best Practices
- Use `ViewSets` for CRUD operations
- Override `get_queryset()` for filtering/optimization
- Override `get_serializer_class()` for different serializers per action
- Implement proper permissions
- Use `@action` decorator for custom endpoints

### 4. URL Best Practices
- Use routers for consistent URL patterns
- Version your APIs (v1, v2)
- Use meaningful endpoint names
- Follow REST conventions

### 5. Security Best Practices
- Always use HTTPS in production
- Implement proper authentication (JWT recommended)
- Use permissions appropriately
- Implement throttling to prevent abuse
- Validate all user input
- Use CORS headers correctly
- Never expose sensitive data in responses

### 6. Performance Best Practices
- Use `select_related` and `prefetch_related`
- Implement pagination
- Use caching where appropriate
- Only return necessary fields
- Use database indexes
- Monitor query performance

---

## Common Patterns

### Pattern 1: Read-Only API

```python
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
```

### Pattern 2: Custom Actions

```python
class PostViewSet(viewsets.ModelViewSet):
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Like a post"""
        post = self.get_object()
        post.likes.add(request.user)
        return Response({'status': 'post liked'})
    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Unlike a post"""
        post = self.get_object()
        post.likes.remove(request.user)
        return Response({'status': 'post unliked'})
```

### Pattern 3: Bulk Operations

```python
class PostViewSet(viewsets.ModelViewSet):
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple posts"""
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Update multiple posts"""
        posts = []
        for item in request.data:
            post = Post.objects.get(id=item['id'])
            serializer = self.get_serializer(post, data=item, partial=True)
            serializer.is_valid(raise_exception=True)
            posts.append(serializer.save())
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
```

---

## Interview Questions (3 Years Experience)

### Q1: What is Django REST Framework and why use it?
**Answer:** Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django. It provides:
- **Serialization** - Convert complex data to JSON/XML and vice versa
- **Authentication & Permissions** - Built-in support for various auth methods
- **Browsable API** - Interactive web interface for testing
- **ViewSets & Routers** - Automatic URL routing and CRUD operations
- **Validation** - Comprehensive field and object-level validation
- **Throttling** - Rate limiting to prevent abuse
- **Pagination** - Multiple pagination styles
- **Content Negotiation** - Support multiple formats (JSON, XML, etc.)

Why use it:
- Rapid API development
- Clean, maintainable code
- Production-ready features
- Extensive documentation
- Large community support
- Used by major companies (Mozilla, Red Hat, etc.)

### Q2: Explain the difference between Serializer and ModelSerializer.
**Answer:**

**Serializer:**
- Manual field definition
- Full control over serialization
- More verbose
- Use when not working with Django models

```python
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
```

**ModelSerializer:**
- Automatically generates fields from model
- Less code, more DRY
- Automatic create/update methods
- Recommended for Django models

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']
```

### Q3: What are ViewSets and how do they differ from APIView?
**Answer:**

**APIView:**
- Most basic, full control
- Define each HTTP method explicitly
- Manual URL configuration
- Good for non-CRUD operations

```python
class PostListAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

**ViewSet:**
- Combines logic for related actions
- Automatic CRUD operations
- Works with routers for automatic URL configuration
- Less code, more DRY

```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Automatically provides: list, create, retrieve, update, partial_update, destroy
```

**Hierarchy:**
1. `APIView` - Most basic, full control
2. Generic Views (`ListAPIView`, `CreateAPIView`, etc.) - Pre-built for common patterns
3. `ViewSet` - Combines related actions
4. `ModelViewSet` - Full CRUD for models

### Q4: How do you implement authentication in DRF?
**Answer:**

**1. Token Authentication:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Generate token
from rest_framework.authtoken.models import Token
token = Token.objects.create(user=user)

# Use in request
# Header: Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**2. JWT Authentication (Recommended):**
```python
# Install: pip install djangorestframework-simplejwt

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# URLs
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]

# Use in request
# Header: Authorization: Bearer <access_token>
```

**3. Session Authentication:**
- Uses Django's session framework
- Good for same-origin requests
- CSRF token required for unsafe methods

**4. Custom Authentication:**
```python
from rest_framework.authentication import BaseAuthentication

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        # Validate api_key and return (user, auth)
        return (user, None)
```

### Q5: Explain select_related vs prefetch_related in context of DRF.
**Answer:**

Both optimize database queries, but work differently:

**select_related (for ForeignKey, OneToOne):**
- Uses SQL JOIN
- Single database query
- More efficient for single relationships

```python
class PostViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Without select_related: 2 queries (1 for posts, N for authors)
        # With select_related: 1 query with JOIN
        return Post.objects.select_related('author')

# SQL: SELECT * FROM posts JOIN authors ON posts.author_id = authors.id
```

**prefetch_related (for ManyToMany, reverse ForeignKey):**
- Uses separate queries
- Joins data in Python
- Better for many-to-many relationships

```python
class PostViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Without prefetch_related: 1 + N queries (1 for posts, N for categories per post)
        # With prefetch_related: 2 queries (1 for posts, 1 for all categories)
        return Post.objects.prefetch_related('categories')

# SQL: 
# Query 1: SELECT * FROM posts
# Query 2: SELECT * FROM categories WHERE post_id IN (1, 2, 3, ...)
```

**Combined:**
```python
Post.objects.select_related('author').prefetch_related('categories', 'comments')
```

### Q6: How do you handle validation in DRF?
**Answer:**

**1. Field-Level Validation:**
```python
class PostSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title too short")
        return value
```

**2. Object-Level Validation:**
```python
class PostSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['status'] == 'published' and not data.get('published_date'):
            raise serializers.ValidationError({
                'published_date': 'Required for published posts'
            })
        return data
```

**3. Custom Validators:**
```python
def validate_no_spam(value):
    if 'spam' in value.lower():
        raise serializers.ValidationError('Contains spam')

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_no_spam])
```

**4. Validation in Views:**
```python
def create(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # Additional business logic validation
    if condition:
        return Response({'error': 'Custom error'}, status=400)
    self.perform_create(serializer)
    return Response(serializer.data, status=201)
```

### Q7: What is throttling and how do you implement it?
**Answer:** Throttling controls the rate of requests to prevent abuse.

**Built-in Throttle Classes:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    }
}
```

**Per-View Throttling:**
```python
class PostViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'posts'
```

**Custom Throttle:**
```python
from rest_framework.throttling import SimpleRateThrottle

class BurstRateThrottle(SimpleRateThrottle):
    scope = 'burst'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {'scope': self.scope, 'ident': ident}

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'burst': '10/minute',
    }
}
```

### Q8: How do you implement pagination in DRF?
**Answer:**

**1. PageNumberPagination:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# URL: /api/posts/?page=2
```

**2. LimitOffsetPagination:**
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

# URL: /api/posts/?limit=10&offset=20
```

**3. CursorPagination (best for large datasets):**
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 10,
}

# URL: /api/posts/?cursor=cD0yMDIx
```

**4. Custom Pagination:**
```python
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
```

### Q9: How do you handle nested serializers and relationships?
**Answer:**

**ForeignKey (Many-to-One):**
```python
# Nested read, PK write
class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_id']
```

**ManyToMany:**
```python
class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        source='categories',
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'categories', 'category_ids']
```

**Reverse Relationships:**
```python
class AuthorSerializer(serializers.ModelSerializer):
    posts = PostMinimalSerializer(many=True, read_only=True)
    post_count = serializers.IntegerField(source='posts.count', read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'posts', 'post_count']
```

**Nested Writes:**
```python
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    
    def create(self, validated_data):
        comments_data = validated_data.pop('comments')
        post = Post.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(post=post, **comment_data)
        return post
```

### Q10: How do you implement custom permissions?
**Answer:**

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit.
    """
    
    def has_permission(self, request, view):
        """View-level check"""
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require authentication
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Object-level check"""
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        return obj.author.user == request.user

# Usage
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
```

**Multiple Permissions (all must pass):**
```python
permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, CanPublishPost]
```

### Q11: How do you implement API versioning?
**Answer:**

**1. URL Path Versioning:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}

# urls.py
urlpatterns = [
    path('api/v1/', include('myapp.api.v1.urls')),
    path('api/v2/', include('myapp.api.v2.urls')),
]
```

**2. Query Parameter Versioning:**
```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
}
# URL: /api/posts/?version=v1
```

**3. Header Versioning:**
```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
}
# Header: Accept: application/json; version=v1
```

**Using Versioning in Views:**
```python
class PostViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return PostSerializerV1
        return PostSerializerV2
```

### Q12: How do you optimize DRF API performance?
**Answer:**

**1. Query Optimization:**
```python
class PostViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Post.objects.select_related('author')\
                          .prefetch_related('categories')\
                          .only('id', 'title', 'slug')
```

**2. Caching:**
```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class PostViewSet(viewsets.ModelViewSet):
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

**3. Pagination:**
```python
# Use CursorPagination for large datasets
class PostViewSet(viewsets.ModelViewSet):
    pagination_class = CursorPagination
```

**4. Field Selection:**
```python
# Only return necessary fields
class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug']  # Minimal fields for list
```

**5. Database Indexing:**
```python
class Post(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['status', '-created_at']),
        ]
```

**6. Bulk Operations:**
```python
@action(detail=False, methods=['post'])
def bulk_create(self, request):
    serializer = self.get_serializer(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)
    Post.objects.bulk_create([Post(**item) for item in serializer.validated_data])
    return Response(serializer.data, status=201)
```

### Q13: How do you handle file uploads in DRF?
**Answer:**

```python
# models.py
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# serializers.py
class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'file', 'file_url', 'uploaded_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def validate_file(self, file):
        # Validate file size (max 5MB)
        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('File too large')
        
        # Validate file extension
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ['.pdf', '.doc', '.docx']:
            raise serializers.ValidationError('Invalid file type')
        
        return file

# views.py
from rest_framework.parsers import MultiPartParser, FormParser

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
```

### Q14: What are custom actions in ViewSets?
**Answer:** Custom actions extend ViewSets with additional endpoints.

```python
from rest_framework.decorators import action

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # Detail action (requires pk)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        """POST /api/posts/{id}/publish/"""
        post = self.get_object()
        post.status = 'published'
        post.save()
        return Response({'status': 'published'})
    
    # Collection action (no pk required)
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """GET /api/posts/featured/"""
        posts = self.get_queryset().filter(featured=True)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    # Multiple HTTP methods
    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        """GET/POST /api/posts/{id}/comments/"""
        post = self.get_object()
        if request.method == 'GET':
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=post, user=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
```

### Q15: How do you test DRF APIs?
**Answer:**

```python
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('user', 'pass')
        self.post = Post.objects.create(title='Test', author=self.user)
    
    def test_list_posts(self):
        """Test GET /api/posts/"""
        url = reverse('post-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_post_authenticated(self):
        """Test POST /api/posts/ (authenticated)"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'Content'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
    
    def test_create_post_unauthenticated(self):
        """Test POST /api/posts/ (not authenticated)"""
        url = reverse('post-list')
        data = {'title': 'New Post'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_post(self):
        """Test PUT /api/posts/{id}/"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated', 'content': 'Updated content'}
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated')
```

---

**This comprehensive guide covers all essential DRF concepts for 3 years of experience. Practice building APIs, understand the "why" behind design decisions, and be prepared to discuss your real-world experience with Django REST Framework projects.**
