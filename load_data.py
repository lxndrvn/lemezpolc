from models import Release
from read_releases import collect_releases
import os

PATH = os.environ.get('LEMEZPOLC_DEFAULT_PATH')

def populate_database():
    releases = collect_releases(PATH)
    
    for release in releases:
        create_release(release)
        

def create_release(release):
    Release.create(artist=release['artist'],
                   title=release['title'],
                   year=release['year'])
    print('release created')
    
populate_database()