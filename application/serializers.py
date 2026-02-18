from rest_framework import serializers
from .models import Notes

class NotesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Notes
        fields = '__all__'