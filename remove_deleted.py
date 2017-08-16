import os
from models import Release

def remove_deleted_data():
    for release in Release.select():
        if not os.path.exists(release.directory):
           release.delete_instance()


remove_deleted_data()