import os
from models import Release

def remove_deleted_data():
    for release in Release.select():
        if not os.path.exists(release.directory):
           print('Deleted release {0}'.format(release.directory))
           release.delete_instance()
    return


remove_deleted_data()