import math
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import People
from django.contrib.auth.models import User
from .serializers import UserSerializer, PeopleSerializer

class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    


class PeopleView(APIView):
    # existing methods...

    def get(self, request):
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lng')

        center_point = Point(float(longitude), float(latitude), srid=4326)
        max_distance = D(km=1)  

        if latitude and longitude:
            people_nearby = People.objects.annotate(
                                distance=Distance('location', center_point)
                            ).filter(
                                distance__lte=max_distance
                            ).order_by('distance')

            serializer = PeopleSerializer(people_nearby, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Missing latitude and/or longitude parameters"}, status=400)
        
    

# class PeopleView(APIView):
#     # existing methods...

#     def get(self, request):
#         latitude = request.GET.get('lat')
#         longitude = request.GET.get('lng')

#         center_point = Point(float(longitude), float(latitude), srid=4326)  # Longitude, Latitude
#         # people_nearby = People.objects.annotate(distance=Distance('location', center_point)).filter(distance__lte=max_distance.km).order_by('distance')
#         # people_nearby = People.objects.filter(location__distance_lte=(filter_location, max_distance))
#         # Serialize and return the queryset

#         max_distance = D(km=1)  
#         # max_distance = self.distance_to_decimal_degrees(max_distance.km, float(latitude))

#         if latitude and longitude:
#             # people_nearby = People.objects.filter(
#             #     location__distance_lte=(filter_location, max_distance)
#             # )
#             people_nearby = People.objects.annotate(
#                                 distance=Distance('location', center_point)
#                             ).filter(
#                                 distance__lte=max_distance.km
#                             ).order_by('distance')

#             serializer = PeopleSerializer(people_nearby, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({"error": "Missing latitude and/or longitude parameters"}, status=400)
        
    
#     def distance_to_decimal_degrees(self, distance, latitude):
#         lat_radius = math.radians(latitude)
#         earth_radius = 6371000
#         meters_per_degree = math.cos(lat_radius) * 2 * math.pi * earth_radius / 360
#         return distance/meters_per_degree

    
