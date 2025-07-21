# serializers.py
from django.db.models import Prefetch
from rest_framework import serializers
from .models import (
    Films, Planets, People, Species, Vehicles, Starships,
    Climates, Terrains, EyeColors, HairColors, SkinColors,
    StarshipClasses, StarshipManufacturers, VehicleClasses, VehicleManufacturers, PeopleEyeColors, PeopleHairColors,
    PeopleSkinColors
)


# =============================================================================
# SIMPLE/STATIC MODEL SERIALIZERS
# =============================================================================

class ClimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climates
        fields = ['id', 'name', 'description']


class TerrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terrains
        fields = ['id', 'name', 'description']


class EyeColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EyeColors
        fields = ['id', 'name', 'color']


class HairColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairColors
        fields = ['id', 'name', 'color']


class SkinColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkinColors
        fields = ['id', 'name', 'color']


class StarshipClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarshipClasses
        fields = ['id', 'name']


class StarshipManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarshipManufacturers
        fields = ['id', 'name']


class VehicleClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleClasses
        fields = ['id', 'name']


class VehicleManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleManufacturers
        fields = ['id', 'name']


# =============================================================================
# LIST/NESTED SERIALIZERS - Used for both lists and nested relationships
# =============================================================================

class FilmListSerializer(serializers.ModelSerializer):
    """List and nested Film serializer"""

    class Meta:
        model = Films
        fields = ['id', 'title', 'episode_id', 'director', 'producer', 'release_date']


class PlanetListSerializer(serializers.ModelSerializer):
    """List and nested Planet serializer"""
    climate = serializers.CharField(source='climate.description', allow_null=True)
    terrain = serializers.CharField(source='terrain.description', allow_null=True)

    class Meta:
        model = Planets
        fields = [
            'id', 'name', 'rotation_period', 'orbital_period', 'diameter',
            'climate', 'gravity', 'terrain', 'surface_water', 'population'
        ]


class PersonListSerializer(serializers.ModelSerializer):
    """List and nested Person serializer"""
    homeworld = serializers.CharField(source='homeworld.name', allow_null=True)
    eye_colors = serializers.SerializerMethodField()
    hair_colors = serializers.SerializerMethodField()
    skin_colors = serializers.SerializerMethodField()

    class Meta:
        model = People
        fields = [
            'id', 'name', 'height', 'mass', 'hair_colors', 'skin_colors',
            'eye_colors', 'birth_year', 'gender', 'homeworld'
        ]

    def get_eye_colors(self, obj):
        colors = obj.people_eye_colors.all()
        return [_.eye_color.color for _ in colors] if colors.exists() else []

    def get_hair_colors(self, obj):
        colors = obj.people_hair_colors.all()
        return [_.hair_color.color for _ in colors] if colors.exists() else []

    def get_skin_colors(self, obj):
        colors = obj.people_skin_colors.all()
        return [_.skin_color.color for _ in colors] if colors.exists() else []


class SpeciesListSerializer(serializers.ModelSerializer):
    """List and nested Species serializer"""
    homeworld = serializers.CharField(source='homeworld.name', allow_null=True)
    skin_colors = serializers.SerializerMethodField()
    hair_colors = serializers.SerializerMethodField()
    eye_colors = serializers.SerializerMethodField()

    class Meta:
        model = Species
        fields = [
            'id', 'name', 'classification', 'designation',
            'average_height', 'average_lifespan', 'homeworld', 'language',
            'skin_colors', 'hair_colors', 'eye_colors'
        ]

    def get_skin_colors(self, obj):
        colors = SkinColors.objects.filter(skin_color_species__species=obj)
        return [color.color for color in colors]

    def get_hair_colors(self, obj):
        colors = HairColors.objects.filter(hair_color_species__species=obj)
        return [color.color for color in colors]

    def get_eye_colors(self, obj):
        colors = EyeColors.objects.filter(eye_color_species__species=obj)
        return [color.color for color in colors]


