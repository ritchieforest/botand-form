# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContextViewSet, LabelViewSet

router = DefaultRouter()
router.register(r'contextos', ContextViewSet, basename='contexto')
router.register(r'etiquetas', LabelViewSet, basename='etiqueta')

urlpatterns = [
    path('', include(router.urls)),
]
