import os
import re

pattern = re.compile('(.*)\s-\s(.*)\s*\((\d{4})\)')

def collect_releases(path):
    with open("data.csv", "w") as f:
        for root, dirs, files in os.walk(path):
            for name in dirs:
                match = re.match(pattern, name)
                if not match:
                    print(name)
                    continue
                artist, title, year = match.groups()
                artist = artist.strip()
                title = title.strip()
                line = ",".join((artist, title, year))
                f.write(line)
                f.write("\n")

