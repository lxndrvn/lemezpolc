import os

from lemezpolc.models import Release


def remove_deleted_data():
    for release in Release.objects.all():
        if not os.path.exists(release.directory):
           print('Deleted release {0}'.format(release.directory))
           release.delete()
    return


remove_deleted_data()