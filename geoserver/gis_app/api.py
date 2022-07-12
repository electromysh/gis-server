from django.contrib.gis.db.models.functions import Area
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.gis.geos import Polygon
from .serializer import CountrySerializer, CitySerializer
from .models import Country, City

def get_bbox(bbox_query):
    bbox_params = bbox_query.split(',') if bbox_query != None else []

    if len(bbox_params) == 4:
        try:
            bbox = (
                float(bbox_params[0]),
                float(bbox_params[1]),
                float(bbox_params[2]),
                float(bbox_params[3]),
            )
            return bbox
        except ValueError:
            raise ValueError
    elif len(bbox_params) != 4 and len(bbox_params) != 0:
            raise ValueError


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_queryset(self):
        queryset = self.queryset

        bbox_query = self.request.query_params.get('bbox')
        try:
            bbox = get_bbox(bbox_query)
            if bbox: queryset = City.objects.filter(geom__within=Polygon.from_bbox(bbox))
        except ValueError:
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


class AreaBbox(viewsets.ViewSet):
    def list(self, request):
        bbox_query = request.query_params.get('bbox')
        try:
            bbox = get_bbox(bbox_query)
            result_area = 0

            if bbox:
                queryset = City.objects.filter(geom__within=Polygon.from_bbox(bbox))
                queryset = queryset.annotate(area=Area('geom'))
                for city in queryset:
                    result_area += city.area.sq_m
            return Response({'result': result_area}, status=status.HTTP_200_OK)
        except ValueError:
            raise ValidationError({'result': 'bbox query is invalid'}, status.HTTP_400_BAD_REQUEST)
