import time

from django.core.management import BaseCommand

from lemezpolc.config import DEFAULT_PATH
from lemezpolc.jobs.read_releases import collect_releases
from lemezpolc.jobs.resize_image import resize_image
from lemezpolc.jobs.scrape_discogs_data import extend_release
from lemezpolc.management.common import is_in_database
from lemezpolc.models import Release


class Command(BaseCommand):
    def handle(self, *args, **options):
        releases = collect_releases(DEFAULT_PATH)
        for release in releases:
            if not is_in_database(release):
                self.create_release(release)
                time.sleep(3)

    def create_release(self, release):
        release = extend_release(release)

        if not release.cover:
            print('No cover found for {0} - {1}'.format(release.artist, release.title))
            return

        release.cover = resize_image(release.cover, release.artist, release.title)
        Release.objects.create(artist=release.artist,
                               title=release.title,
                               year=int(release.year),
                               discogs_link=release.discogs_link,
                               cover=release.cover,
                               directory=release.directory,
                               release_format=release.release_format)
        print('Created release {0} - {1} - {2}'.format(
            release.artist, release.title, release.year))

