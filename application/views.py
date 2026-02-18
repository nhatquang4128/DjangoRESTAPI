from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Notes
from .serializers import NotesSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def notes_view(request):
    if request.method == 'GET':
        notes = Notes.objects.all()
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'error': 'User is not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
                )

        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def notes_detail_view(request, pk):
        try:
            notes = Notes.objects.get(pk=pk)
        except Notes.DoesNotExist:
            return Response(
                {'error': 'Note does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_authenticated:
            return Response(
                {'error': 'User is not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if notes.author != request.user:
            return Response(
                {'error': 'You must be the author to access this note'},
                status=status.HTTP_403_FORBIDDEN,
            )

        elif request.method == 'GET':
            serializer = NotesSerializer(notes)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = NotesSerializer(notes, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            notes.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)








