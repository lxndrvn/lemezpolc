import requests
import os

DISCOGS_KEY = os.environ.get('DISCOGS_KEY')
DISCOGS_SECRET = os.environ.get('DISCOGS_SECRET')

discogs_keys = 'Discogs key={0}, secret={1}'.format(DISCOGS_KEY, DISCOGS_SECRET)

HEADERS = {'user-agent': 'lemezpolc',
           'Authorization': discogs_keys}

SEARCH_URL = 'https://api.discogs.com/database/search'


def get_release_data(release):
    artist = release['artist']
    release_title = release['title']
    response = send_request(SEARCH_URL, params={'artist': artist,
                                                'release_title': release_title})
    discogs_link = response.json()['results'][0]['resource_url']
    image_link = response.json()['results'][0]['thumb']
    directory = release['directory']
    release['discogs_link'] = discogs_link
    release['image'] = download_image(image_link, directory)
    return release


def send_request(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def download_image(url, directory):
    filename = directory + '/folder.jpg'
    response = send_request(url)
    image = response.content
    with open(filename, 'wb+') as image_file:
        image_file.write(image)
    return image
