import requests
import os
from difflib import SequenceMatcher

import sys


DISCOGS_KEY = os.environ.get('DISCOGS_KEY')
DISCOGS_SECRET = os.environ.get('DISCOGS_SECRET')

discogs_keys = 'Discogs key={0}, secret={1}'.format(DISCOGS_KEY, DISCOGS_SECRET)

HEADERS = {'user-agent': 'lemezpolc',
           'Authorization': discogs_keys}

SEARCH_URL = 'https://api.discogs.com/database/search'


class DiscogsException(RuntimeError):
    pass


def extend_release(release):
    try:
        release_by_search = get_release_by_search(release)
        if not release_by_search:
            return release

        release.release_format = get_release_format(release_by_search['format'])

        release_by_url = get_release_by_api_url(release_by_search['resource_url'])
        release.discogs_link = release_by_url['uri']

        if not release.cover:
            release.cover = get_image(release, release_by_url, release.directory)

        return release

    except DiscogsException as e:
        sys.stderr.write(
            '{0} for {1} - {2} - {3}\n'.format(e, release.artist, release.title, release.year)
        )
        return release


def get_results(url, params=None):
    response = send_request(url, params)
    return response.json()['results']


def send_request(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    if not response.ok:
        print(response.text)
    return response


def get_release_by_search(release):
    results = get_results(SEARCH_URL, params={'artist': release.artist, 'release_title': release.title})
    if not results:
        results = get_release_by_title_search(release)
        if not results:
            return None
    return get_match_by_year(results, release.year)


def get_match_by_year(results, year):
    for version in results:
        if version.get('year') == year:
            return version

    results_with_year = [result for result in results if result.get('year')]
    if not results_with_year:
        return None

    return max(results_with_year, key=lambda version: version['year'])


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_release_by_title_search(release):
    # Title at Discogs means artist and release title, like "G.S. Schray - Gabriel"

    results = get_results(SEARCH_URL, params={'release_title': release.title})
    if not results:
        print('No Discogs match found for {0} - {1} - {2}'.format(release.artist, release.title, release.year))
        return None

    if release.artist == 'VA':
        full_title = 'Various - {0}'.format(release.title)

    else:
        full_title = '{0} - {1}'.format(release.artist, release.title)

    matches = [(similarity(full_title, result['title']), result) for result in results]
    return get_best_match(full_title, matches, release)


def get_best_match(full_title, matches, release):
    possible_matches = [match[1] for match in matches if match[0] > 0.9]
    print('Matches for {0}: {1}'.format(full_title, possible_matches))
    return possible_matches


def get_release_format(discogs_release_formats):
    formats = [f.lower() for f in discogs_release_formats]
    album_types = ['album', 'lp', 'cd', 'cdr', 'mixed', 'cassette', 'compilation', 'mixtape']

    if any(s in album_types for s in formats):
        return 'ALBUM'
    if 'mini-album' in formats:
        return 'MINI-ALBUM'
    if 'ep' in formats or 'vinyl' in formats:
        return 'EP'
    return 'UNKNOWN'


def get_release_by_api_url(url):
    response = send_request(url)
    return response.json()


def get_image(release, discogs_result, directory):
    images = discogs_result.get('images')
    if not images:
        print('Could not find image for {0} - {1}'.format(release.artist, release.title))
        return None

    image = get_primary_image(discogs_result['images'])
    return download_image(image['uri'], directory)


def get_primary_image(images):
    for image in images:
        if image['type'] == 'primary':
            return image
    return images[0]


def download_image(url, directory):
    try:
        filename = directory + '/folder.jpg'
        response = send_request(url)
        image = response.content
        with open(filename, 'wb+') as image_file:
            image_file.write(image)
        return filename
    except:
        raise DiscogsException('Could not download image')