class VehicleListSerializer(serializers.ModelSerializer):
    """List and nested Vehicle serializer"""
    vehicle_class = serializers.CharField(source='vehicle_class.name', allow_null=True)
    manufacturers = serializers.SerializerMethodField()

    class Meta:
        model = Vehicles
        fields = [
            'id', 'name', 'model', 'vehicle_class', 'length',
            'cost_in_credits', 'crew', 'passengers', 'manufacturers',
            'max_atmosphering_speed', 'cargo_capacity', 'consumables'
        ]

    def get_manufacturers(self, obj):
        manufacturers = VehicleManufacturers.objects.filter(
            manufacturer_vehicles__vehicle=obj
        )
        return [manufacturer.name for manufacturer in manufacturers]


class StarshipListSerializer(serializers.ModelSerializer):
    """List and nested Starship serializer"""
    starship_class = serializers.CharField(source='starship_class.name', allow_null=True)
    manufacturers = serializers.SerializerMethodField()

    class Meta:
        model = Starships
        fields = [
            'id', 'name', 'model', 'starship_class', 'length',
            'cost_in_credits', 'crew', 'passengers', 'hyperdrive_rating',
            'manufacturers', 'max_atmosphering_speed', 'cargo_capacity',
            'consumables', 'MGLT'
        ]

    def get_manufacturers(self, obj):
        manufacturers = StarshipManufacturers.objects.filter(
            manufacturer_starships__starship=obj
        )
        return [manufacturer.name for manufacturer in manufacturers]


# =============================================================================
# DETAILED RETRIEVE SERIALIZERS - WITH NESTED OBJECTS
# =============================================================================

class FilmDetailSerializer(serializers.ModelSerializer):
    """Detailed Film serializer with nested objects"""
    characters = serializers.SerializerMethodField()
    planets = serializers.SerializerMethodField()
    starships = serializers.SerializerMethodField()
    vehicles = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()

    class Meta:
        model = Films
        fields = [
            'id', 'title', 'episode_id', 'opening_crawl', 'director',
            'producer', 'release_date', 'characters', 'planets',
            'starships', 'vehicles', 'species', 'created', 'edited'
        ]

    def get_characters(self, obj):
        people = People.objects.filter(people_films__film=obj).select_related(
            'homeworld'
        ).prefetch_related(
            Prefetch(
                'people_eye_colors',
                queryset=PeopleEyeColors.objects.all()
            ),
            Prefetch(
                'people_hair_colors',
                queryset=PeopleHairColors.objects.all()
            ),
            Prefetch(
                'people_skin_colors',
                queryset=PeopleSkinColors.objects.all()
            )
        )
        return PersonListSerializer(people, many=True).data

    def get_planets(self, obj):
        planets = Planets.objects.filter(planet_films__film=obj).select_related(
            'climate', 'terrain'
        )
        return PlanetListSerializer(planets, many=True).data

    def get_starships(self, obj):
        starships = Starships.objects.filter(starship_films__film=obj).select_related(
            'starship_class'
        ).prefetch_related('starship_manufacturers__manufacturer')
        return StarshipListSerializer(starships, many=True).data

    def get_vehicles(self, obj):
        vehicles = Vehicles.objects.filter(vehicle_films__film=obj).select_related(
            'vehicle_class'
        ).prefetch_related('vehicle_manufacturers__manufacturer')
        return VehicleListSerializer(vehicles, many=True).data

    def get_species(self, obj):
        species = Species.objects.filter(species_films__film=obj).prefetch_related(
            'species_eye_colors__eye_color',
            'species_hair_colors__hair_color',
            'species_skin_colors__skin_color'
        )
        return SpeciesListSerializer(species, many=True).data


class PlanetDetailSerializer(serializers.ModelSerializer):
    """Detailed Planet serializer with nested objects"""
    climate = ClimateSerializer(read_only=True)
    terrain = TerrainSerializer(read_only=True)
    residents = serializers.SerializerMethodField()
    films = serializers.SerializerMethodField()

    class Meta:
        model = Planets
        fields = [
            'id', 'name', 'rotation_period', 'orbital_period', 'diameter',
            'climate', 'gravity', 'terrain', 'surface_water', 'population',
            'residents', 'films', 'created', 'edited'
        ]

    def get_residents(self, obj):
        residents = People.objects.filter(homeworld=obj).select_related(
            'homeworld'
        ).prefetch_related(
            Prefetch(
                'people_eye_colors',
                queryset=PeopleEyeColors.objects.all()
            ),
            Prefetch(
                'people_hair_colors',
                queryset=PeopleHairColors.objects.all()
            ),
            Prefetch(
                'people_skin_colors',
                queryset=PeopleSkinColors.objects.all()
            )
        )
        return PersonListSerializer(residents, many=True).data

    def get_films(self, obj):
        films = Films.objects.filter(film_planets__planet=obj)
        return FilmListSerializer(films, many=True).data


