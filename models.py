from peewee import PostgresqlDatabase, Model, CharField, IntegerField, BlobField

db = PostgresqlDatabase('lemezpolc', user='lxndrvn')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db

class Release(BaseModel):
    artist = CharField(null=False)
    title = CharField(null=False)
    year = IntegerField(null=False)
    cover = BlobField()
    discogs_link = CharField()
    path = CharField()
