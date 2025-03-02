
from django.urls import path
from blog import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    path("post-create/", views.PostCreateView.as_view(), name="post-create"),
    path("<int:pk>/complete/", views.PostCompleteView.as_view(), name="post-complete"),
    path('comment/edit/<int:pk>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('comment/like/<int:pk>/', views.CommentLikeToggle.as_view(), name='comment-like-toggle'),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]