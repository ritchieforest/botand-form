# api/serializers.py

from rest_framework import serializers
from .models import Context, Label

class ContextSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(max_length=255, allow_blank=True)

class LabelSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(max_length=255, allow_blank=True)
    contexto = serializers.CharField(max_length=255)
