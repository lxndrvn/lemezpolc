from models import Release
from read_releases import collect_releases
import os
import time

from scrape_discogs_data import get_release_data

PATH = os.environ.get('LEMEZPOLC_DEFAULT_PATH')

def populate_database():
    releases = collect_releases(PATH)

    for release in releases:
        updated_release = get_release_data(release)
        create_release(updated_release)
        time.sleep(3)

    print('Releases created')


def create_release(release):
    Release.create(artist=release['artist'],
                   title=release['title'],
                   year=release['year'],
                   discogs_link=release['discogs_link'],
                   cover=release['image'],
                   directory=release['directory'])
    
populate_database()