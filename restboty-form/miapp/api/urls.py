# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContextViewSet, LabelViewSet,SchemeByContextViewSet,StringProcessorViewSet

router = DefaultRouter()
router.register(r'contextos', ContextViewSet, basename='contexto')
router.register(r'etiquetas', LabelViewSet, basename='etiqueta')
router.register(r'esquema-por-contexto', SchemeByContextViewSet, basename='esquema-por-contexto')
router.register(r'text-processor', StringProcessorViewSet, basename='string-processor')


urlpatterns = [
    path('', include(router.urls)),
]
