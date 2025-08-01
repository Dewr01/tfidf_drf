from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="TF-IDF API",
        default_version='v1',
        description="API for calculating TF-IDF values for documents",
        contact=openapi.Contact(email="your@email.com"),
    ),
    public=True,
)
