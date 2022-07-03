from django.contrib.gis.db import models

class Country(models.Model):
    name = models.CharField(max_length=255)
    geom = models.MultiPolygonField(null=True, srid=4326)

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    images = models.ImageField(null=True, blank=True, upload_to='image')
    geom = models.MultiPolygonField(null=True, srid=4326)
    isCapital = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)


    def __str__(self) -> str:
        return self.name
