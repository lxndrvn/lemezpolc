from django.core.management import BaseCommand

from lemezpolc.config import PATH
from lemezpolc.jobs.read_releases import collect_releases
from lemezpolc.jobs.resize_image import resize_image
from lemezpolc.models import Release


class Command(BaseCommand):
    def handle(self, *args, **options):
        releases = collect_releases(PATH)
        for release in releases:
            cover = release['cover']
            artist = release['artist']
            title = release['title']
            if cover:
                try:
                    db_release = Release.objects.get(artist=artist, title=title)
                    image_path = resize_image(cover, artist, title)
                    db_release.cover_path = image_path
                    db_release.save()
                except:
                    continue

