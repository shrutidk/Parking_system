from django.contrib import admin
from django.urls import path,include
import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    #path('auth/', include('rest_auth.urls')),
    path('sign-up/', views.CustomerList.as_view()),
    path('signup/<int:pk>/', views.CustomerDetails.as_view()),
    path('login/', views.CustomerLoginList.as_view()),
    path('park/', views.ParkView.as_view()),
    path('search-parking-spots/', views.ParkingSpots.as_view()),
    path('park/<park_pk>/parkingtickets/', views.PriceForParking.as_view()),

]
