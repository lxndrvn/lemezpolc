from lemezpolc.models import Release


def is_in_database(release):
    db_record = Release.objects.filter(artist=release.artist, title=release.title)
    return db_record.exists()
