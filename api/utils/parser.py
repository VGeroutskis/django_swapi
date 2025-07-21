# star_wars_parser.py
import json
import re
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import (  # Replace 'your_app' with your actual app name
    Films, Planets, People, Species, Vehicles, Starships,
    Climates, Terrains, EyeColors, HairColors, SkinColors,
    StarshipClasses, StarshipManufacturers, VehicleClasses, VehicleManufacturers,
    # Junction models
    PlanetFilms, PeopleFilms, PeopleSpecies, SpeciesFilms, SpeciesEyeColors,
    SpeciesHairColors, SpeciesSkinColors, VehicleFilms, VehiclePilots,
    VehicleManufacturerRelations, StarshipFilms, StarshipPilots,
    StarshipManufacturerRelations, PeopleEyeColors, PeopleHairColors, PeopleSkinColors
)


class StarWarsParser:
    """Parser for Star Wars API JSON data compatible with Django models"""

    def __init__(self):
        self.url_to_id_cache = {}
        self.created_objects = {
            'films': {},
            'planets': {},
            'people': {},
            'species': {},
            'vehicles': {},
            'starships': {},
        }

    def parse_json_file(self, file_path):
        """Parse JSON file and populate database"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with transaction.atomic():
            print("Starting Star Wars data import...")

            # Parse in order of dependencies
            self.parse_films(data.get('films', []))
            self.parse_planets(data.get('planets', []))
            self.parse_species(data.get('species', []))
            self.parse_people(data.get('people', []))
            self.parse_vehicles(data.get('vehicles', []))
            self.parse_starships(data.get('starships', []))

            # Create relationships after all objects exist
            self.create_relationships(data)

            print("Star Wars data import completed successfully!")

    def parse_json_string(self, json_string):
        """Parse JSON string and populate database"""
        data = json.loads(json_string)
        return self.parse_json_data(data)

    def parse_json_data(self, data):
        """Parse JSON data dict and populate database"""
        with transaction.atomic():
            print("Starting Star Wars data import...")

            # Parse in order of dependencies
            self.parse_films(data.get('films', []))
            self.parse_planets(data.get('planets', []))
            self.parse_species(data.get('species', []))
            self.parse_people(data.get('people', []))
            self.parse_vehicles(data.get('vehicles', []))
            self.parse_starships(data.get('starships', []))

            # Create relationships after all objects exist
            self.create_relationships(data)

            print("Star Wars data import completed successfully!")

    # Utility Methods
    def extract_id_from_url(self, url):
        """Extract ID from SWAPI URL"""
        if not url:
            return None
        match = re.search(r'/(\d+)/?$', url)
        return int(match.group(1)) if match else None

    def split_comma_separated(self, value):
        """Split comma-separated string into list"""
        if not value or value.lower() in ['unknown', 'n/a', 'none']:
            return []

        # Clean the value first
        value = value.strip()

        # Split by comma and clean each item
        items = [item.strip() for item in value.split(',') if item.strip()]

        # If no comma found, return the single value as list
        if len(items) == 1 and ',' not in value:
            return items

        # Filter out empty items after cleaning
        return [item for item in items if item and item.lower() not in ['unknown', 'n/a', 'none']]

    def get_or_create_simple_model(self, model_class, name, field_name='name'):
        """Get or create simple models like Colors, Classes etc."""
        if not name or name.lower() in ['unknown', 'n/a', 'none']:
            return None

        kwargs = {field_name: name.strip()}
        obj, created = model_class.objects.get_or_create(**kwargs)
        return obj

    def get_or_create_climate_terrain(self, model_class, description):
        """Get or create Climate or Terrain with description field"""
        if not description or description.lower() in ['unknown', 'n/a', 'none']:
            # Create default "unknown" entry instead of returning None
            obj, created = model_class.objects.get_or_create(
                description='unknown',
                defaults={'name': 'unknown'}
            )
            return obj

        obj, created = model_class.objects.get_or_create(
            description=description.strip(),
            defaults={'name': description.strip()}  # NamedModel requires name
        )
        return obj

    def safe_date_parse(self, date_string):
        """Safely parse date string"""
        if not date_string:
            return None
        try:
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            return None

    def safe_int_parse(self, value):
        """Safely parse integer"""
        if not value or str(value).lower() in ['unknown', 'n/a']:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    # Parsing Methods
    def parse_films(self, films_data):
        """Parse films data"""
        print("Parsing films...")
        for film_data in films_data:
            film_id = self.extract_id_from_url(film_data['url'])

            film, created = Films.objects.get_or_create(
                id=film_id,
                defaults={
                    'title': film_data['title'],
                    'episode_id': film_data['episode_id'],
                    'opening_crawl': film_data['opening_crawl'],
                    'director': film_data['director'],
                    'producer': film_data['producer'],
                    'release_date': self.safe_date_parse(film_data['release_date']),
                }
            )

            self.created_objects['films'][film_data['url']] = film
            if created:
                print(f"Created film: {film.title}")

    def parse_planets(self, planets_data):
        """Parse planets data"""
        print("Parsing planets...")
        for planet_data in planets_data:
            planet_id = self.extract_id_from_url(planet_data['url'])

            # Get or create climate and terrain
            climate = self.get_or_create_climate_terrain(Climates, planet_data['climate'])
            terrain = self.get_or_create_climate_terrain(Terrains, planet_data['terrain'])

            planet, created = Planets.objects.get_or_create(
                id=planet_id,
                defaults={
                    'name': planet_data['name'],
                    'rotation_period': planet_data.get('rotation_period', '0'),
                    'orbital_period': planet_data.get('orbital_period', '0'),
                    'diameter': planet_data.get('diameter', '0'),
                    'gravity': planet_data.get('gravity', '1'),
                    'surface_water': planet_data.get('surface_water', '0'),
                    'population': planet_data.get('population', '0'),
                    'climate': climate,
                    'terrain': terrain,
                }
            )

            self.created_objects['planets'][planet_data['url']] = planet
            if created:
                print(f"Created planet: {planet.name}")

    def parse_species(self, species_data_list):
        """Parse species data"""
        print("Parsing species...")
        for species_data in species_data_list:
            species_id = self.extract_id_from_url(species_data['url'])

            # Get homeworld if exists
            homeworld = None
            if species_data.get('homeworld'):
                homeworld = self.created_objects['planets'].get(species_data['homeworld'])

            species, created = Species.objects.get_or_create(
                id=species_id,
                defaults={
                    'name': species_data['name'],
                    'classification': species_data.get('classification', ''),
                    'designation': species_data.get('designation', ''),
                    'average_height': species_data.get('average_height', ''),
                    'average_lifespan': species_data.get('average_lifespan', ''),
                    'language': species_data.get('language', ''),
                    'homeworld': homeworld,
                }
            )

            # Handle colors (many-to-many through junction tables)
            if created:
                self._create_species_colors(species, species_data)

            self.created_objects['species'][species_data['url']] = species
            if created:
                print(f"Created species: {species.name}")

    def _create_species_colors(self, species, species_data):
        """Create species color relationships"""
        # Eye colors
        eye_colors = self.split_comma_separated(species_data.get('eye_colors', ''))
        for color_name in eye_colors:
            eye_color = self.get_or_create_simple_model(EyeColors, color_name, 'color')
            if eye_color:
                SpeciesEyeColors.objects.get_or_create(
                    species=species,
                    eye_color=eye_color
                )

        # Hair colors
        hair_colors = self.split_comma_separated(species_data.get('hair_colors', ''))
        for color_name in hair_colors:
            hair_color = self.get_or_create_simple_model(HairColors, color_name, 'color')
            if hair_color:
                SpeciesHairColors.objects.get_or_create(
                    species=species,
                    hair_color=hair_color
                )

        # Skin colors
        skin_colors = self.split_comma_separated(species_data.get('skin_colors', ''))
        for color_name in skin_colors:
            skin_color = self.get_or_create_simple_model(SkinColors, color_name, 'color')
            if skin_color:
                SpeciesSkinColors.objects.get_or_create(
                    species=species,
                    skin_color=skin_color
                )

    def parse_people(self, people_data):
        """Parse people data"""
        print("Parsing people...")
        for person_data in people_data:
            person_id = self.extract_id_from_url(person_data['url'])

            # Get related objects
            homeworld = None
            if person_data.get('homeworld'):
                homeworld = self.created_objects['planets'].get(person_data['homeworld'])

            person, created = People.objects.get_or_create(
                id=person_id,
                defaults={
                    'name': person_data['name'],
                    'birth_year': person_data.get('birth_year', ''),
                    'gender': person_data.get('gender', ''),
                    'height': person_data.get('height', ''),
                    'mass': person_data.get('mass', ''),
                    'homeworld': homeworld,
                }
            )

            # Create junction table relationships for multiple colors
            if created:
                self._create_people_colors(person, person_data)

            self.created_objects['people'][person_data['url']] = person
            if created:
                print(f"Created person: {person.name}")

    def _create_people_colors(self, person, person_data):
        """Create people color relationships for multiple colors"""
        # Eye colors
        eye_colors = self.split_comma_separated(person_data.get('eye_color', ''))

        for color_name in eye_colors:
            eye_color = self.get_or_create_simple_model(EyeColors, color_name, 'color')
            if eye_color:
                PeopleEyeColors.objects.get_or_create(
                    person=person,
                    eye_color=eye_color
                )

        # Hair colors
        hair_colors = self.split_comma_separated(person_data.get('hair_color', ''))

        for color_name in hair_colors:
            hair_color = self.get_or_create_simple_model(HairColors, color_name, 'color')
            if hair_color:
                PeopleHairColors.objects.get_or_create(
                    person=person,
                    hair_color=hair_color
                )

        # Skin colors
        skin_colors = self.split_comma_separated(person_data.get('skin_color', ''))

        for color_name in skin_colors:
            skin_color = self.get_or_create_simple_model(SkinColors, color_name, 'color')
            if skin_color:
                PeopleSkinColors.objects.get_or_create(
                    person=person,
                    skin_color=skin_color
                )

    def parse_vehicles(self, vehicles_data):
        """Parse vehicles data"""
        print("Parsing vehicles...")
        for vehicle_data in vehicles_data:
            vehicle_id = self.extract_id_from_url(vehicle_data['url'])

            # Get vehicle class
            vehicle_class = self.get_or_create_simple_model(
                VehicleClasses,
                vehicle_data.get('vehicle_class')
            )

            vehicle, created = Vehicles.objects.get_or_create(
                id=vehicle_id,
                defaults={
                    'name': vehicle_data['name'],
                    'model': vehicle_data.get('model', ''),
                    'vehicle_class': vehicle_class,
                    'length': vehicle_data.get('length', ''),
                    'cost_in_credits': vehicle_data.get('cost_in_credits', ''),
                    'crew': vehicle_data.get('crew', ''),
                    'passengers': vehicle_data.get('passengers', ''),
                    'max_atmosphering_speed': vehicle_data.get('max_atmosphering_speed', ''),
                    'cargo_capacity': vehicle_data.get('cargo_capacity', ''),
                    'consumables': vehicle_data.get('consumables', ''),
                }
            )

            # Handle manufacturers
            if created:
                self._create_vehicle_manufacturers(vehicle, vehicle_data)

            self.created_objects['vehicles'][vehicle_data['url']] = vehicle
            if created:
                print(f"Created vehicle: {vehicle.name}")

    def _create_vehicle_manufacturers(self, vehicle, vehicle_data):
        """Create vehicle manufacturer relationships"""
        manufacturers = self.split_comma_separated(vehicle_data.get('manufacturer', ''))
        for manufacturer_name in manufacturers:
            manufacturer = self.get_or_create_simple_model(VehicleManufacturers, manufacturer_name)
            if manufacturer:
                VehicleManufacturerRelations.objects.get_or_create(
                    vehicle=vehicle,
                    manufacturer=manufacturer
                )

    def parse_starships(self, starships_data):
        """Parse starships data"""
        print("Parsing starships...")
        for starship_data in starships_data:
            starship_id = self.extract_id_from_url(starship_data['url'])

            # Get starship class
            starship_class = self.get_or_create_simple_model(
                StarshipClasses,
                starship_data.get('starship_class')
            )

            starship, created = Starships.objects.get_or_create(
                id=starship_id,
                defaults={
                    'name': starship_data['name'],
                    'model': starship_data.get('model', ''),
                    'starship_class': starship_class,
                    'cost_in_credits': starship_data.get('cost_in_credits', ''),
                    'length': starship_data.get('length', ''),
                    'crew': starship_data.get('crew', ''),
                    'passengers': starship_data.get('passengers', ''),
                    'max_atmosphering_speed': starship_data.get('max_atmosphering_speed', ''),
                    'hyperdrive_rating': starship_data.get('hyperdrive_rating', ''),
                    'MGLT': starship_data.get('MGLT', ''),
                    'cargo_capacity': starship_data.get('cargo_capacity', ''),
                    'consumables': starship_data.get('consumables', ''),
                }
            )

            # Handle manufacturers
            if created:
                self._create_starship_manufacturers(starship, starship_data)

            self.created_objects['starships'][starship_data['url']] = starship
            if created:
                print(f"Created starship: {starship.name}")

    def _create_starship_manufacturers(self, starship, starship_data):
        """Create starship manufacturer relationships"""
        manufacturers = self.split_comma_separated(starship_data.get('manufacturer', ''))
        for manufacturer_name in manufacturers:
            manufacturer = self.get_or_create_simple_model(StarshipManufacturers, manufacturer_name)
            if manufacturer:
                StarshipManufacturerRelations.objects.get_or_create(
                    starship=starship,
                    manufacturer=manufacturer
                )

    def create_relationships(self, data):
        """Create all many-to-many relationships after objects are created"""
        print("Creating relationships...")

        # Planet-Film relationships
        for planet_data in data.get('planets', []):
            planet = self.created_objects['planets'].get(planet_data['url'])
            if planet:
                for film_url in planet_data.get('films', []):
                    film = self.created_objects['films'].get(film_url)
                    if film:
                        PlanetFilms.objects.get_or_create(planet=planet, film=film)

        # People relationships
        for person_data in data.get('people', []):
            person = self.created_objects['people'].get(person_data['url'])
            if person:
                # People-Films
                for film_url in person_data.get('films', []):
                    film = self.created_objects['films'].get(film_url)
                    if film:
                        PeopleFilms.objects.get_or_create(person=person, film=film)

                # People-Species
                for species_url in person_data.get('species', []):
                    species = self.created_objects['species'].get(species_url)
                    if species:
                        PeopleSpecies.objects.get_or_create(person=person, species=species)

                # Vehicle Pilots
                for vehicle_url in person_data.get('vehicles', []):
                    vehicle = self.created_objects['vehicles'].get(vehicle_url)
                    if vehicle:
                        VehiclePilots.objects.get_or_create(vehicle=vehicle, pilot=person)

                # Starship Pilots
                for starship_url in person_data.get('starships', []):
                    starship = self.created_objects['starships'].get(starship_url)
                    if starship:
                        StarshipPilots.objects.get_or_create(starship=starship, pilot=person)

        # Species-Films relationships
        for species_data in data.get('species', []):
            species = self.created_objects['species'].get(species_data['url'])
            if species:
                for film_url in species_data.get('films', []):
                    film = self.created_objects['films'].get(film_url)
                    if film:
                        SpeciesFilms.objects.get_or_create(species=species, film=film)

        # Vehicle-Films relationships
        for vehicle_data in data.get('vehicles', []):
            vehicle = self.created_objects['vehicles'].get(vehicle_data['url'])
            if vehicle:
                for film_url in vehicle_data.get('films', []):
                    film = self.created_objects['films'].get(film_url)
                    if film:
                        VehicleFilms.objects.get_or_create(vehicle=vehicle, film=film)

        # Starship-Films relationships
        for starship_data in data.get('starships', []):
            starship = self.created_objects['starships'].get(starship_data['url'])
            if starship:
                for film_url in starship_data.get('films', []):
                    film = self.created_objects['films'].get(film_url)
                    if film:
                        StarshipFilms.objects.get_or_create(starship=starship, film=film)

        print("All relationships created successfully!")
