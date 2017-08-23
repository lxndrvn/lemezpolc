from django.db import models

# Create your models here.
class Release(models.Model):
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    cover = models.BinaryField(blank=True, null=True)
    discogs_link = models.CharField(max_length=255, blank=True, null=True)
    directory = models.CharField(max_length=255, blank=True, null=True)
    format = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'release'