from django.contrib.gis.db import models

class Country(models.Model):
    name = models.CharField(max_length=255)
    geom = models.MultiPolygonField(null=True)

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ImageField()
    geom = models.MultiPolygonField(null=True)
    isCapital = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)


    def __str__(self) -> str:
        return self.name
