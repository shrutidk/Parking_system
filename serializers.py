import math
from datetime import datetime, timezone

from rest_framework import serializers
from .models import User, Park, ParkingTicket


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)

        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['username', 'password']

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        user=User(username=validated_data['username'],password=validated_data['password'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class ParkSerializer(serializers.ModelSerializer):
    available_space = serializers.ReadOnlyField()
    number_of_parked_cars = serializers.ReadOnlyField()

    class Meta:
        model = Park
        fields = '__all__'


class ParkTicketSerializer(serializers.ModelSerializer):
    ticket_fee = serializers.SerializerMethodField(read_only=True)

    def get_ticket_fee(self, obj):
        stayed_time = datetime.now() - obj.entry_time
        stayed_time_mins = stayed_time.total_seconds()

        # left park within the first 30 minutes
        if stayed_time_mins < 1:
            return 0.0
        return math.ceil(stayed_time_mins) * obj.park.charge_per_min

    class Meta:
        model = ParkingTicket
        fields = ('ticket_fee', 'plate_number', 'entry_time', 'exit_time', 'park')