class PersonDetailSerializer(serializers.ModelSerializer):
    """Detailed Person serializer with nested objects"""
    homeworld = PlanetListSerializer(read_only=True)
    films = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()
    vehicles = serializers.SerializerMethodField()
    starships = serializers.SerializerMethodField()
    eye_colors = serializers.SerializerMethodField()
    hair_colors = serializers.SerializerMethodField()
    skin_colors = serializers.SerializerMethodField()

    class Meta:
        model = People
        fields = [
            'id', 'name', 'height', 'mass', 'hair_colors', 'skin_colors',
            'eye_colors', 'birth_year', 'gender', 'homeworld', 'films',
            'species', 'vehicles', 'starships', 'created', 'edited'
        ]

    def get_eye_colors(self, obj):
        colors = EyeColors.objects.filter(eye_color_people__person=obj)
        return [color.color for color in colors] if colors.exists() else []

    def get_hair_colors(self, obj):
        colors = HairColors.objects.filter(hair_color_people__person=obj)
        return [color.color for color in colors] if colors.exists() else []

    def get_skin_colors(self, obj):
        colors = SkinColors.objects.filter(skin_color_people__person=obj)
        return [color.color for color in colors] if colors.exists() else []

    def get_films(self, obj):
        films = Films.objects.filter(film_people__person=obj)
        return FilmListSerializer(films, many=True).data

    def get_species(self, obj):
        species = Species.objects.filter(species_people__person=obj).prefetch_related(
            'species_eye_colors__eye_color',
            'species_hair_colors__hair_color',
            'species_skin_colors__skin_color'
        )
        return SpeciesListSerializer(species, many=True).data

    def get_vehicles(self, obj):
        vehicles = Vehicles.objects.filter(vehicle_pilots__pilot=obj).select_related(
            'vehicle_class'
        ).prefetch_related('vehicle_manufacturers__manufacturer')
        return VehicleListSerializer(vehicles, many=True).data

    def get_starships(self, obj):
        starships = Starships.objects.filter(starship_pilots__pilot=obj).select_related(
            'starship_class'
        ).prefetch_related('starship_manufacturers__manufacturer')
        return StarshipListSerializer(starships, many=True).data


class SpeciesDetailSerializer(serializers.ModelSerializer):
    """Detailed Species serializer with nested objects"""
    homeworld = PlanetListSerializer(read_only=True)
    people = serializers.SerializerMethodField()
    films = serializers.SerializerMethodField()
    skin_colors = serializers.SerializerMethodField()
    hair_colors = serializers.SerializerMethodField()
    eye_colors = serializers.SerializerMethodField()

    class Meta:
        model = Species
        fields = [
            'id', 'name', 'classification', 'designation', 'average_height',
            'skin_colors', 'hair_colors', 'eye_colors', 'average_lifespan',
            'homeworld', 'language', 'people', 'films', 'created', 'edited'
        ]

    def get_people(self, obj):
        people = People.objects.filter(people_species__species=obj).select_related(
            'homeworld',
        ).prefetch_related(
            Prefetch(
                'people_eye_colors',
                queryset=PeopleEyeColors.objects.all()
            ),
            Prefetch(
                'people_hair_colors',
                queryset=PeopleHairColors.objects.all()
            ),
            Prefetch(
                'people_skin_colors',
                queryset=PeopleSkinColors.objects.all()
            )
        )
        return PersonListSerializer(people, many=True).data

    def get_films(self, obj):
        films = Films.objects.filter(film_species__species=obj)
        return FilmListSerializer(films, many=True).data

    def get_skin_colors(self, obj):
        colors = SkinColors.objects.filter(skin_color_species__species=obj)
        return [{"id": color.id, "name": color.name, "color": color.color} for color in colors]

    def get_hair_colors(self, obj):
        colors = HairColors.objects.filter(hair_color_species__species=obj)
        return [{"id": color.id, "name": color.name, "color": color.color} for color in colors]

    def get_eye_colors(self, obj):
        colors = EyeColors.objects.filter(eye_color_species__species=obj)
        return [{"id": color.id, "name": color.name, "color": color.color} for color in colors]


