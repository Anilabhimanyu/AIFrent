# Complete Django Guide

## Table of Contents
1. [Introduction to Django](#introduction-to-django)
2. [Django Architecture](#django-architecture)
3. [Installation & Setup](#installation--setup)
4. [Django Project Structure](#django-project-structure)
5. [Models & Database](#models--database)
6. [Views & URLs](#views--urls)
7. [Templates](#templates)
8. [Forms](#forms)
9. [Admin Interface](#admin-interface)
10. [Authentication & Authorization](#authentication--authorization)
11. [Middleware](#middleware)
12. [Static Files & Media](#static-files--media)
13. [Django REST Framework](#django-rest-framework)
14. [Testing](#testing)
15. [Security](#security)
16. [Performance Optimization](#performance-optimization)
17. [Deployment](#deployment)
18. [Best Practices](#best-practices)
19. [Interview Questions (3 YOE)](#interview-questions-3-years-experience)

---

## Introduction to Django

### What is Django?
- **High-level Python web framework**
- Follows **MVT (Model-View-Template)** architecture
- **"Batteries included"** philosophy - comes with many built-in features
- Created in 2003, maintained by Django Software Foundation
- Used by: Instagram, Pinterest, Mozilla, NASA, National Geographic

### Key Features
- **ORM (Object-Relational Mapping)** - Database abstraction
- **Admin Interface** - Auto-generated admin panel
- **URL Routing** - Clean, elegant URL design
- **Template Engine** - Powerful templating system
- **Forms** - Form handling and validation
- **Authentication** - Built-in user authentication
- **Security** - Protection against common vulnerabilities
- **Scalability** - Can handle high traffic
- **Internationalization** - Multi-language support
- **Caching** - Built-in caching framework

### Django Philosophy
- **DRY (Don't Repeat Yourself)** - Minimize code duplication
- **Explicit is better than implicit** - Clear, readable code
- **Loose coupling** - Components are independent
- **Less code** - Rapid development
- **Convention over configuration** - Sensible defaults

---

## Django Architecture

### MVT Pattern (Model-View-Template)

```
┌─────────────────────────────────────────────────────┐
│                    Django MVT                        │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌─────────┐      ┌──────────┐      ┌───────────┐  │
│  │  Model  │ ───> │   View   │ ───> │ Template  │  │
│  │ (Data)  │      │ (Logic)  │      │   (UI)    │  │
│  └─────────┘      └──────────┘      └───────────┘  │
│       │                 │                   │        │
│       ▼                 ▼                   ▼        │
│  ┌─────────┐      ┌──────────┐      ┌───────────┐  │
│  │Database │      │ Business │      │   HTML    │  │
│  │         │      │  Logic   │      │   CSS     │  │
│  └─────────┘      └──────────┘      └───────────┘  │
└─────────────────────────────────────────────────────┘
```

**Model:**
- Represents data structure
- Database schema definition
- Business logic related to data
- ORM for database operations

**View:**
- Contains business logic
- Processes user requests
- Interacts with models
- Returns HTTP responses

**Template:**
- Presentation layer
- HTML with template tags
- Dynamic content rendering
- Receives data from views

### Request-Response Cycle

```
User Request → URL Dispatcher → View → Model (if needed)
                                 ↓
                          Template Engine
                                 ↓
                          HTML Response → User
```

**Detailed Flow:**
1. User sends HTTP request
2. URL Dispatcher matches URL pattern
3. Corresponding View is called
4. View processes request, queries Model if needed
5. Model interacts with Database
6. View passes data to Template
7. Template renders HTML
8. View returns HTTP response
9. Response sent to User

---

## Installation & Setup

### Prerequisites
```bash
# Python 3.8+ required
python --version

# Install pip (if not installed)
python -m pip install --upgrade pip
```

### Install Django
```bash
# Install latest Django
pip install django

# Install specific version
pip install django==4.2

# Verify installation
django-admin --version
python -m django --version
```

### Create Virtual Environment
```bash
# Create virtual environment
python -m venv myenv

# Activate (Windows)
myenv\Scripts\activate

# Activate (Linux/Mac)
source myenv/bin/activate

# Install Django in venv
pip install django
```

### Create Django Project
```bash
# Create new project
django-admin startproject myproject

# Navigate to project
cd myproject

# Run development server
python manage.py runserver

# Access at: http://127.0.0.1:8000/
```

### Create Django App
```bash
# Create new app
python manage.py startapp myapp

# Register app in settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # Add your app
]
```

---

## Django Project Structure

### Default Project Structure
```
myproject/
│
├── myproject/              # Project configuration
│   ├── __init__.py
│   ├── settings.py         # Configuration settings
│   ├── urls.py             # Project URL patterns
│   ├── asgi.py             # ASGI config
│   └── wsgi.py             # WSGI config
│
├── myapp/                  # Application
│   ├── migrations/         # Database migrations
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py            # Admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Data models
│   ├── tests.py            # Test cases
│   └── views.py            # View functions
│
├── static/                 # Static files (CSS, JS, Images)
├── media/                  # User uploaded files
├── templates/              # HTML templates
├── manage.py               # Management script
└── db.sqlite3              # SQLite database (default)
```

### Key Files Explained

**manage.py:**
- Command-line utility for Django
- Used for: runserver, migrate, createsuperuser, etc.

**settings.py:**
- Project configuration
- Database settings, installed apps, middleware, etc.

**urls.py:**
- URL patterns for the project
- Routes URLs to views

**models.py:**
- Define database models
- ORM class definitions

**views.py:**
- Request handlers
- Business logic

**admin.py:**
- Admin interface customization

---

## Models & Database

### Defining Models

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    """Author model"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    
    def __str__(self):
        return self.name

class Category(models.Model):
    """Blog category"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    """Blog post model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    categories = models.ManyToManyField(Category, related_name='posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.IntegerField(default=0)
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    """Comment on blog post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, 
                               on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
```

### Field Types

**Common Field Types:**
- `CharField` - Short text (max_length required)
- `TextField` - Long text
- `IntegerField` - Integer numbers
- `FloatField` - Floating point numbers
- `DecimalField` - Precise decimal numbers
- `BooleanField` - True/False
- `DateField` - Date (YYYY-MM-DD)
- `DateTimeField` - Date and time
- `EmailField` - Email address
- `URLField` - URL
- `FileField` - File upload
- `ImageField` - Image upload (requires Pillow)
- `JSONField` - JSON data (Django 3.1+)
- `UUIDField` - UUID field

**Relationship Fields:**
- `ForeignKey` - Many-to-One relationship
- `ManyToManyField` - Many-to-Many relationship
- `OneToOneField` - One-to-One relationship

### Field Options

```python
# Common field options
field = models.CharField(
    max_length=100,          # Maximum length
    unique=True,             # Unique constraint
    blank=True,              # Allow empty in forms
    null=True,               # Allow NULL in database
    default='default_value', # Default value
    choices=CHOICES,         # Dropdown choices
    db_index=True,           # Create database index
    editable=False,          # Hide in forms
    help_text='Help text',   # Field description
    verbose_name='Field Name', # Human-readable name
)
```

### Database Operations

```python
# Create
author = Author.objects.create(name='John Doe', email='john@example.com')

# Or using save()
author = Author(name='Jane Doe', email='jane@example.com')
author.save()

# Read - Get single object
author = Author.objects.get(id=1)
author = Author.objects.get(email='john@example.com')

# Read - Filter multiple objects
published_posts = Post.objects.filter(status='published')
recent_posts = Post.objects.filter(created_at__gte='2024-01-01')

# Read - All objects
all_authors = Author.objects.all()

# Update
author = Author.objects.get(id=1)
author.name = 'Updated Name'
author.save()

# Or update directly
Author.objects.filter(id=1).update(name='Updated Name')

# Delete
author = Author.objects.get(id=1)
author.delete()

# Or delete directly
Author.objects.filter(id=1).delete()

# QuerySet chaining
posts = Post.objects.filter(status='published')\
                    .filter(categories__name='Python')\
                    .order_by('-created_at')\
                    .select_related('author')\
                    .prefetch_related('categories')[:10]

# Aggregation
from django.db.models import Count, Avg, Sum, Max, Min

# Count
post_count = Post.objects.count()
author_post_counts = Author.objects.annotate(post_count=Count('posts'))

# Average
avg_views = Post.objects.aggregate(avg_views=Avg('views'))

# Q objects for complex queries
from django.db.models import Q

posts = Post.objects.filter(
    Q(status='published') & (Q(author__name='John') | Q(categories__name='Python'))
)

# F objects for field comparisons
from django.db.models import F

# Get posts with more than 100 views
popular_posts = Post.objects.filter(views__gt=F('author__posts__count') * 10)

# Bulk operations
Post.objects.bulk_create([
    Post(title='Post 1', author=author),
    Post(title='Post 2', author=author),
])

# Raw SQL (when needed)
posts = Post.objects.raw('SELECT * FROM myapp_post WHERE status = %s', ['published'])
```

### Migrations

```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Reverse migration
python manage.py migrate myapp 0003

# Create empty migration
python manage.py makemigrations --empty myapp

# SQL for migration
python manage.py sqlmigrate myapp 0001
```

### Custom Migration Example

```python
# migrations/0002_custom_migration.py
from django.db import migrations

def populate_categories(apps, schema_editor):
    Category = apps.get_model('myapp', 'Category')
    Category.objects.bulk_create([
        Category(name='Python', slug='python'),
        Category(name='Django', slug='django'),
        Category(name='Web Development', slug='web-development'),
    ])

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(populate_categories),
    ]
```

---

## Views & URLs

### Function-Based Views (FBV)

```python
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Post, Author

def home(request):
    """Home page view"""
    posts = Post.objects.filter(status='published').order_by('-created_at')[:10]
    context = {
        'posts': posts,
        'title': 'Home Page'
    }
    return render(request, 'home.html', context)

def post_detail(request, slug):
    """Post detail view"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment views
    post.views += 1
    post.save(update_fields=['views'])
    
    context = {
        'post': post,
        'comments': post.comments.filter(is_approved=True),
    }
    return render(request, 'post_detail.html', context)

@require_http_methods(["GET", "POST"])
def create_post(request):
    """Create new post"""
    if request.method == 'POST':
        # Process form
        title = request.POST.get('title')
        content = request.POST.get('content')
        # ... create post
        return redirect('post_detail', slug=slug)
    
    return render(request, 'create_post.html')

def api_posts(request):
    """JSON API endpoint"""
    posts = Post.objects.filter(status='published').values('title', 'slug', 'created_at')
    return JsonResponse(list(posts), safe=False)
```

### Class-Based Views (CBV)

```python
# views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

class HomeView(TemplateView):
    """Home page"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(status='published')[:10]
        return context

class PostListView(ListView):
    """List all posts"""
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author')

class PostDetailView(DetailView):
    """Post detail"""
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """Create new post"""
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Update post"""
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    
    def get_queryset(self):
        # Only allow editing own posts
        return Post.objects.filter(author__user=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete post"""
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'post_confirm_delete.html'
    
    def get_queryset(self):
        return Post.objects.filter(author__user=self.request.user)
```

### URL Configuration

```python
# urls.py (Project level)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('api/', include('myapp.api_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urls.py (App level)
from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    # Function-based views
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    
    # Class-based views
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail_cbv'),
    path('posts/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # API endpoints
    path('api/posts/', views.api_posts, name='api_posts'),
]

# URL patterns with regex
from django.urls import re_path

urlpatterns = [
    re_path(r'^posts/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^posts/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
]
```

---

## Templates

### Template Syntax

```django
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Site{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <nav>
            <a href="{% url 'home' %}">Home</a>
            <a href="{% url 'post_list' %}">Posts</a>
            {% if user.is_authenticated %}
                <a href="{% url 'post_create' %}">Create Post</a>
                <span>Welcome, {{ user.username }}</span>
                <a href="{% url 'logout' %}">Logout</a>
            {% else %}
                <a href="{% url 'login' %}">Login</a>
            {% endif %}
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; {% now "Y" %} My Site. All rights reserved.</p>
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>

<!-- post_list.html -->
{% extends 'base.html' %}

{% block title %}Posts - {{ block.super }}{% endblock %}

{% block content %}
<h1>Blog Posts</h1>

{% if posts %}
    {% for post in posts %}
        <article>
            <h2><a href="{% url 'post_detail' slug=post.slug %}">{{ post.title }}</a></h2>
            <p class="meta">
                By {{ post.author.name }} on {{ post.created_at|date:"F d, Y" }}
            </p>
            <p>{{ post.content|truncatewords:50 }}</p>
            <p>Views: {{ post.views|default:"0" }}</p>
            
            {% if post.categories.all %}
                <p>Categories:
                {% for category in post.categories.all %}
                    <span class="badge">{{ category.name }}</span>
                    {% if not forloop.last %}, {% endif %}
                {% endfor %}
                </p>
            {% endif %}
        </article>
        
        {% if not forloop.last %}<hr>{% endif %}
    {% endfor %}
    
    <!-- Pagination -->
    {% if is_paginated %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page=1">First</a>
                <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
            {% endif %}
            
            <span>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
            
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">Next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
            {% endif %}
        </div>
    {% endif %}
{% else %}
    <p>No posts available.</p>
{% endif %}
{% endblock %}
```

### Template Tags & Filters

**Built-in Template Tags:**
```django
{% if condition %}...{% endif %}
{% for item in list %}...{% endfor %}
{% with var=value %}...{% endwith %}
{% url 'view_name' arg1 arg2 %}
{% static 'path/to/file' %}
{% csrf_token %}
{% include 'template.html' %}
{% load static %}
{% block name %}...{% endblock %}
{% extends 'base.html' %}
{% comment %}...{% endcomment %}
{% now "Y-m-d" %}
{% spaceless %}...{% endspaceless %}
{% verbatim %}...{% endverbatim %}
```

**Built-in Filters:**
```django
{{ value|default:"nothing" }}
{{ text|truncatewords:30 }}
{{ text|truncatechars:100 }}
{{ text|upper }}
{{ text|lower }}
{{ text|title }}
{{ text|capfirst }}
{{ date|date:"Y-m-d" }}
{{ number|floatformat:2 }}
{{ value|length }}
{{ list|join:", " }}
{{ text|linebreaks }}
{{ text|safe }}
{{ text|escape }}
{{ text|slugify }}
{{ number|add:5 }}
{{ value|yesno:"Yes,No,Maybe" }}
```

### Custom Template Tags & Filters

```python
# myapp/templatetags/custom_tags.py
from django import template
from django.utils.safestring import mark_safe
from ..models import Category

register = template.Library()

# Simple filter
@register.filter(name='multiply')
def multiply(value, arg):
    """Multiply value by argument"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

# Simple tag
@register.simple_tag
def get_categories():
    """Get all categories"""
    return Category.objects.all()

# Inclusion tag
@register.inclusion_tag('tags/sidebar.html')
def show_sidebar(count=5):
    """Render sidebar with recent posts"""
    from ..models import Post
    posts = Post.objects.filter(status='published')[:count]
    return {'posts': posts}

# Filter with is_safe
@register.filter(is_safe=True)
def highlight(text, word):
    """Highlight word in text"""
    highlighted = text.replace(word, f'<mark>{word}</mark>')
    return mark_safe(highlighted)

# Usage in template:
# {% load custom_tags %}
# {{ 10|multiply:5 }}  <!-- 50 -->
# {% get_categories as categories %}
# {% show_sidebar 10 %}
# {{ text|highlight:"Django" }}
```

---

## Forms

### Django Forms

```python
# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """Post creation/edit form"""
    
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'categories', 'status', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'categories': forms.CheckboxSelectMultiple(),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_slug(self):
        """Validate slug"""
        slug = self.cleaned_data.get('slug')
        if Post.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This slug is already in use.')
        return slug
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError('Title must be at least 5 characters long.')
        return title
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        
        if title and content and title.lower() in content.lower():
            raise ValidationError('Content should not contain the exact title.')
        
        return cleaned_data

class CommentForm(forms.ModelForm):
    """Comment form"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
        }

class ContactForm(forms.Form):
    """Contact form (not bound to model)"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise ValidationError('Only @example.com emails are allowed.')
        return email
    
    def send_email(self):
        """Send email (called after form validation)"""
        from django.core.mail import send_mail
        send_mail(
            subject=self.cleaned_data['subject'],
            message=self.cleaned_data['message'],
            from_email=self.cleaned_data['email'],
            recipient_list=['admin@example.com'],
        )
```

### Form Handling in Views

```python
# views.py
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.author
            post.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'post_form.html', {'form': form})

def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'post_form.html', {'form': form, 'post': post})
```

### Form in Template

```django
<!-- post_form.html -->
{% extends 'base.html' %}

{% block content %}
<h1>{% if post %}Edit Post{% else %}Create Post{% endif %}</h1>

<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    <!-- Render entire form -->
    {{ form.as_p }}
    
    <!-- Or render field by field -->
    <div class="form-group">
        {{ form.title.label_tag }}
        {{ form.title }}
        {% if form.title.errors %}
            <div class="error">{{ form.title.errors }}</div>
        {% endif %}
    </div>
    
    <!-- Non-field errors -->
    {% if form.non_field_errors %}
        <div class="alert alert-danger">{{ form.non_field_errors }}</div>
    {% endif %}
    
    <button type="submit" class="btn btn-primary">Save</button>
</form>
{% endblock %}
```

---

## Admin Interface

### Basic Admin Configuration

```python
# admin.py
from django.contrib import admin
from .models import Author, Category, Post, Comment

# Simple registration
admin.site.register(Category)

# Customized admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'views', 'created_at']
    list_filter = ['status', 'created_at', 'categories']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    filter_horizontal = ['categories']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Content', {
            'fields': ('content', 'featured_image')
        }),
        ('Categories', {
            'fields': ('categories',)
        }),
        ('Metadata', {
            'fields': ('views', 'published_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'views']
    
    actions = ['make_published', 'make_draft']
    
    def make_published(self, request, queryset):
        """Custom action to publish posts"""
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} posts published.')
    make_published.short_description = 'Mark selected posts as published'
    
    def make_draft(self, request, queryset):
        """Custom action to draft posts"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts moved to draft.')

class CommentInline(admin.TabularInline):
    """Inline comments in post admin"""
    model = Comment
    extra = 0
    fields = ['user', 'content', 'is_approved']
    readonly_fields = ['user', 'created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'user__username', 'post__title']
    actions = ['approve_comments', 'reject_comments']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Approve selected comments'
    
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)

# Customize admin site
admin.site.site_header = 'My Blog Admin'
admin.site.site_title = 'My Blog Admin Portal'
admin.site.index_title = 'Welcome to My Blog Admin'
```

---

## Authentication & Authorization

### User Authentication

```python
# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    """User logout"""
    logout(request)
    return redirect('home')

def user_register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    """User profile (requires login)"""
    return render(request, 'profile.html')

# Class-based view with login required
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = '/login/'
```

### Permissions & Groups

```python
# Check permissions in views
from django.contrib.auth.decorators import permission_required

@permission_required('myapp.add_post')
def create_post(request):
    # Only users with add_post permission
    pass

@permission_required(['myapp.change_post', 'myapp.delete_post'])
def edit_post(request, pk):
    # User needs both permissions
    pass

# Class-based view
from django.contrib.auth.mixins import PermissionRequiredMixin

class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'myapp.add_post'
    model = Post

# Custom permission checks
def my_view(request):
    if not request.user.has_perm('myapp.can_publish'):
        return HttpResponseForbidden()
    
    # Check object-level permission
    post = Post.objects.get(pk=1)
    if not request.user.has_perm('myapp.change_post', post):
        return HttpResponseForbidden()

# Add custom permissions in model
class Post(models.Model):
    # ... fields ...
    
    class Meta:
        permissions = [
            ("can_publish", "Can publish posts"),
            ("can_feature", "Can feature posts"),
        ]

# Working with groups
from django.contrib.auth.models import Group, Permission

# Create group
editors_group = Group.objects.create(name='Editors')

# Add permissions to group
permission = Permission.objects.get(codename='add_post')
editors_group.permissions.add(permission)

# Add user to group
user.groups.add(editors_group)

# Check if user in group
if user.groups.filter(name='Editors').exists():
    # User is an editor
    pass
```

---

## Middleware

### Built-in Middleware

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### Custom Middleware

```python
# middleware.py
import time
from django.utils.deprecation import MiddlewareMixin

class RequestTimingMiddleware(MiddlewareMixin):
    """Measure request processing time"""
    
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Request-Duration'] = str(duration)
        return response

class CustomHeaderMiddleware:
    """Add custom header to all responses"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Code before view
        request.custom_data = 'Some value'
        
        response = self.get_response(request)
        
        # Code after view
        response['X-Custom-Header'] = 'My Value'
        return response

class RestrictIPMiddleware:
    """Restrict access based on IP"""
    
    ALLOWED_IPS = ['127.0.0.1', '192.168.1.1']
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip not in self.ALLOWED_IPS:
            return HttpResponseForbidden('Access denied')
        return self.get_response(request)

# Add to MIDDLEWARE in settings.py
MIDDLEWARE = [
    # ... other middleware
    'myapp.middleware.RequestTimingMiddleware',
    'myapp.middleware.CustomHeaderMiddleware',
]
```

---

## Static Files & Media

### Configuration

```python
# settings.py

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Project Structure

```
project/
├── static/                    # Development static files
│   ├── css/
│   ├── js/
│   └── images/
├── staticfiles/               # Collected static files (production)
├── media/                     # User uploads
│   ├── posts/
│   └── avatars/
└── templates/
```

### Usage in Templates

```django
{% load static %}

<!-- Static files -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">

<!-- Media files -->
{% if post.featured_image %}
    <img src="{{ post.featured_image.url }}" alt="{{ post.title }}">
{% endif %}
```

### Collect Static Files

```bash
# Collect all static files to STATIC_ROOT
python manage.py collectstatic

# Clear existing files first
python manage.py collectstatic --clear --noinput
```

---

## Django REST Framework

### Installation & Setup

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

### Serializers

```python
# serializers.py
from rest_framework import serializers
from .models import Post, Author, Category, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class AuthorSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'post_count']
    
    def get_post_count(self, obj):
        return obj.posts.count()

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'categories', 
                  'content', 'status', 'views', 'comments_count', 
                  'created_at', 'updated_at']
        read_only_fields = ['views', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title too short")
        return value

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at', 'is_approved']
        read_only_fields = ['user', 'created_at', 'is_approved']
```

### API Views

```python
# views.py (API)
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Author, Category
from .serializers import PostSerializer, AuthorSerializer, CategorySerializer

# ViewSet
class PostViewSet(viewsets.ModelViewSet):
    """API endpoint for posts"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'author', 'categories']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Custom action to publish post"""
        post = self.get_object()
        post.status = 'published'
        post.save()
        return Response({'status': 'post published'})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured posts"""
        featured_posts = Post.objects.filter(status='published', views__gte=100)
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)

# Function-based API view
@api_view(['GET', 'POST'])
def post_list(request):
    """List all posts or create new post"""
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user.author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    """Retrieve, update or delete post"""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### API URLs

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
```

---

## Testing

### Unit Tests

```python
# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Author, Category

class PostModelTest(TestCase):
    """Test Post model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.author = Author.objects.create(name='Test Author', email='test@example.com')
        self.category = Category.objects.create(name='Python', slug='python')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.author,
            content='Test content',
            status='published'
        )
    
    def test_post_creation(self):
        """Test post is created correctly"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.slug, 'test-post')
        self.assertEqual(self.post.status, 'published')
    
    def test_post_str(self):
        """Test __str__ method"""
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_post_get_absolute_url(self):
        """Test get_absolute_url method"""
        url = self.post.get_absolute_url()
        self.assertEqual(url, '/post/test-post/')
    
    def test_post_categories(self):
        """Test many-to-many relationship"""
        self.post.categories.add(self.category)
        self.assertEqual(self.post.categories.count(), 1)
        self.assertIn(self.category, self.post.categories.all())

class PostViewTest(TestCase):
    """Test Post views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.author = Author.objects.create(name='Test Author', email='test@example.com')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.author,
            content='Test content',
            status='published'
        )
    
    def test_post_list_view(self):
        """Test post list view"""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'post_list.html')
    
    def test_post_detail_view(self):
        """Test post detail view"""
        response = self.client.get(reverse('post_detail', kwargs={'slug': 'test-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test content')
    
    def test_post_create_view_authenticated(self):
        """Test post creation requires authentication"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_create_view_unauthenticated(self):
        """Test post creation redirects if not authenticated"""
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

class PostFormTest(TestCase):
    """Test Post forms"""
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author', email='test@example.com')
    
    def test_valid_form(self):
        """Test form with valid data"""
        from .forms import PostForm
        data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'content': 'Test content',
            'status': 'draft'
        }
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_short_title(self):
        """Test form with invalid title"""
        from .forms import PostForm
        data = {
            'title': 'Test',  # Too short
            'slug': 'test',
            'content': 'Test content',
            'status': 'draft'
        }
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test myapp

# Run specific test class
python manage.py test myapp.tests.PostModelTest

# Run specific test method
python manage.py test myapp.tests.PostModelTest.test_post_creation

# With verbose output
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb

# Parallel testing
python manage.py test --parallel
```

---

## Security

### Security Settings

```python
# settings.py

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware
]

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### Common Security Practices

**1. CSRF Protection:**
```django
<!-- Always include csrf_token in forms -->
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**2. SQL Injection Prevention:**
```python
# GOOD - Using ORM (safe)
Post.objects.filter(status='published')

# BAD - Raw SQL without parameterization
Post.objects.raw("SELECT * FROM posts WHERE status = '%s'" % status)

# GOOD - Parameterized raw SQL
Post.objects.raw("SELECT * FROM posts WHERE status = %s", [status])
```

**3. XSS Prevention:**
```django
<!-- Auto-escaped by default -->
{{ user_input }}

<!-- Mark as safe only if you trust the content -->
{{ trusted_html|safe }}
```

**4. Authentication:**
```python
# Use built-in authentication
from django.contrib.auth.decorators import login_required

@login_required
def sensitive_view(request):
    pass
```

---

## Performance Optimization

### Database Optimization

```python
# 1. select_related (for ForeignKey, OneToOneField)
# Reduces queries by performing SQL join
posts = Post.objects.select_related('author').all()

# 2. prefetch_related (for ManyToManyField, reverse ForeignKey)
# Reduces queries by fetching related objects in separate query
posts = Post.objects.prefetch_related('categories', 'comments').all()

# 3. only() - Fetch only specified fields
posts = Post.objects.only('id', 'title', 'slug')

# 4. defer() - Exclude specified fields
posts = Post.objects.defer('content')

# 5. values() / values_list() - Return dictionaries/tuples instead of model instances
posts = Post.objects.values('id', 'title')
titles = Post.objects.values_list('title', flat=True)

# 6. Bulk operations
# Bulk create
Post.objects.bulk_create([
    Post(title='Post 1', author=author),
    Post(title='Post 2', author=author),
])

# Bulk update
Post.objects.filter(status='draft').update(status='published')

# 7. Database indexes
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]

# 8. Count efficiently
# GOOD
Post.objects.count()

# BAD
len(Post.objects.all())

# 9. exists() instead of count() for checking existence
# GOOD
if Post.objects.filter(slug=slug).exists():
    pass

# BAD
if Post.objects.filter(slug=slug).count() > 0:
    pass
```

### Caching

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Per-view caching
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def my_view(request):
    pass

# Template fragment caching
{% load cache %}
{% cache 500 sidebar %}
    <!-- sidebar content -->
{% endcache %}

# Low-level cache API
from django.core.cache import cache

# Set cache
cache.set('key', 'value', timeout=300)

# Get cache
value = cache.get('key')

# Get with default
value = cache.get('key', 'default')

# Delete
cache.delete('key')

# Set many
cache.set_many({'a': 1, 'b': 2, 'c': 3})

# Get many
cache.get_many(['a', 'b', 'c'])
```

### Query Optimization

```python
# Use Django Debug Toolbar to identify N+1 queries
# Install: pip install django-debug-toolbar

# settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

---

## Deployment

### Production Settings

```python
# settings/production.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

# Static files
STATIC_ROOT = '/var/www/static/'
MEDIA_ROOT = '/var/www/media/'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Deployment Checklist

```bash
# Run deployment check
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Common Deployment Platforms

**1. Heroku:**
```bash
# Procfile
web: gunicorn myproject.wsgi

# requirements.txt
Django==4.2
gunicorn
psycopg2-binary
```

**2. AWS (with Gunicorn + Nginx):**
```bash
# Install Gunicorn
pip install gunicorn

# Run Gunicorn
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
```

**3. Docker:**
```dockerfile
# Dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## Best Practices

### 1. Project Structure
```
project/
├── config/                    # Settings files
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                      # All Django apps
│   ├── blog/
│   ├── users/
│   └── api/
├── static/
├── media/
├── templates/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
└── manage.py
```

### 2. Model Best Practices
- Use meaningful model names (singular, e.g., `Post`, not `Posts`)
- Always define `__str__` method
- Use `auto_now_add` and `auto_now` for timestamps
- Add indexes to frequently queried fields
- Use `blank=True` for optional form fields
- Use `null=True` for optional database fields
- Keep business logic in models, not views

### 3. View Best Practices
- Keep views thin, move logic to models/services
- Use class-based views for CRUD operations
- Use function-based views for simple operations
- Always validate user input
- Use `get_object_or_404` instead of try/except
- Return appropriate HTTP status codes

### 4. URL Best Practices
- Use meaningful URL patterns
- Use `app_name` for URL namespacing
- Use named URLs (avoid hardcoding URLs)
- Keep URLs consistent and RESTful

### 5. Template Best Practices
- Use template inheritance (extends)
- Keep logic in views, not templates
- Use template filters for formatting
- Create custom template tags for reusable components
- Always escape user input (Django does this by default)

### 6. Security Best Practices
- Never commit SECRET_KEY to version control
- Use environment variables for sensitive data
- Keep Django and dependencies updated
- Use HTTPS in production
- Implement proper authentication and authorization
- Validate and sanitize all user input
- Use CSRF protection
- Implement rate limiting

### 7. Performance Best Practices
- Use `select_related` and `prefetch_related`
- Implement caching where appropriate
- Use database indexes
- Optimize queries (avoid N+1 problem)
- Use pagination for large datasets
- Compress and minify static files
- Use CDN for static files in production

---

## Interview Questions (3 Years Experience)

### Basic Django Concepts

**Q1: Explain Django's MVT architecture.**
**Answer:** Django follows the MVT (Model-View-Template) pattern:
- **Model:** Represents the data structure and handles database operations using Django's ORM
- **View:** Contains business logic, processes requests, interacts with models, and returns responses
- **Template:** Presentation layer that renders HTML with dynamic content using Django's template engine
- URL Dispatcher routes requests to appropriate views

**Q2: What is Django ORM? What are its advantages?**
**Answer:** Django ORM (Object-Relational Mapping) is a technique that lets you interact with databases using Python code instead of SQL.

Advantages:
- Database agnostic - work with different databases using same code
- Prevents SQL injection attacks automatically
- Cleaner, more Pythonic code
- Automatic schema migrations
- Built-in query optimization
- Relationships handled elegantly (ForeignKey, ManyToMany)

**Q3: Explain the difference between `null=True` and `blank=True`.**
**Answer:**
- `null=True` - Database-level: Allows NULL values in the database column
- `blank=True` - Validation-level: Allows empty values in forms (not required)
- Example:
```python
# Optional text field (form can be empty, but DB stores empty string, not NULL)
bio = models.TextField(blank=True)

# Optional foreign key (form can be empty, DB can have NULL)
category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
```

**Q4: What is the difference between `select_related` and `prefetch_related`?**
**Answer:**
- **`select_related`:** 
  - For ForeignKey and OneToOneField relationships
  - Uses SQL JOIN in single query
  - More efficient for single relationships
  ```python
  posts = Post.objects.select_related('author')  # Single query with JOIN
  ```

- **`prefetch_related`:**
  - For ManyToManyField and reverse ForeignKey
  - Uses separate queries then joins in Python
  - Better for many-to-many relationships
  ```python
  posts = Post.objects.prefetch_related('categories')  # 2 queries
  ```

**Q5: Explain Django's request-response cycle.**
**Answer:**
1. User makes HTTP request
2. WSGI/ASGI server receives request
3. Middleware processes request (authentication, sessions, etc.)
4. URL dispatcher matches URL pattern
5. View function/class is called
6. View queries Model (if needed) and prepares context
7. Template renders with context data
8. View returns HttpResponse
9. Middleware processes response
10. Response sent to user

### Models & Database

**Q6: How do you handle database migrations in Django?**
**Answer:**
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Reverse migration
python manage.py migrate app_name migration_name

# See SQL for migration
python manage.py sqlmigrate app_name 0001
```

Best practices:
- Review migrations before applying
- Commit migrations to version control
- Test migrations on staging before production
- Use data migrations for complex data transformations
- Never edit applied migrations

**Q7: What are Django signals? Provide use cases.**
**Answer:** Signals allow decoupled applications to get notified when actions occur elsewhere in the framework.

Common signals:
- `pre_save` / `post_save` - Before/after model save
- `pre_delete` / `post_delete` - Before/after model delete
- `m2m_changed` - ManyToMany field changes
- `request_started` / `request_finished` - HTTP request lifecycle

Example:
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Only for new users
        send_mail(
            'Welcome!',
            'Thanks for signing up.',
            'from@example.com',
            [instance.email],
        )
```

Use cases:
- Send notifications
- Create related objects automatically
- Update cache
- Log activities
- Trigger background tasks

**Q8: Explain different types of relationships in Django.**
**Answer:**
```python
# 1. One-to-Many (ForeignKey)
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')

# Access:
author.posts.all()  # All posts by author
post.author         # Author of post

# 2. Many-to-Many (ManyToManyField)
class Post(models.Model):
    categories = models.ManyToManyField(Category, related_name='posts')

# Access:
post.categories.all()     # All categories of post
category.posts.all()      # All posts in category

# 3. One-to-One (OneToOneField)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# Access:
user.userprofile         # Profile of user
profile.user             # User of profile
```

`on_delete` options:
- `CASCADE` - Delete related objects
- `PROTECT` - Prevent deletion
- `SET_NULL` - Set to NULL (requires null=True)
- `SET_DEFAULT` - Set to default value
- `SET()` - Set to value from function
- `DO_NOTHING` - Do nothing (database must handle)

**Q9: How would you optimize a slow query in Django?**
**Answer:**
1. **Identify the problem:** Use Django Debug Toolbar or `queryset.explain()`
2. **Solutions:**
```python
# Add select_related for ForeignKey
posts = Post.objects.select_related('author')

# Add prefetch_related for ManyToMany
posts = Post.objects.prefetch_related('categories', 'comments')

# Use only() to fetch specific fields
posts = Post.objects.only('id', 'title')

# Add database indexes
class Meta:
    indexes = [
        models.Index(fields=['created_at']),
        models.Index(fields=['slug', 'status']),
    ]

# Use annotate for aggregations
from django.db.models import Count
authors = Author.objects.annotate(post_count=Count('posts'))

# Cache expensive queries
from django.core.cache import cache
posts = cache.get('featured_posts')
if not posts:
    posts = Post.objects.filter(featured=True)
    cache.set('featured_posts', posts, 3600)
```

### Views & URLs

**Q10: Difference between function-based views and class-based views?**
**Answer:**

**Function-Based Views (FBV):**
- Simple and explicit
- Easy to understand for beginners
- Good for simple views
- More flexible for custom logic

**Class-Based Views (CBV):**
- Reusable and extendable
- Built-in generic views (ListView, DetailView, etc.)
- DRY principle - less code
- Uses mixins for additional functionality
- Better for CRUD operations

Example:
```python
# FBV
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

# CBV
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
```

**Q11: What are Django middleware? Give examples.**
**Answer:** Middleware is a framework of hooks into Django's request/response processing. It's a way to process requests globally before they reach the view.

Common use cases:
- Authentication
- Session management
- CSRF protection
- Logging
- Custom headers
- Rate limiting

Example:
```python
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Code before view
        print(f"Request: {request.path}")
        
        response = self.get_response(request)
        
        # Code after view
        print(f"Response status: {response.status_code}")
        return response
```

Order matters! Middleware is processed in order for requests and reverse order for responses.

**Q12: How do you handle file uploads in Django?**
**Answer:**
```python
# Model
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Form
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']

# View
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})

# Template
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>

# Settings
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

For production:
- Use cloud storage (AWS S3, Google Cloud Storage)
- Validate file types and sizes
- Scan for viruses
- Use django-storages library

### Django REST Framework

**Q13: How do you create a RESTful API in Django?**
**Answer:**
```python
# Install DRF
# pip install djangorestframework

# Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']

# ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# URLs
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

This provides:
- GET /api/posts/ - List all posts
- POST /api/posts/ - Create post
- GET /api/posts/1/ - Retrieve post
- PUT /api/posts/1/ - Update post
- DELETE /api/posts/1/ - Delete post

**Q14: How do you implement authentication in DRF?**
**Answer:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Token authentication
# Install: pip install djangorestframework
# Add to INSTALLED_APPS: 'rest_framework.authtoken'
# Run: python manage.py migrate

# Generate token for user
from rest_framework.authtoken.models import Token
token = Token.objects.create(user=user)

# Use in API request
# Header: Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# JWT authentication (more secure)
# Install: pip install djangorestframework-simplejwt

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
```

### Security

**Q15: What security measures does Django provide?**
**Answer:**
1. **CSRF Protection:** Automatic protection against Cross-Site Request Forgery
2. **SQL Injection Protection:** ORM automatically escapes parameters
3. **XSS Protection:** Template engine auto-escapes variables
4. **Clickjacking Protection:** X-Frame-Options header
5. **SSL/HTTPS Support:** Secure cookies, SSL redirect
6. **Password Hashing:** PBKDF2 with SHA256 by default
7. **User Authentication:** Built-in authentication system
8. **Session Security:** Secure session cookies
9. **Content Security Policy:** Prevent XSS attacks
10. **Security Middleware:** Multiple security headers

Example settings:
```python
# CSRF
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# XSS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Clickjacking
X_FRAME_OPTIONS = 'DENY'
```

**Q16: How do you prevent SQL injection in Django?**
**Answer:**
Django's ORM automatically prevents SQL injection by:
1. Using parameterized queries
2. Escaping special characters
3. Using prepared statements

```python
# SAFE - ORM automatically parameterizes
users = User.objects.filter(username=username)

# SAFE - Using raw() with parameters
users = User.objects.raw('SELECT * FROM users WHERE username = %s', [username])

# UNSAFE - String formatting (DON'T DO THIS!)
users = User.objects.raw(f'SELECT * FROM users WHERE username = "{username}"')
```

Additional protection:
- Use ORM instead of raw SQL when possible
- If using raw SQL, always use parameterization
- Validate and sanitize user input
- Use Django forms for input validation
- Limit database user permissions

### Performance & Optimization

**Q17: How would you improve Django application performance?**
**Answer:**

**1. Database Optimization:**
```python
# Use select_related and prefetch_related
posts = Post.objects.select_related('author').prefetch_related('categories')

# Add database indexes
class Meta:
    indexes = [models.Index(fields=['created_at', 'status'])]

# Use only() and defer()
posts = Post.objects.only('title', 'slug')

# Bulk operations
Post.objects.bulk_create([...])
Post.objects.update(status='published')
```

**2. Caching:**
```python
# View caching
from django.views.decorators.cache import cache_page
@cache_page(60 * 15)
def my_view(request):
    pass

# Template fragment caching
{% cache 500 sidebar %}...{% endcache %}

# Low-level caching
from django.core.cache import cache
cache.set('key', 'value', 300)
value = cache.get('key')
```

**3. Query Optimization:**
- Avoid N+1 queries
- Use pagination
- Use count() instead of len()
- Use exists() instead of count() for checking existence

**4. Other Optimizations:**
- Use CDN for static files
- Compress and minify CSS/JS
- Enable GZIP compression
- Use connection pooling
- Implement database read replicas
- Use asynchronous tasks (Celery) for heavy operations
- Optimize images
- Use HTTP/2

**Q18: What is Django's caching framework?**
**Answer:**
Django supports multiple cache backends:

1. **Memcached** - Fast, production-ready
2. **Redis** - Feature-rich, persistent
3. **Database** - Simple, not recommended for production
4. **Filesystem** - For development
5. **Local memory** - For development/testing

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Cache levels in Django:
# 1. Per-site cache (entire site)
# 2. Per-view cache (specific views)
# 3. Template fragment cache (parts of templates)
# 4. Low-level cache API (manual control)
```

### Advanced Topics

**Q19: What is Django's ORM lazy loading?**
**Answer:**
Django QuerySets are lazy - they don't hit the database until you actually need the data.

```python
# No database hit yet
posts = Post.objects.filter(status='published')

# Database hit happens here
for post in posts:  # Iteration
    print(post.title)

# Or here
post_list = list(posts)  # Conversion to list

# Or here
count = posts.count()  # Aggregation

# Query is cached after first evaluation
posts = Post.objects.all()
list(posts)  # Database hit
list(posts)  # Uses cached result, no database hit
```

Benefits:
- Efficient - only queries when needed
- Can chain filters before execution
- Allows query optimization

**Q20: Explain Django's template inheritance.**
**Answer:**
Template inheritance allows you to build a base template with common elements and extend it in child templates.

```django
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    <header>{% block header %}Default Header{% endblock %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}Default Footer{% endblock %}</footer>
</body>
</html>

<!-- child.html -->
{% extends 'base.html' %}

{% block title %}Child Page - {{ block.super }}{% endblock %}

{% block content %}
    <h1>Child Page Content</h1>
{% endblock %}
```

Benefits:
- DRY principle
- Consistent layout
- Easy maintenance
- Overrideable blocks

**Q21: How do you handle asynchronous tasks in Django?**
**Answer:**
Use Celery - distributed task queue for asynchronous processing.

```python
# Install
# pip install celery redis

# celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(subject, message, recipient):
    send_mail(subject, message, 'from@example.com', [recipient])
    return f'Email sent to {recipient}'

@shared_task
def process_large_file(file_path):
    # Heavy processing
    pass

# Use in views
def my_view(request):
    # Asynchronous execution
    send_email_task.delay('Subject', 'Message', 'user@example.com')
    return HttpResponse('Task queued')

# Run Celery worker
# celery -A myproject worker -l info

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

Use cases:
- Send emails
- Process files
- Generate reports
- API calls to external services
- Scheduled tasks (periodic tasks)

**Q22: What are Django management commands?**
**Answer:**
Custom management commands extend `python manage.py` functionality.

```python
# myapp/management/commands/cleanup_posts.py
from django.core.management.base import BaseCommand
from myapp.models import Post
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete draft posts older than 30 days'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days (default: 30)',
        )
    
    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)
        
        posts = Post.objects.filter(
            status='draft',
            created_at__lt=cutoff_date
        )
        
        count = posts.count()
        posts.delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} posts')
        )

# Run command
# python manage.py cleanup_posts
# python manage.py cleanup_posts --days=60
```

Common use cases:
- Data cleanup
- Import/export data
- Scheduled tasks
- Database maintenance
- Deployment tasks

**Q23: How do you implement pagination in Django?**
**Answer:**

**In Views:**
```python
from django.core.paginator import Paginator

def post_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 10)  # 10 posts per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'post_list.html', {'page_obj': page_obj})

# Class-based view
class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'post_list.html'
```

**In Templates:**
```django
{% for post in page_obj %}
    <h2>{{ post.title }}</h2>
{% endfor %}

<div class="pagination">
    {% if page_obj.has_previous %}
        <a href="?page=1">First</a>
        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
    {% endif %}
    
    <span>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
    
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Next</a>
        <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
    {% endif %}
</div>
```

**In DRF:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

**Q24: How do you handle multiple databases in Django?**
**Answer:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'primary_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'users_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'users_database',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

# Database router
class MyDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'users_db'
        return 'default'
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'users_db'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'users':
            return db == 'users_db'
        return db == 'default'

DATABASE_ROUTERS = ['myapp.routers.MyDatabaseRouter']

# Usage
# Explicit database selection
User.objects.using('users_db').all()
post = Post.objects.using('default').get(id=1)

# Migrations
python manage.py migrate --database=users_db
```

**Q25: What is Django's context processor?**
**Answer:**
Context processors add variables to the context of every template automatically.

```python
# myapp/context_processors.py
def site_settings(request):
    return {
        'SITE_NAME': 'My Blog',
        'CURRENT_YEAR': datetime.now().year,
    }

def user_info(request):
    if request.user.is_authenticated:
        return {
            'user_posts_count': request.user.posts.count(),
        }
    return {}

# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'myapp.context_processors.site_settings',
                'myapp.context_processors.user_info',
            ],
        },
    },
]

# Now available in all templates
{{ SITE_NAME }}  <!-- My Blog -->
{{ CURRENT_YEAR }}  <!-- 2026 -->
{{ user_posts_count }}
```

Built-in context processors:
- `debug` - DEBUG and SQL queries
- `request` - request object
- `auth` - user and perms
- `messages` - messages framework
- `media` - MEDIA_URL
- `static` - STATIC_URL
- `csrf` - CSRF token

---

## Additional Interview Topics

### Scenario-Based Questions

**Q26: How would you build a multi-tenant application in Django?**
**Answer:**
Three approaches:

1. **Shared Database, Shared Schema:**
```python
class Post(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    # ... other fields

# Filter by tenant in every query
posts = Post.objects.filter(tenant=request.tenant)
```

2. **Shared Database, Separate Schemas:**
```python
# Use django-tenants package
# pip install django-tenants

# Each tenant gets its own schema in same database
```

3. **Separate Databases:**
```python
# Use database routing
# Each tenant gets separate database
```

Best practices:
- Use middleware to identify tenant
- Enforce tenant isolation at model level
- Use row-level security
- Regular audits
- Data migration strategies

**Q27: How do you implement API versioning?**
**Answer:**
```python
# URL-based versioning
urlpatterns = [
    path('api/v1/', include('myapp.api.v1.urls')),
    path('api/v2/', include('myapp.api.v2.urls')),
]

# Header-based versioning
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
}

# Query parameter versioning
# /api/posts/?version=2

# ViewSet with versioning
class PostViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return PostSerializerV1
        return PostSerializerV2
```

**Q28: How do you handle database transactions?**
**Answer:**
```python
from django.db import transaction

# Method 1: Decorator
@transaction.atomic
def create_post_with_comments(post_data, comments_data):
    post = Post.objects.create(**post_data)
    for comment_data in comments_data:
        Comment.objects.create(post=post, **comment_data)
    return post

# Method 2: Context manager
def create_user_and_profile(user_data, profile_data):
    try:
        with transaction.atomic():
            user = User.objects.create(**user_data)
            UserProfile.objects.create(user=user, **profile_data)
            return user
    except Exception as e:
        # Transaction rolled back automatically
        raise

# Savepoints (nested transactions)
with transaction.atomic():
    post = Post.objects.create(title='Post 1')
    
    sid = transaction.savepoint()
    try:
        Comment.objects.create(post=post, content='Bad comment')
        transaction.savepoint_commit(sid)
    except:
        transaction.savepoint_rollback(sid)
```

**Q29: How would you implement real-time features in Django?**
**Answer:**
Use Django Channels for WebSocket support:

```python
# Install
# pip install channels channels-redis

# settings.py
INSTALLED_APPS = [
    'channels',
    # ...
]

ASGI_APPLICATION = 'myproject.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

# routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
```

Use cases:
- Real-time chat
- Live notifications
- Collaborative editing
- Live dashboards
- Gaming

**Q30: What is the difference between Django's `get()` and `filter()`?**
**Answer:**
```python
# get() - Returns single object or raises exception
post = Post.objects.get(id=1)  # Returns Post object
post = Post.objects.get(slug='test')  # DoesNotExist if not found
post = Post.objects.get(status='published')  # MultipleObjectsReturned if > 1

# filter() - Always returns QuerySet (even if 0 or 1 result)
posts = Post.objects.filter(id=1)  # Returns QuerySet with 0 or 1 object
posts = Post.objects.filter(status='published')  # Returns QuerySet with N objects
posts = Post.objects.filter(title='nonexistent')  # Returns empty QuerySet []

# Best practices:
# Use get() when:
# - Querying by primary key
# - Expecting exactly one result
# - Want exception if not found

# Use filter() when:
# - Expecting multiple results
# - Result might not exist (check with .exists())
# - Need to chain more filters

# Safe alternative to get()
from django.shortcuts import get_object_or_404
post = get_object_or_404(Post, id=1)  # Returns 404 response if not found
```

---

## Tips for Interview Success

### Technical Preparation
1. **Practice coding:** Implement a small blog/e-commerce app
2. **Review documentation:** Official Django docs
3. **Understand core concepts:** ORM, views, templates, forms
4. **Know DRF well:** Serializers, ViewSets, authentication
5. **Study performance optimization:** Caching, query optimization
6. **Security awareness:** CSRF, XSS, SQL injection prevention
7. **Deployment knowledge:** Settings, static files, WSGI/ASGI

### Behavioral Preparation
1. **Project discussion:** Be ready to discuss your Django projects in detail
2. **Challenges faced:** How you solved complex problems
3. **Best practices:** Why you follow certain patterns
4. **Stay updated:** Latest Django version features
5. **Open source:** Contribute to Django projects

### Common Mistakes to Avoid
1. Not using Django's built-in features
2. Writing inefficient queries (N+1 problem)
3. Not understanding middleware execution order
4. Ignoring security best practices
5. Hardcoding configuration values
6. Not writing tests
7. Poor project structure
8. Not using version control effectively

### Resources for Further Learning
- **Official Django Documentation:** docs.djangoproject.com
- **Django REST Framework:** django-rest-framework.org
- **Django Packages:** djangopackages.org
- **Two Scoops of Django** (Book)
- **Django for Professionals** (Book)
- **Real Python Django Tutorials**
- **Django Discord/Community**

---

**Good luck with your Django interviews!**

*This guide covers essential Django concepts for 3 years of experience. Practice implementing these concepts, understand the "why" behind design decisions, and be prepared to discuss your real-world experience with Django projects.*
