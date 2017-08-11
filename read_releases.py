import os
import re

pattern = re.compile('(.*)\s-\s(.*)\s*\((\d{4})\)')

def collect_releases(path):
    releases = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            details = get_details(name)
            if not details:
                print(name)
                continue
            releases.append(details)
    return releases


def get_details(name):
    match = re.match(pattern, name)
    if not match:
        return None
    artist, title, year = match.groups()
    details = {'artist': artist.strip(), 'title': title.strip(), 'year': year}
    return details
