from django.core.management import BaseCommand

from lemezpolc.jobs.resize_images import collect_covers


class Command(BaseCommand):
    def handle(self, *args, **options):
        collect_covers()