# api/views.py

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Context, Label
from .serializers import ContextSerializer, LabelSerializer

class ContextViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Context.objects.all()
        serializer = ContextSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        contexto = Context.objects(pk=pk).first()
        serializer = ContextSerializer(contexto)
        return Response(serializer.data)

    def create(self, request):
        serializer = ContextSerializer(data=request.data)
        if serializer.is_valid():
            contexto = Context(
                nombre=serializer.validated_data['nombre'],
                descripcion=serializer.validated_data.get('descripcion', '')
            )
            contexto.save()
            return Response(ContextSerializer(contexto).data)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        contexto = Context.objects(pk=pk).first()
        serializer = ContextSerializer(contexto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(contexto, serializer.validated_data)
            return Response(ContextSerializer(contexto).data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        contexto = Context.objects(pk=pk).first()
        contexto.delete()
        return Response(status=204)

class LabelViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Label.objects.all()
        serializer = LabelSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        etiqueta = Label.objects(pk=pk).first()
        serializer = LabelSerializer(etiqueta)
        return Response(serializer.data)

    def create(self, request):
        contexto_id = request.data.get('contexto')
        contexto = Context.objects(pk=contexto_id).first()
        if not contexto:
            return Response({'error': 'Contexto no encontrado'}, status=400)

        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            etiqueta = Label(
                nombre=serializer.validated_data['nombre'],
                descripcion=serializer.validated_data.get('descripcion', ''),
                contexto=contexto
            )
            etiqueta.save()
            return Response(LabelSerializer(etiqueta).data)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        etiqueta = Label.objects(pk=pk).first()
        contexto_id = request.data.get('contexto')
        contexto = Context.objects(pk=contexto_id).first()
        if not contexto:
            return Response({'error': 'Contexto no encontrado'}, status=400)

        serializer = LabelSerializer(etiqueta, data=request.data, partial=True)
        if serializer.is_valid():
            etiqueta.nombre = serializer.validated_data.get('nombre', etiqueta.nombre)
            etiqueta.descripcion = serializer.validated_data.get('descripcion', etiqueta.descripcion)
            etiqueta.contexto = contexto
            etiqueta.save()
            return Response(LabelSerializer(etiqueta).data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        etiqueta = Label.objects(pk=pk).first()
        etiqueta.delete()
        return Response(status=204)
