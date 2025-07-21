from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from api.filters import PersonFilter, PlanetsFilter, StarshipsFilter, SpeciesFilter, VehiclesFilter, FilmsFilter
from api.models import People, Planets, Starships, Species, Vehicles, Films
from api.paginators import GenericPagination
from api.serializers import PersonDetailSerializer, PlanetDetailSerializer, StarshipDetailSerializer, \
    SpeciesDetailSerializer, VehicleDetailSerializer, FilmDetailSerializer
from api.swagger.request_parameters import NAME_PARAMETER, TITLE_PARAMETER


class BaseStarWarsAPIView(ListModelMixin, GenericAPIView):
    """Generic base class for all Star Wars API views"""
    filter_backends = [DjangoFilterBackend]
    pagination_class = GenericPagination


class PeopleAPIView(BaseStarWarsAPIView):
    queryset = People.objects.all()
    serializer_class = PersonDetailSerializer
    filterset_class = PersonFilter

    @swagger_auto_schema(manual_parameters=[NAME_PARAMETER])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PlanetsAPIView(BaseStarWarsAPIView):
    queryset = Planets.objects.all()
    serializer_class = PlanetDetailSerializer
    filterset_class = PlanetsFilter

    @swagger_auto_schema(manual_parameters=[NAME_PARAMETER])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StarshipsAPIView(BaseStarWarsAPIView):
    queryset = Starships.objects.all()
    serializer_class = StarshipDetailSerializer
    filterset_class = StarshipsFilter

    @swagger_auto_schema(manual_parameters=[NAME_PARAMETER])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SpeciesAPIView(BaseStarWarsAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesDetailSerializer
    filterset_class = SpeciesFilter

    @swagger_auto_schema(manual_parameters=[NAME_PARAMETER])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class VehiclesAPIView(BaseStarWarsAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleDetailSerializer
    filterset_class = VehiclesFilter

    @swagger_auto_schema(manual_parameters=[NAME_PARAMETER])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FilmsAPIView(BaseStarWarsAPIView):
    queryset = Films.objects.all()
    serializer_class = FilmDetailSerializer
    filterset_class = FilmsFilter

    @swagger_auto_schema(manual_parameters=[TITLE_PARAMETER])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
