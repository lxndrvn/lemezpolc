from models import Release
from read_releases import collect_releases
import os
import time

from scrape_discogs_data import get_release_data

PATH = os.environ.get('LEMEZPOLC_DEFAULT_PATH')

def populate_database():
    releases = collect_releases(PATH)

    for release in releases:
        if not is_in_database(release):
            create_release(release)
            time.sleep(3)
                


def create_release(release):
    try:
        updated_release = get_release_data(release)
        Release.create(artist=updated_release.get('artist'),
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

def is_in_database(release):
    db_record = Release.select().where(
        (Release.artist == release['artist']) &
        (Release.title == release['title'])
    )
    return db_record.exists()

populate_database()
