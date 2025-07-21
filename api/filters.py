from django_filters import FilterSet, filters

from api.models import People, Starships, Planets, Species, Vehicles, Films


class FilterByNameMixin(FilterSet):
    name = filters.CharFilter(method='search_name')

    def search_name(self, queryset, name, value):
        if value:
            return queryset.filter(name__icontains=value)
        return queryset


class FilterByTitleMixin(FilterSet):
    title = filters.CharFilter(method='search_title')

    def search_title(self, queryset, name, value):
        if value:
            return queryset.filter(title__icontains=value)
        return queryset


class PersonFilter(FilterByNameMixin):
    class Meta:
        model = People
        fields = ['name']


class StarshipsFilter(FilterByNameMixin):
    class Meta:
        model = Starships
        fields = ['name']


class PlanetsFilter(FilterByNameMixin):
    class Meta:
        model = Planets
        fields = ['name']


class SpeciesFilter(FilterByNameMixin):
    class Meta:
        model = Species
        fields = ['name']


class VehiclesFilter(FilterByNameMixin):
    class Meta:
        model = Vehicles
        fields = ['name']


class FilmsFilter(FilterByTitleMixin):
    class Meta:
        model = Films
        fields = ['title']
