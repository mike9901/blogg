
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from blog import models
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class PostListView(ListView):
    model = models.Post
    context_object_name = "posts"
    

class PostDetailView(LoginRequiredMixin, DetailView):
    model = models.Post
    context_object_name = "post"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  # Додаємо порожню форму коментаря в контекст
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.blog = self.get_object()
            comment.save()
            return redirect('blog-detail', pk=comment.blog.pk)
        else:
            # Тут можна обробити випадок з невалідною формою
            pass


class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Post
    form_class = PostForm
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PostCompleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        post.status = "done"
        post.save()
        return HttpResponseRedirect(reverse_lazy("post-list"))

    def get_object(self):
        blog_id = self.kwargs.get("pk")
        return get_object_or_404(models.Post, pk=post_id)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Post
    form_class = PostForm
    # template_name = "tasks/task_update_form.html"
    success_url = reverse_lazy("post-list")


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Post
    success_url = reverse_lazy("post-list")
    # template_name = "tasks/task_delete_confirmation.html"


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Comment
    fields = ['content']
    # template_name = 'tasks/edit_comment.html'

    def form_valid(self, form):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("Ви не можете редагувати цей коментар.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Comment
    template_name = 'post/delete_comment.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'pk': self.object.post.pk})


class CommentLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(models.Comment, pk=self.kwargs.get('pk'))
        like_qs = models.Like.objects.filter(comment=comment, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            models.Like.objects.create(comment=comment, user=request.user)
        return HttpResponseRedirect(comment.get_absolute_url())


class CustomLoginView(LoginView):
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "login"


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("login"))

# Create your views here.
