import time

from django.core.management import BaseCommand

from lemezpolc.config import DEFAULT_PATH
from lemezpolc.jobs.read_releases import collect_releases
from lemezpolc.jobs.scrape_discogs_data import get_release_data
from lemezpolc.models import Release


class Command(BaseCommand):
    def handle(self, *args, **options):
        releases = collect_releases(DEFAULT_PATH)
        for release in releases:
            if not self.is_in_database(release):
                self.create_release(release)
                time.sleep(3)

    def create_release(self, release):
        release = get_release_data(release)
        Release.objects.create(artist=release.artist,
                               title=release.title,
                               year=release.year,
                               discogs_link=release.discogs_link,
                               cover=release.cover,
                               directory=release.directory,
                               format=release.format)
        print('Created release {0} - {1} - {2}'.format(
            release.artist, release.title, release.year))

    def is_in_database(self, release):
        db_record = Release.objects.filter(artist=release.artist, title=release.title)
        return db_record.exists()
