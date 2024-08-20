# api/views.py

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Context, LabelByContext,SchemeByContext,LabelsRefs
from .serializers import ContextSerializer, LabelSerializer,SchemeByContextSerializer
from rest_framework.decorators import action
from rest_framework import status
from .utils import TextComparer

class SchemeByContextViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = SchemeByContext.objects.all()
        serializer = SchemeByContextSerializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request):
        serializer = SchemeByContextSerializer(data=request.data)
        if serializer.is_valid():
            labels_data = serializer.validated_data['labels']
            # Crear una lista de objetos LabelTrain
            labels = [LabelsRefs(**label_data) for label_data in labels_data]
            contexto = SchemeByContext(
                descripcion=serializer.validated_data.get('descripcion', ''),
                contexto=serializer.validated_data.get('contexto', ''),
                labels=labels
            )
            contexto.save()
            return Response(SchemeByContextSerializer(contexto).data)
        return Response(serializer.errors, status=400)

class StringProcessorViewSet(viewsets.ViewSet):
 
    @action(detail=False, methods=['POST'])
    def process(self, request):
        # Obtener la cadena del cuerpo de la solicitud POST
        textCom=TextComparer()
        cadena = request.data.get('text', '')
        contexto=request.data.get("contexto",'')
        context_ids = Context.objects(nombre=contexto).only('id')
        resultados = SchemeByContext.objects(contexto__in=context_ids)
        response=textCom.calculate_similarity_arr(textComparer=cadena,textArr=resultados)
        
        # Iterar sobre los resultados
        if cadena:
            # Procesar la cadena (por ejemplo, convertirla a mayúsculas)
            processed_string = cadena.upper()
            return Response({"text": processed_string,"response_form":response,"contexto":contexto}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No se proporcionó ninguna cadena."}, status=status.HTTP_400_BAD_REQUEST)


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
        queryset = LabelByContext.objects.all()
        serializer = LabelSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        etiqueta = LabelByContext.objects(pk=pk).first()
        serializer = LabelSerializer(etiqueta)
        return Response(serializer.data)

    def create(self, request):
        contexto_id = request.data.get('contexto')
        contexto = Context.objects(pk=contexto_id).first()
        if not contexto:
            return Response({'error': 'Contexto no encontrado'}, status=400)

        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            etiqueta = LabelByContext(
                nombre=serializer.validated_data['nombre'],
                descripcion=serializer.validated_data.get('descripcion', ''),
                contexto=contexto
            )
            etiqueta.save()
            return Response(LabelSerializer(etiqueta).data)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        etiqueta = LabelSerializer.objects(pk=pk).first()
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
        etiqueta = LabelByContext.objects(pk=pk).first()
        etiqueta.delete()
        return Response(status=204)
