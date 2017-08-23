from PIL import Image
from resizeimage import resizeimage

from lemezpolc.config import PATH, TEST_PATH
from lemezpolc.models import Release
from lemezpolc.read_releases import collect_releases
from lemezpolc_project.settings import STATIC_ROOT

def collect_covers():
    releases = collect_releases(TEST_PATH)
    for release in releases:
        cover = release['cover']
        artist = release['artist']
        title = release['title']
        if cover:
            try:
                db_release = Release.objects.get(artist=artist, title=title)
                image_path = resize_image(cover, artist, title)
                db_release.cover_path = image_path
                db_release.save()
            except:
                continue

def resize_image(image_path, artist, title):
    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        thumbnail = resizeimage.resize_thumbnail(image, [150, 150])
        image_name = generate_image_name(artist, title)
        resized_image_path = '{0}/{1}'.format(STATIC_ROOT, image_name)   
        thumbnail.save(resized_image_path, thumbnail.format)
    return resized_image_path


def generate_image_name(artist, title):
    return '{0}_{1}.jpg'.format(snake_case(artist), snake_case(title))

def snake_case(string):
    return '_'.join(string.lower().split())


collect_covers()