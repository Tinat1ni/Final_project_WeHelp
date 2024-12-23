from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, DetailView, ListView
from django.urls import reverse_lazy
from django.core.cache import cache
from django.db.models import Q, Prefetch
from .forms import PostForm
from .models import Post, Category


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    success_url = reverse_lazy('post:post_list')

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return redirect('user:login')

        form.instance.author = self.request.user
        selected_preferences =form.cleaned_data.get('prefer', [])
        existing_categories = Category.objects.filter(name__in=selected_preferences)
        existing_category_names = set(existing_categories.values_list('name', flat=True))

        categories_to_create = [
            Category(name=name) for name in selected_preferences
            if name not in existing_category_names
        ]
        if categories_to_create:
            Category.objects.bulk_create(categories_to_create)

        categories_to_assign = Category.objects.filter(name__in=selected_preferences)

        post = form.save(commit=False)
        post.save()

        post.categories.set(categories_to_assign)

        custom_input_1 = self.request.POST.get('custom_input_1', '') or None
        custom_input_2 = self.request.POST.get('custom_input_2', '') or None


        if not form.cleaned_data.get('picture'):
            form.instance.picture = 'default_images/default_picture.png'
        post.save()

        return super().form_valid(form)


class PostListByCategoryView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'


    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Post.objects.filter(categories__name=category_name).prefetch_related('categories').order_by('-created_at')


class PostListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at').prefetch_related('categories', 'author')


class PostSearchView(ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        cache_key = f"search_{query}"
        cached_results = cache.get(cache_key)

        if cached_results:
            return cached_results

        filters = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(custom_input_1__icontains=query) |
            Q(custom_input_2__icontains=query) |
            Q(author__username__icontains=query) |
            Q(categories__name__icontains=query)
        )
        queryset = Post.objects.filter(filters).distinct().select_related('author').prefetch_related('categories')
        cache.set(cache_key, queryset, timeout=3600)
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'