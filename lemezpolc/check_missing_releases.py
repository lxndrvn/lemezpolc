import os

from read_releases import collect_releases

from lemezpolc_project.lemezpolc.load_data import is_in_database

PATH = os.environ.get('LEMEZPOLC_DEFAULT_PATH')

def check_missing():
    releases = collect_releases(PATH)
    for release in releases:
        if is_in_database(release):
            continue
        print(release['artist'],release['title'])

check_missing()