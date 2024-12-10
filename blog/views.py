from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# Function-based view for the home page
# Fetches all posts from the database and renders them on the home page.
def home(request):
    context = {
        'posts': Post.objects.all()  # Fetch all posts
    }
    return render(request, 'blog/home.html', context)

# Class-based view for listing posts
# Displays a list of posts in the 'blog/home.html' template.
class PostListView(ListView):
    model = Post  # Specifies the model to use
    template_name = 'blog/home.html'  # Template for displaying the list of posts
    context_object_name = 'posts'  # Context variable name for template
    ordering = ['-date_posted']  # Orders posts by newest first
    paginate_by = 10

class UserPostListView(ListView):
    model = Post  # Specifies the model to use
    template_name = 'blog/user_posts.html'  # Template for displaying the list of posts
    context_object_name = 'posts'  # Context variable name for template
    ordering = ['-date_posted']  # Orders posts by newest first
    paginate_by = 10

    def get_queryset(self):
        # Fetch the user based on the 'username' in the URL
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # Return posts that belong to the specified user, ordered by the newest first
        return Post.objects.filter(author=user).order_by('-date_posted')


# Class-based view for displaying post details
# Displays the details of a single post in the 'blog/post_detail.html' template.
class PostDetailView(DetailView):
    model = Post  # Specifies the model to use
    template_name = 'blog/post_detail.html'  # Template for post details


# Class-based view for creating a new post
# Only accessible to logged-in users due to the LoginRequiredMixin.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post  # Specifies the model to use
    fields = ['title', 'content']  # Specifies the fields to display in the form

    # Ensures that the logged-in user is set as the author of the post.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Class-based view for updating an existing post
# Only accessible to the author of the post and logged-in users.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post  # Specifies the model to use
    fields = ['title', 'content']  # Specifies the fields to display in the form

    # Ensures that the logged-in user is set as the author of the updated post.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Test function to ensure that only the author can update their own posts.
    def test_func(self):
        post = self.get_object()  # Fetches the post being updated
        if self.request.user == post.author:  # Checks if the logged-in user is the author
            return True
        return False


# Class-based view for deleting a post
# Only accessible to the author of the post and logged-in users.
# After deletion, redirects to the post list (home page).
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post  # Specifies the model to use
    template_name = 'blog/post_confirm_delete.html'  # Template for post deletion confirmation
    success_url = reverse_lazy('blog-home')  # Redirect to home page after successful deletion

    # Test function to ensure that only the author can delete their own posts.
    def test_func(self):
        post = self.get_object()  # Fetches the post being deleted
        if self.request.user == post.author:  # Checks if the logged-in user is the author
            return True
        return False

    # Override the form_valid method to add a success message
    def form_valid(self, form):
        messages.success(self.request, "Your post was successfully deleted.")  # Success message
        return super().form_valid(form)


# Function-based view for the About page
# Renders the 'About' page with a title in the context.
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
