from django.contrib import admin
from django.urls import path,include
import views
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('sign-up/',views.CustomerList.as_view()),
    # path('account/',include('allauth.urls')),
    # path('login/',views.CustomerLoginList.as_view()),
    # path('login-token/',obtain_auth_token),
    # path('signup/<int:pk>/', views.CustomerDetails.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
