from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='analyzer/main.html'), name='main'),
    path('api/', include('analyzer.api.ursl')),  # API endpoints
    path('upload/', TemplateView.as_view(template_name='analyzer/upload_form.html'), name='upload'),
]
