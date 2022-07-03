from tokenize import Number
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Polygon
from .serializer import CountrySerializer, CitySerializer
from .models import Country, City

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request):
        bbox_query = request.query_params.get('bbox', '')
        bbox_params = bbox_query.split(',') if bbox_query != '' else []
        if len(bbox_params) == 4:
            bbox = (
                float(bbox_params[0]),
                float(bbox_params[1]),
                float(bbox_params[2]),
                float(bbox_params[3]),
            )
            polygon = Polygon.from_bbox(bbox)
            cities_in_bbox = City.objects.filter(geom__within=polygon)
            return Response({'detail': CitySerializer(cities_in_bbox, many=True).data}, status=status.HTTP_200_OK)
        elif len(bbox_params) != 0:
            return Response({'detail': 'bbox query invalid'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': CountrySerializer(self.queryset, many=True).data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        return Response(
            {'detail': CountrySerializer(get_object_or_404(self.queryset, pk=pk)).data},
            status=status.HTTP_200_OK
        )

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
