from models import Release
from read_releases import collect_releases

def populate_database():
    releases = collect_releases("/Users/lxndrvn/Downloads/Zene")
    
    for release in releases:
        create_release(release)
        

def create_release(release):
    Release.create(artist=release['artist'],
                   title=release['title'],
                   year=release['year'])
    print('release created')
    
populate_database()