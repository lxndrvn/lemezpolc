import os

from django.core.management import BaseCommand

from lemezpolc.models import Release


class Command(BaseCommand):
    def handle(self, *args, **options):
        for release in Release.objects.all():
            if not os.path.exists(release.directory):
               print('Deleted release {0}'.format(release.directory))
               release.delete()
