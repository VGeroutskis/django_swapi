from django.conf import settings
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api import views

app_name = "api"

SchemaView = get_schema_view(
    openapi.Info(
        title="Star Wars API",
        default_version='v1',
        description="A Star Wars API with all your favorite characters, planets, starships and more!",
        contact=openapi.Contact(email="v.geroutskis@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path(
        'people/',
        views.PeopleAPIView.as_view(),
        name='people',
    ),
    path(
        'films/',
        views.FilmsAPIView.as_view(),
        name='films',
    ),
    path(
        'starships/',
        views.StarshipsAPIView.as_view(),
        name='starships',
    ),
    path(
        'species/',
        views.SpeciesAPIView.as_view(),
        name='species',
    ),
    path(
        'planets/',
        views.PlanetsAPIView.as_view(),
        name='planets',
    ),
    path(
        'vehicles/',
        views.VehiclesAPIView.as_view(),
        name='vehicles',
    ),
]

if settings.ENABLE_SWAGGER:
    urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            SchemaView.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            SchemaView.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            SchemaView.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
