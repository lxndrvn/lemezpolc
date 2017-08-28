import os

from django.core.management import BaseCommand

from lemezpolc.jobs.read_releases import collect_releases
from lemezpolc.management.common import is_in_database

PATH = os.environ.get('LEMEZPOLC_DEFAULT_PATH')

class Command(BaseCommand):
    def handle(self, *args, **options):
        releases = collect_releases(PATH)
        for release in releases:
            if is_in_database(release):
                continue
            print(release.artist, release.title)
