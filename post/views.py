from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer,CommentSerializer
from .models import Post,Comment
from datetime import datetime
from accounts.permissions import IsAuthUser
# Create your views here.

from rest_framework import status



class PostListByUser(generics.ListAPIView):
    permission_classes = (IsAuthUser,)

    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(author=user_id)


    

class PostView(generics.ListAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        queryset = Post.objects.filter(created_at__lte = datetime.now()).order_by('-created_at')
        print(datetime.now())
        
        return queryset
    



class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = (IsAuthUser,)

class PostViewUpdatedelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthUser,)
    
    queryset = Post.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = PostSerializer
    permission_classes = (IsAuthUser,)

class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthUser,)



class DelateComment(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = CommentSerializer
    permission_classes = (IsAuthUser,)



    def destroy(self, request, *args, **kwargs):

        message = {'message': 'Comment deleted successfully'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)
    

class UpdateComment(generics.UpdateAPIView):
    permission_classes = (IsAuthUser,)

    queryset = Comment.objects.all()
    lookup_url_kwarg = 'id' 
    serializer_class = CommentSerializer



