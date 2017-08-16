import os
import re

pattern = re.compile('.*\/(.*)\s-\s(.*)\s*\((\d{4})\)')


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
    details = {'artist': artist.strip(), 'title': title.strip(), 'year': year}
    return details


def get_cover(root, files):
    cover = None
    cover_file_names = ('folder.jpg', 'front.jpg')
    for name in cover_file_names:
        if name in files:
            cover = name

    if not cover:
        candidates = []
        for f in files:
            if f.endswith('.jpg'):
                candidates.append(f)

        if len(candidates) == 1:
            cover = candidates[0]
        if len(candidates) > 1:
            print(root, candidates)

    if cover:
        with open('{0}/{1}'.format(root, cover), 'rb') as cover_file:
            image = cover_file.read()
        return image
    return None
