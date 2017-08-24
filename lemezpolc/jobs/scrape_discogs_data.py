import requests
import os
from difflib import SequenceMatcher

import sys

from lemezpolc.jobs.resize_image import resize_image

DISCOGS_KEY = os.environ.get('DISCOGS_KEY')
DISCOGS_SECRET = os.environ.get('DISCOGS_SECRET')

discogs_keys = 'Discogs key={0}, secret={1}'.format(DISCOGS_KEY, DISCOGS_SECRET)

HEADERS = {'user-agent': 'lemezpolc',
           'Authorization': discogs_keys}

SEARCH_URL = 'https://api.discogs.com/database/search'


class DiscogsException(RuntimeError):
    pass


def get_release_data(release):
    try:
        release_by_search = get_release_by_search(release)
        release['format'] = get_release_format(release_by_search['format'])

        release_by_url = get_release_by_api_url(release_by_search['resource_url'])
        release['discogs_link'] = release_by_url['uri']

        if not any(file.endswith(".jpg") for file in release['directory']):
            image_path = get_image(release_by_url, release['directory'])
            release['cover'] = resize_image(image_path, release['artist'], release['title'])

        return release

    except DiscogsException as e:
        sys.stderr.write(
            '{0} for {1} - {2} - {3}\n'.format(e, release['artist'], release['title'], release['year'])
        )
        raise e


def send_request(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_release_by_search(release):
    artist = release['artist']
    title = release['title']
    year = release['year']
    response = send_request(SEARCH_URL, params={'artist': artist, 'release_title': title})
    results = response.json()['results']

    if results:
        matching_release = get_matching_release(results, year)
    else:
        response = send_request(SEARCH_URL, params={'release_title': title, 'year': year})
        matching_release = get_release_by_title_match(artist, title, response.json()['results'])

    return matching_release


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_release_by_title_match(artist, title, results):
    # Title at Discogs means artist and release title, like "G.S. Schray - Gabriel"

    full_title = artist + ' - ' + title
    matches = [
        (
            similarity(full_title, result['title']),
            result,
        )
        for result in results
    ]

    match_ratio, matching_result = max(matches)
    if match_ratio > 0.9:
        return matching_result
    else:
        if is_various_artists(full_title, matching_result['title']) and match_ratio > 0.7:
            return matching_result

    print('Found match for {0}: {1}. match ratio: {2}'.format(
        full_title, matching_result['title'], match_ratio)
    )


def is_various_artists(title, match_title):
    return title.startswith('VA') and match_title.startwith('Various')


def get_matching_release(results, year):
    for version in results:
        if version['year'] == year:
            return version

    return max(results, key=lambda version: version['year'])


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


def get_image(release, directory):
    image = get_primary_image(release['images'])
    return download_image(image['uri'], directory)


def get_primary_image(images):
    try:
        for image in images:
            if image['type'] == 'primary':
                return image
        return images[0]
    except:
        raise DiscogsException('Could not find image')


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
