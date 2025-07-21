from django.core.management import BaseCommand

from api.utils.download_data import fetch_swapi_data
from api.utils.parser import StarWarsParser


class Command(BaseCommand):
    help = 'Download and import Star Wars data'

    def handle(self, *args, **options):
        data = fetch_swapi_data()
        parser = StarWarsParser()
        parser.parse_json_data(data)