class VehicleDetailSerializer(serializers.ModelSerializer):
    """Detailed Vehicle serializer with nested objects"""
    vehicle_class = VehicleClassSerializer(read_only=True)
    manufacturers = serializers.SerializerMethodField()
    pilots = serializers.SerializerMethodField()
    films = serializers.SerializerMethodField()

    class Meta:
        model = Vehicles
        fields = [
            'id', 'name', 'model', 'manufacturers', 'cost_in_credits', 'length',
            'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity',
            'consumables', 'vehicle_class', 'pilots', 'films', 'created', 'edited'
        ]

    def get_manufacturers(self, obj):
        manufacturers = VehicleManufacturers.objects.filter(
            manufacturer_vehicles__vehicle=obj
        )
        return VehicleManufacturerSerializer(manufacturers, many=True).data

    def get_pilots(self, obj):
        pilots = People.objects.filter(piloted_vehicles__vehicle=obj).select_related(
            'homeworld'
        ).prefetch_related(
            Prefetch(
                'people_eye_colors',
                queryset=PeopleEyeColors.objects.all()
            ),
            Prefetch(
                'people_hair_colors',
                queryset=PeopleHairColors.objects.all()
            ),
            Prefetch(
                'people_skin_colors',
                queryset=PeopleSkinColors.objects.all()
            )
        )
        return PersonListSerializer(pilots, many=True).data

    def get_films(self, obj):
        films = Films.objects.filter(film_vehicles__vehicle=obj)
        return FilmListSerializer(films, many=True).data


class StarshipDetailSerializer(serializers.ModelSerializer):
    """Detailed Starship serializer with nested objects"""
    starship_class = StarshipClassSerializer(read_only=True)
    manufacturers = serializers.SerializerMethodField()
    pilots = serializers.SerializerMethodField()
    films = serializers.SerializerMethodField()

    class Meta:
        model = Starships
        fields = [
            'id', 'name', 'model', 'manufacturers', 'cost_in_credits', 'length',
            'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity',
            'consumables', 'hyperdrive_rating', 'MGLT', 'starship_class',
            'pilots', 'films', 'created', 'edited'
        ]

    def get_manufacturers(self, obj):
        manufacturers = StarshipManufacturers.objects.filter(
            manufacturer_starships__starship=obj
        )
        return StarshipManufacturerSerializer(manufacturers, many=True).data

    def get_pilots(self, obj):
        pilots = People.objects.filter(piloted_starships__starship=obj).select_related(
            'homeworld'
        ).prefetch_related(
            Prefetch(
                'people_eye_colors',
                queryset=PeopleEyeColors.objects.all()
            ),
            Prefetch(
                'people_hair_colors',
                queryset=PeopleHairColors.objects.all()
            ),
            Prefetch(
                'people_skin_colors',
                queryset=PeopleSkinColors.objects.all()
            )
        )
        return PersonListSerializer(pilots, many=True).data

    def get_films(self, obj):
        films = Films.objects.filter(film_starships__starship=obj)
        return FilmListSerializer(films, many=True).data


# =============================================================================
# LIST SERIALIZERS (For paginated lists) - Simple versions removed since they're the same as above
# =============================================================================


# =============================================================================
# UTILITY FUNCTIONS FOR VIEWS
# =============================================================================

def get_serializer_class_for_action(model_name, action):
    """
    Helper function to get appropriate serializer class based on action
    Usage in ViewSets:

    def get_serializer_class(self):
        return get_serializer_class_for_action('film', self.action)
    """
    serializer_map = {
        'film': {
            'list': FilmListSerializer,
            'retrieve': FilmDetailSerializer,
        },
        'planet': {
            'list': PlanetListSerializer,
            'retrieve': PlanetDetailSerializer,
        },
        'person': {
            'list': PersonListSerializer,
            'retrieve': PersonDetailSerializer,
        },
        'species': {
            'list': SpeciesListSerializer,
            'retrieve': SpeciesDetailSerializer,
        },
        'vehicle': {
            'list': VehicleListSerializer,
            'retrieve': VehicleDetailSerializer,
        },
        'starship': {
            'list': StarshipListSerializer,
            'retrieve': StarshipDetailSerializer,
        }
    }

    return serializer_map.get(model_name, {}).get(action, serializers.ModelSerializer)
