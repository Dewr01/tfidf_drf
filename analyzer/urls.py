from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, MainView
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('api/', include(router.urls)),
    path('upload/', TemplateView.as_view(template_name='analyzer/upload_form.html'), name='upload'),
]
