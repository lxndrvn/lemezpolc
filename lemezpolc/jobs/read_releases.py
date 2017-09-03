import os
import re

pattern = re.compile('.*\/(.*)\s-\s(.*)\s*\((\d{4})\)')


class Release(object):
    def __init__(self, artist, title, year):
        self.artist = artist
        self.title = title
        self.year = year
        self.cover = None
        self.discogs_link = None
        self.directory = None
        self.release_format = None


def collect_releases(path):
    releases = []

    for root, dirs, files in os.walk(path):
        release = get_details(root)
        if not release:
            print('No regex match for {0}'.format(root))
            continue

        release.cover = get_cover_by_filename(root, files)
        release.directory = root
        releases.append(release)

    return releases


def get_details(name):
    match = re.match(pattern, name)
    if not match:
        return None
    artist, title, year = match.groups()
    release = Release(artist.strip(), title.strip(), year)
    return release


def get_cover_by_filename(root, files):
    cover_file_names = ('folder.jpg', 'front.jpg')
    for name in cover_file_names:
        if name in files:
            return '{0}/{1}'.format(root, name)

    return get_cover_from_images(root, files)


def get_cover_from_images(root, files):
    possible_covers = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png'))]

    if len(possible_covers) == 1:
        return '{0}/{1}'.format(root, possible_covers[0])

    if len(possible_covers) > 1:
        print('Multiple covers found for {0}: {1}'.format(root, possible_covers))

    return None
