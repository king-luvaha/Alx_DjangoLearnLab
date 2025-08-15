from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post

# List view
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # You can change this if your template differs
    context_object_name = 'posts'
    ordering = ['-date_posted']  # Assuming your Post model has date_posted

# Detail view
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Optional if following Django naming conventions

# Create view
class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'  # Default is blog/post_form.html
    fields = ['title', 'content']  # Adjust according to your Post model

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update view
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')   # Change 'post-list' to your actual list view name

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author