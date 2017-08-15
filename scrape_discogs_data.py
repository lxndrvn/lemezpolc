import requests
import os

DISCOGS_KEY = os.environ.get('DISCOGS_KEY')
DISCOGS_SECRET = os.environ.get('DISCOGS_SECRET')

discogs_keys = 'Discogs key={0}, secret={1}'.format(DISCOGS_KEY, DISCOGS_SECRET)

HEADERS = {'user-agent': 'lemezpolc',
           'Authorization': discogs_keys}

SEARCH_URL = 'https://api.discogs.com/database/search'


def get_release_data(release):
    release_by_search = get_release_by_search(release)
    release['format'] = get_release_format(release_by_search['format'])
    
    release_by_url = get_release_by_api_url(release_by_search['resource_url'])
    release['discogs_link'] = release_by_url['uri']

    if not any(file.endswith(".jpg") for file in release['directory']):
        release['image'] = get_image(release_by_url, release['directory'])

    return release


def send_request(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_release_by_search(release):
    response = send_request(
        SEARCH_URL,
        params={'artist': release['artist'], 'release_title': release['title']}
    )
    return get_matching_release(response, release['year'])
    
    
def get_matching_release(response, year):
    all_releases = response.json()['results']
    for version in all_releases:
        if version['year'] == year:
            return version

def get_release_format(discogs_release_format):
    if 'Album' in discogs_release_format:
        return 'ALBUM'
    if 'Mini-Album' in discogs_release_format:
        return 'MINI-ALBUM'
    if 'EP' in discogs_release_format:
        return 'EP'
    
    print('Could not find format in {0}'.format(discogs_release_format))
    return None

def get_release_by_api_url(url):
    response = send_request(url)
    return response.json()


def get_image(release, directory):
    image = get_primary_image(release['images'])
    return download_image(image['uri'] , directory)
    
def get_primary_image(images):
    for image in images:
        if image['type'] == 'primary':
            return image
    return images[0]
    
def download_image(url, directory):
    filename = directory + '/folder.jpg'
    response = send_request(url)
    image = response.content
    with open(filename, 'wb+') as image_file:
        image_file.write(image)
    return image
