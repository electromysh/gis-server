from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from django.contrib.gis.geos import Polygon
from .serializer import CountrySerializer, CitySerializer
from .models import Country, City

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def query_set(self, request):
        queryset = self.queryset

        bbox_query = request.query_params.get('bbox')
        bbox_params = bbox_query.split(',') if bbox_query != None else []

        if len(bbox_params) == 4:
            try:
                bbox = (
                    float(bbox_params[0]),
                    float(bbox_params[1]),
                    float(bbox_params[2]),
                    float(bbox_params[3]),
                )
                queryset = City.objects.filter(geom__within=Polygon.from_bbox(bbox))
            except ValueError:
                raise ValidationError({'result': 'bbox query is invalid'}, status.HTTP_400_BAD_REQUEST)
        elif len(bbox_params) != 4 and len(bbox_params) != 0:
            raise ValidationError({'result': 'bbox query is invalid'}, status.HTTP_400_BAD_REQUEST)

        return queryset

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = self.queryset
        country_query = self.request.query_params.get('country')

        if country_query != None:
            try:
                country_query = int(country_query)
                queryset = City.objects.filter(country=country_query)
            except ValueError:
                raise ValidationError({'result': 'city id must be integer'}, status.HTTP_400_BAD_REQUEST)

        return queryset
