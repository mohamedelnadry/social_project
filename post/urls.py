
from django.urls import path
from .views import PostView,PostCreateView,PostViewUpdatedelete, CommentView,DelateComment,UpdateComment,PostListByUser

urlpatterns = [
    path('', PostView.as_view(),name='ListView'),
    path('create/', PostCreateView.as_view(),name='CreateView'),
    path('createcomment/', CommentView.as_view(),name='Createcomment'),
    path('view/<int:id>/', PostViewUpdatedelete.as_view(),name='PostViewUpdatedelete'),
    path('deletecomment/<int:id>/', DelateComment.as_view(),name='deletecomment'),
    path('updatecomment/<int:id>/', UpdateComment.as_view(),name='updatecomment'),
    # path('userposts/<int:id>/', ViewUserPosts.as_view(),name='userposts'),
    path('users/<int:user_id>/posts/', PostListByUser.as_view(), name='post-list-by-user'),




]
