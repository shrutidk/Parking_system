from django.shortcuts import render
from models import User, Park
from serializers import UserSerializer, LoginSerializer, ParkSerializer, ParkTicketSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CustomerLoginList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request):
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # user = authenticate(username=username, password=password)

        credentials = {
            "username":  request.data.get("username", ""),
            "password": request.data.get("password", ""),
        }

        #print(credentials)
        user = authenticate(**credentials)
        token = Token.objects.get(user=user).key

        #print(user)
        #print(token)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(token)


class CustomerList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ParkView(generics.ListCreateAPIView):
    """
    This endpoint presents the parks in the System
    """
    serializer_class = ParkSerializer
    queryset = Park.objects.all()
    permission_classes = (IsAuthenticated)  # Permission controlled by Admin


class ParkingSpots(generics.ListCreateAPIView):
    """
    This endpoint presents the searched parks in the System
    """
    serializer_class = ParkSerializer
    queryset = Park.objects.all()
    permission_classes = (IsAuthenticated)  # Permission controlled by Admin

    def post(self, request, *args, **kwargs):
        all_parking_spots = Park.objects.all()
        lat = request.data["lat"]
        long = request.data["long"]
        radius = request.data["radius"]
        all_avail_spots = []

        for spot in all_parking_spots:
            if ((spot.lat - lat) * (spot.long-lat) + (spot.long - long) * (spot.long - long) <= radius * radius):
                dt = ParkSerializer(instance=spot).data
                all_avail_spots.append(dt)

        return Response(data=all_avail_spots, status=status.HTTP_200_OK)


class PriceForParking(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated)
    serializer_class = ParkTicketSerializer
    def post(self, request, *args, **kwargs):
        plate_number = self.kwargs['plate_number']
        return Response(status=status.HTTP_200_OK)




