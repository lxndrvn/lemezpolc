from peewee import PostgresqlDatabase, Model, CharField, IntegerField, BlobField

db = PostgresqlDatabase('lemezpolc', user='lxndrvn')


class BaseModel(Model):

    class Meta:
        database = db

class Release(BaseModel):
    artist = CharField()
    title = CharField()
    year = IntegerField()
    cover = BlobField(null=True)
    discogs_link = CharField(null=True)
    directory = CharField(null=True)
