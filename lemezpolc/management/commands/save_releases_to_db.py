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
        try:
            updated_release = get_release_data(release)
            Release.objects.create(artist=updated_release.get('artist'),
                                   title=updated_release.get('title'),
                                   year=updated_release.get('year'),
                                   discogs_link=updated_release.get('discogs_link'),
                                   cover=updated_release.get('cover'),
                                   directory=updated_release.get('directory'),
                                   format=updated_release.get('format'))
            print('Created release {0} - {1} - {2}'.format(
                updated_release['artist'], updated_release['title'], updated_release['year']))
        except:
            pass

    def is_in_database(self, release):
        db_record = Release.objects.filter(artist=release['artist'], title=release['title'])
        return db_record.exists()
