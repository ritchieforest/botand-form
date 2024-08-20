# api/serializers.py

from rest_framework import serializers
from .models import Context, LabelByContext,SchemeByContext


class RefLabelSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    refString=serializers.CharField(max_length=255)
    labelByContext_id=serializers.CharField(max_length=255)

class SchemeByContextSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    descripcion = serializers.CharField(max_length=255, allow_blank=True)
    contexto = serializers.CharField(max_length=255)
    labels=serializers.ListField(child=RefLabelSerializer())
 
class ContextSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(max_length=255, allow_blank=True)

class LabelSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(max_length=255, allow_blank=True)
    contexto = serializers.CharField(max_length=255)
