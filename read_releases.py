import os
import re

pattern = re.compile('(.*)\s-\s(.*)\s*\((\d{4})\)')

def collect_releases(path):
    with open("data.csv", "w") as output_file:
        for root, dirs, files in os.walk(path):
            for name in dirs:
                details = get_details(name)
                if not details:
                    print(name)
                    continue
                output_file.write(details)
                output_file.write("\n")

def get_details(name):
    match = re.match(pattern, name)
    if not match:
        return None
    artist, title, year = match.groups()
    artist = artist.strip()
    title = title.strip()
    line = ",".join((artist, title, year))
    return line

