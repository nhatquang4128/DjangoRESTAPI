from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication Credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(
            {'error': 'Post not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {'detail': 'Authentication Credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if post.author != request.user:
        return Response(
            {'detail': 'You are not the author of this post.'},
            status=status.HTTP_403_FORBIDDEN
        )
    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method =='DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



