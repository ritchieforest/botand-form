# api/serializers.py

from rest_framework import serializers
from .models import Context, Label,LabelTrain,TrainData,SchemeByContext

class SchemeByContextSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    descripcion = serializers.CharField(max_length=255, allow_blank=True)
    contexto = serializers.CharField(max_length=255)
 
   
class LabelTrainSerializer(serializers.Serializer):
    start= serializers.IntegerField(required=True)
    end= serializers.IntegerField(required=True)
    label = serializers.CharField(max_length=255)

class TrainDataSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    context=serializers.CharField(max_length=255)
    text = serializers.CharField(max_length=255)
    labels = serializers.ListField(child=LabelTrainSerializer())


class ContextSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(max_length=255, allow_blank=True)

class LabelSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(max_length=255, allow_blank=True)
    contexto = serializers.CharField(max_length=255)
