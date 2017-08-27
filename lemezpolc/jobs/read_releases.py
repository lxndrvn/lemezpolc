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
        self.format = None


def collect_releases(path):
    releases = []

    for root, dirs, files in os.walk(path):
        details = get_details(root)
        if not details:
            continue

        details['cover'] = get_cover(root, files)
        details['directory'] = root
        releases.append(details)

    return releases


def get_details(name):
    match = re.match(pattern, name)
    if not match:
        return None
    artist, title, year = match.groups()
    release = Release(artist.strip(), title.strip(), year)
    return release


def get_cover(root, files):
    cover = None
    cover_file_names = ('folder.jpg', 'front.jpg')
    for name in cover_file_names:
        if name in files:
            cover = name

    if not cover:
        candidates = []
        for f in files:
            if f.endswith(('.jpg', '.jpeg', '.png')):
                candidates.append(f)

        if len(candidates) == 1:
            cover = candidates[0]
        if len(candidates) > 1:
            print(root, candidates)

    if cover:
        return '{0}/{1}'.format(root, cover)
    return None
