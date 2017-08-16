import requests
import os

import sys

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
        release['format'] = get_release_format(release, release_by_search['format'])
        
        release_by_url = get_release_by_api_url(release_by_search['resource_url'])
        release['discogs_link'] = release_by_url['uri']
    
        if not any(file.endswith(".jpg") for file in release['directory']):
            release['image'] = get_image(release_by_url, release['directory'])
    
        return release
    
    except DiscogsException as e:
        sys.stderr.write(
            '{0} for {1} - {2} - {3}'.format(e, release['artist'], release['title'], release['year'])
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
    return get_matching_release(response, year)
    
def get_matching_release(response, year):
    all_releases = response.json()['results']
    for version in all_releases:
        if version['year'] == year:
            return version
    raise DiscogsException('Could not find matching release')

def get_release_format(release, discogs_release_format):
    if 'Album' in discogs_release_format or 'LP' in discogs_release_format:
        return 'ALBUM'
    if 'Mini-Album' in discogs_release_format:
        return 'MINI-ALBUM'
    if 'EP' in discogs_release_format:
        return 'EP'
    
    raise DiscogsException('Could not find format ({0})'.format(discogs_release_format))

def get_release_by_api_url(url):
    response = send_request(url)
    return response.json()


def get_image(release, directory):
    image = get_primary_image(release['images'])
    return download_image(image['uri'] , directory)

    
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
        return image
    except:
        raise DiscogsException('Could not download image')
