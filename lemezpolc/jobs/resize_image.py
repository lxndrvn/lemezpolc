from PIL import Image
from resizeimage import resizeimage
from lemezpolc_project.settings import STATIC_ROOT


def resize_image(image_path, artist, title):
    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        thumbnail = resizeimage.resize_thumbnail(image, [150, 150])
        image_name = generate_image_name(artist, title)
        resized_image_path = '{0}/covers/{1}'.format(STATIC_ROOT, image_name)   
        thumbnail.save(resized_image_path, thumbnail.format)
    return image_name


def generate_image_name(artist, title):
    return '{0}_{1}.jpg'.format(snake_case(artist), snake_case(title))

def snake_case(string):
    return '_'.join(string.lower().split())

