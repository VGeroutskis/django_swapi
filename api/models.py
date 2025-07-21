from django.db import models
from api.utils import help_text

# =============================================================================
# ABSTRACT BASE CLASSES
# =============================================================================

class BaseModel(models.Model):
    """Abstract base class for common fields"""
    created = models.DateTimeField(
        auto_now_add=True,
        **help_text("The ISO 8601 date format of the time that this resource was created.")
    )

    edited = models.DateTimeField(
        auto_now=True,
        **help_text("The ISO 8601 date format of the time that this resource was edited.")
    )

    class Meta:
        abstract = True


class NamedModel(BaseModel):
    """Abstract base class for models with name field"""
    name = models.CharField(
        max_length=255,
        db_index=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

# =============================================================================
# STATIC MODELS
# =============================================================================

class StarshipClasses(NamedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = "Starship Class"
        verbose_name_plural = "Starship Classes"
        ordering = ['name']
        db_table = 'static_starship_classes'


class StarshipManufacturers(NamedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = "Starship Manufacturer"
        verbose_name_plural = "Starship Manufacturers"
        ordering = ['name']
        db_table = 'static_starship_manufacturers'


class VehicleClasses(NamedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = "Vehicle Class"
        verbose_name_plural = "Vehicle Classes"
        ordering = ['name']
        db_table = 'static_vehicle_classes'


class VehicleManufacturers(NamedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = "Vehicle Manufacturer"
        verbose_name_plural = "Vehicle Manufacturers"
        ordering = ['name']
        db_table = 'static_vehicle_manufacturers'


class Climates(NamedModel):
    description = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = "Climate"
        verbose_name_plural = "Climates"
        ordering = ['description']
        db_table = 'static_climates'

    def __str__(self):
        return self.description


class Terrains(NamedModel):
    description = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = "Terrain"
        verbose_name_plural = "Terrains"
        ordering = ['description']
        db_table = 'static_terrains'

    def __str__(self):
        return self.description


class EyeColors(NamedModel):
    color = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = "Eye Color"
        verbose_name_plural = "Eye Colors"
        ordering = ['color']
        db_table = 'static_eye_colors'

    def __str__(self):
        return self.color


class HairColors(NamedModel):
    color = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = "Hair Color"
        verbose_name_plural = "Hair Colors"
        ordering = ['color']
        db_table = 'static_hair_colors'

    def __str__(self):
        return self.color


class SkinColors(NamedModel):
    color = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = "Skin Color"
        verbose_name_plural = "Skin Colors"
        ordering = ['color']
        db_table = 'static_skin_colors'

    def __str__(self):
        return self.color

# =============================================================================
# FILMS RELATED MODELS
# =============================================================================

class Films(BaseModel):
    title = models.CharField(
        max_length=255,
        **help_text("The title of this film")
    )

    episode_id = models.IntegerField(
        **help_text("The episode number of this film.")
    )

    opening_crawl = models.TextField(
        **help_text("The opening paragraphs at the beginning of this film.")
    )

    director = models.CharField(
        max_length=255,
        **help_text("The name of the director of this film.")
    )

    producer = models.CharField(
        max_length=255,
        **help_text("The name(s) of the producer(s) of this film. Comma separated.")
    )

    release_date = models.DateField(
        **help_text("The ISO 8601 date format of film release at original creator country.")
    )

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Films"
        ordering = ['episode_id', 'title']
        db_table = 'api_films'

    def __str__(self):
        return self.title

    @property
    def url(self):
        return f"/api/films/{self.id}/"

# =============================================================================
# PLANETS RELATED MODELS
# =============================================================================

class Planets(NamedModel):
    name = models.CharField(
        max_length=255,
        db_index=True,
        **help_text("The name of this planet.")
    )

    rotation_period = models.CharField(
        max_length=50,
        default="0",
        **help_text("The number of standard hours it takes for this planet to complete a single rotation on its axis.")
    )

    orbital_period = models.CharField(
        max_length=50,
        default="0",
        **help_text(
            "The number of standard days it takes for this planet to complete a single orbit of its local star.")
    )

    diameter = models.CharField(
        max_length=50,
        default="0",
        **help_text("The diameter of this planet in kilometers.")
    )

    gravity = models.CharField(
        max_length=255,
        default="1",
        **help_text(
            "A number denoting the gravity of this planet, where '1' is normal or 1 standard G. '2' is twice or 2 standard Gs. '0.5' is half or 0.5 standard Gs.")
    )

    population = models.CharField(
        max_length=255,
        default="0",
        **help_text("The average population of sentient beings inhabiting this planet.")
    )

    surface_water = models.CharField(
        max_length=255,
        default="0",
        **help_text("The percentage of the planet surface that is naturally occurring water or bodies of water.")
    )

    climate = models.ForeignKey(
        Climates,
        on_delete=models.CASCADE,
        related_name="planets",
        null=True,
        blank=True,
        **help_text("The climate of this planet")
    )

    terrain = models.ForeignKey(
        Terrains,
        on_delete=models.CASCADE,
        related_name="planets",
        null=True,
        blank=True,
        **help_text("The terrain of this planet")
    )

    class Meta:
        verbose_name = "Planet"
        verbose_name_plural = "Planets"
        ordering = ['name']
        db_table = 'api_planets'

    @property
    def url(self):
        return f"/api/planets/{self.id}/"

# =============================================================================
# SPECIES RELATED MODELS
# =============================================================================

class Species(NamedModel):
    name = models.CharField(
        max_length=255,
        **help_text("The name of this species.")
    )

    classification = models.CharField(
        max_length=255,
        **help_text("The classification of this species, such as 'mammal' or 'reptile'.")
    )

    designation = models.CharField(
        max_length=255,
        **help_text("The designation of this species, such as 'sentient'.")
    )

    average_height = models.CharField(
        max_length=50,
        **help_text("The average height of this species in centimeters.")
    )

    average_lifespan = models.CharField(
        max_length=50,
        **help_text("The average lifespan of this species in years.")
    )

    language = models.CharField(
        max_length=255,
        **help_text("The language commonly spoken by this species.")
    )

    homeworld = models.ForeignKey(
        Planets,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="native_species",
        **help_text("The planet that this species originates from.")
    )

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"
        ordering = ['name']
        db_table = 'api_species'

    @property
    def url(self):
        return f"/api/species/{self.id}/"

# =============================================================================
# PEOPLE RELATED MODELS
# =============================================================================

class People(NamedModel):
    name = models.CharField(
        max_length=255,
        **help_text("The name of this person.")
    )

    birth_year = models.CharField(
        max_length=50,
        **help_text("The birth year of the person, using the in-universe standard of BBY or ABY.")
    )

    gender = models.CharField(
        max_length=50,
        **help_text("The gender of this person. Either 'Male', 'Female' or 'unknown', 'n/a'.")
    )

    height = models.CharField(
        max_length=50,
        **help_text("The height of the person in centimeters.")
    )

    mass = models.CharField(
        max_length=50,
        **help_text("The mass of the person in kilograms.")
    )

    homeworld = models.ForeignKey(
        Planets,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="residents",
        **help_text("The planet that this person was born on or inhabits.")
    )

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ['name']
        db_table = 'api_people'

    @property
    def url(self):
        return f"/api/people/{self.id}/"

# =============================================================================
# STARSHIPS RELATED MODELS
# =============================================================================

class Starships(NamedModel):
    name = models.CharField(
        max_length=255,
        **help_text("The name of this starship. The common name, such as 'Death Star'.")
    )

    model = models.CharField(
        max_length=255,
        **help_text(
            "The model or official name of this starship. Such as 'T-65 X-wing' or 'DS-1 Orbital Battle Station'.")
    )

    starship_class = models.ForeignKey(
        StarshipClasses,
        on_delete=models.CASCADE,
        related_name="starships",
        **help_text("The class of this starship, such as 'Starfighter' or 'Deep Space Mobile Battlestation'")
    )

    cost_in_credits = models.CharField(
        max_length=50,
        **help_text("The cost of this starship new, in galactic credits.")
    )

    length = models.CharField(
        max_length=50,
        **help_text("The length of this starship in meters.")
    )

    crew = models.CharField(
        max_length=50,
        **help_text("The number of personnel needed to run or pilot this starship.")
    )

    passengers = models.CharField(
        max_length=50,
        **help_text("The number of non-essential people this starship can transport.")
    )

    max_atmosphering_speed = models.CharField(
        max_length=50,
        **help_text("The maximum speed of this starship in the atmosphere.")
    )

    hyperdrive_rating = models.CharField(
        max_length=50,
        **help_text("The class of this starships hyperdrive.")
    )

    MGLT = models.CharField(
        max_length=50,
        **help_text("The Maximum number of Megalights this starship can travel in a standard hour.")
    )

    cargo_capacity = models.CharField(
        max_length=50,
        **help_text("The maximum number of kilograms that this starship can transport.")
    )

    consumables = models.CharField(
        max_length=255,
        **help_text(
            "The maximum length of time that this starship can provide consumables for its entire crew without having to resupply.")
    )

    class Meta:
        verbose_name = "Starship"
        verbose_name_plural = "Starships"
        ordering = ['name']
        db_table = 'api_starships'

    @property
    def url(self):
        return f"/api/starships/{self.id}/"

# =============================================================================
# VEHICLES RELATED MODELS
# =============================================================================

class Vehicles(NamedModel):
    name = models.CharField(
        max_length=255,
        **help_text("The name of this vehicle. The common name, such as 'Sand Crawler' or 'Speeder bike'.")
    )

    model = models.CharField(
        max_length=255,
        **help_text("The model or official name of this vehicle. Such as 'All-Terrain Attack Transport'.")
    )

    vehicle_class = models.ForeignKey(
        VehicleClasses,
        on_delete=models.CASCADE,
        related_name="vehicles",
        **help_text("The class of this vehicle, such as 'Wheeled' or 'Repulsorcraft'.")
    )

    length = models.CharField(
        max_length=50,
        **help_text("The length of this vehicle in meters.")
    )

    cost_in_credits = models.CharField(
        max_length=50,
        **help_text("The cost of this vehicle new, in Galactic Credits.")
    )

    crew = models.CharField(
        max_length=50,
        **help_text("The number of personnel needed to run or pilot this vehicle.")
    )

    passengers = models.CharField(
        max_length=50,
        **help_text("The number of non-essential people this vehicle can transport.")
    )

    max_atmosphering_speed = models.CharField(
        max_length=50,
        **help_text("The maximum speed of this vehicle in the atmosphere.")
    )

    cargo_capacity = models.CharField(
        max_length=50,
        **help_text("The maximum number of kilograms that this vehicle can transport.")
    )

    consumables = models.CharField(
        max_length=255,
        **help_text(
            "The maximum length of time that this vehicle can provide consumables for its entire crew without having to resupply.")
    )

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ['name']
        db_table = 'api_vehicles'

    @property
    def url(self):
        return f"/api/vehicles/{self.id}/"

# =============================================================================
# JUNCTION MODELS
# =============================================================================

class StarshipManufacturerRelations(BaseModel):
    starship = models.ForeignKey(
        Starships,
        on_delete=models.CASCADE,
        related_name="starship_manufacturers"
    )
    manufacturer = models.ForeignKey(
        StarshipManufacturers,
        on_delete=models.CASCADE,
        related_name="manufacturer_starships"
    )

    class Meta:
        unique_together = ('starship', 'manufacturer')
        verbose_name = "Starship Manufacturer"
        verbose_name_plural = "Starship Manufacturers"
        ordering = ['starship__name', 'manufacturer__name']
        db_table = 'relation_starship_manufacturers'


class StarshipFilms(BaseModel):
    starship = models.ForeignKey(
        Starships,
        on_delete=models.CASCADE,
        related_name="starship_films"
    )
    film = models.ForeignKey(
        Films,
        on_delete=models.CASCADE,
        related_name="film_starships"
    )

    class Meta:
        unique_together = ('starship', 'film')
        verbose_name = "Starship Film"
        verbose_name_plural = "Starship Films"
        ordering = ['film__episode_id', 'starship__name']
        db_table = 'relation_starship_films'


class StarshipPilots(BaseModel):
    starship = models.ForeignKey(
        Starships,
        on_delete=models.CASCADE,
        related_name="starship_pilots"
    )
    pilot = models.ForeignKey(
        People,
        on_delete=models.CASCADE,
        related_name="piloted_starships"
    )

    class Meta:
        unique_together = ('starship', 'pilot')
        verbose_name = "Starship Pilot"
        verbose_name_plural = "Starship Pilots"
        ordering = ['starship__name', 'pilot__name']
        db_table = 'relation_starship_pilots'


class VehicleManufacturerRelations(BaseModel):
    vehicle = models.ForeignKey(
        Vehicles,
        on_delete=models.CASCADE,
        related_name="vehicle_manufacturers"
    )
    manufacturer = models.ForeignKey(
        VehicleManufacturers,
        on_delete=models.CASCADE,
        related_name="manufacturer_vehicles"
    )

    class Meta:
        unique_together = ('vehicle', 'manufacturer')
        verbose_name = "Vehicle Manufacturer"
        verbose_name_plural = "Vehicle Manufacturers"
        ordering = ['vehicle__name', 'manufacturer__name']
        db_table = 'relation_vehicle_manufacturers'


class VehicleFilms(BaseModel):
    vehicle = models.ForeignKey(
        Vehicles,
        on_delete=models.CASCADE,
        related_name="vehicle_films"
    )
    film = models.ForeignKey(
        Films,
        on_delete=models.CASCADE,
        related_name="film_vehicles"
    )

    class Meta:
        unique_together = ('vehicle', 'film')
        verbose_name = "Vehicle Film"
        verbose_name_plural = "Vehicle Films"
        ordering = ['film__episode_id', 'vehicle__name']
        db_table = 'relation_vehicle_films'


class VehiclePilots(BaseModel):
    vehicle = models.ForeignKey(
        Vehicles,
        on_delete=models.CASCADE,
        related_name="vehicle_pilots"
    )
    pilot = models.ForeignKey(
        People,
        on_delete=models.CASCADE,
        related_name="piloted_vehicles"
    )

    class Meta:
        unique_together = ('vehicle', 'pilot')
        verbose_name = "Vehicle Pilot"
        verbose_name_plural = "Vehicle Pilots"
        ordering = ['vehicle__name', 'pilot__name']
        db_table = 'relation_vehicle_pilots'


class PlanetFilms(BaseModel):
    planet = models.ForeignKey(
        Planets,
        on_delete=models.CASCADE,
        related_name="planet_films"
    )
    film = models.ForeignKey(
        Films,
        on_delete=models.CASCADE,
        related_name="film_planets"
    )

    class Meta:
        unique_together = ('planet', 'film')
        verbose_name = "Planet Film"
        verbose_name_plural = "Planet Films"
        ordering = ['film__episode_id', 'planet__name']
        db_table = 'relation_planet_films'


class SpeciesEyeColors(BaseModel):
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="species_eye_colors"
    )
    eye_color = models.ForeignKey(
        EyeColors,
        on_delete=models.CASCADE,
        related_name="eye_color_species"
    )

    class Meta:
        unique_together = ('species', 'eye_color')
        verbose_name = "Species Eye Color"
        verbose_name_plural = "Species Eye Colors"
        ordering = ['species__name', 'eye_color__color']
        db_table = 'relation_species_eye_colors'


class SpeciesHairColors(BaseModel):
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="species_hair_colors"
    )
    hair_color = models.ForeignKey(
        HairColors,
        on_delete=models.CASCADE,
        related_name="hair_color_species"
    )

    class Meta:
        unique_together = ('species', 'hair_color')
        verbose_name = "Species Hair Color"
        verbose_name_plural = "Species Hair Colors"
        ordering = ['species__name', 'hair_color__color']
        db_table = 'relation_species_hair_colors'


class SpeciesSkinColors(BaseModel):
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="species_skin_colors"
    )
    skin_color = models.ForeignKey(
        SkinColors,
        on_delete=models.CASCADE,
        related_name="skin_color_species"
    )

    class Meta:
        unique_together = ('species', 'skin_color')
        verbose_name = "Species Skin Color"
        verbose_name_plural = "Species Skin Colors"
        ordering = ['species__name', 'skin_color__color']
        db_table = 'relation_species_skin_colors'


class SpeciesFilms(BaseModel):
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="species_films"
    )
    film = models.ForeignKey(
        Films,
        on_delete=models.CASCADE,
        related_name="film_species"
    )

    class Meta:
        unique_together = ('species', 'film')
        verbose_name = "Species Film"
        verbose_name_plural = "Species Films"
        ordering = ['film__episode_id', 'species__name']
        db_table = 'relation_species_films'


class PeopleFilms(BaseModel):
    person = models.ForeignKey(
        People,
        on_delete=models.CASCADE,
        related_name="people_films"
    )
    film = models.ForeignKey(
        Films,
        on_delete=models.CASCADE,
        related_name="film_people"
    )

    class Meta:
        unique_together = ('person', 'film')
        verbose_name = "People Film"
        verbose_name_plural = "People Films"
        ordering = ['film__episode_id', 'person__name']
        db_table = 'relation_people_films'


class PeopleSpecies(BaseModel):
    person = models.ForeignKey(
        People,
        on_delete=models.CASCADE,
        related_name="people_species"
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="species_people"
    )

    class Meta:
        unique_together = ('person', 'species')
        verbose_name = "People Species"
        verbose_name_plural = "People Species"
        ordering = ['person__name', 'species__name']
        db_table = 'relation_people_species'


# =============================================================================
# PEOPLE COLORS JUNCTION MODELS
# =============================================================================

class PeopleEyeColors(BaseModel):
    person = models.ForeignKey(
        People,
        on_delete=models.CASCADE,
        related_name="people_eye_colors"
    )
    eye_color = models.ForeignKey(
        EyeColors,
        on_delete=models.CASCADE,
        related_name="eye_color_people"
    )

    class Meta:
        unique_together = ('person', 'eye_color')
        verbose_name = "People Eye Color"
        verbose_name_plural = "People Eye Colors"
        ordering = ['person__name', 'eye_color__color']
        db_table = 'relation_people_eye_colors'


class PeopleHairColors(BaseModel):
    person = models.ForeignKey(
        People,
        on_delete=models.CASCADE,
        related_name="people_hair_colors"
    )
    hair_color = models.ForeignKey(
        HairColors,
        on_delete=models.CASCADE,
        related_name="hair_color_people"
    )

    class Meta:
        unique_together = ('person', 'hair_color')
        verbose_name = "People Hair Color"
        verbose_name_plural = "People Hair Colors"
        ordering = ['person__name', 'hair_color__color']
        db_table = 'relation_people_hair_colors'


class PeopleSkinColors(BaseModel):
    person = models.ForeignKey(
        People,
        on_delete=models.CASCADE,
        related_name="people_skin_colors"
    )
    skin_color = models.ForeignKey(
        SkinColors,
        on_delete=models.CASCADE,
        related_name="skin_color_people"
    )

    class Meta:
        unique_together = ('person', 'skin_color')
        verbose_name = "People Skin Color"
        verbose_name_plural = "People Skin Colors"
        ordering = ['person__name', 'skin_color__color']
        db_table = 'relation_people_skin_colors'