import os

from lemezpolc.jobs.load_data import is_in_database
from lemezpolc.jobs.read_releases import collect_releases

PATH = os.environ.get('LEMEZPOLC_DEFAULT_PATH')

def check_missing():
    releases = collect_releases(PATH)
    for release in releases:
        if is_in_database(release):
            continue
        print(release['artist'],release['title'])

check_missing()