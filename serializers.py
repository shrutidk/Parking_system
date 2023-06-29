from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        """
        Create and return a new `Product` instance, given the validated data.
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Product` instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)

        instance.save()
        return instance


# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields = ['username', 'password']
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Product` instance, given the validated data.
#         """
#         user=User(username=validated_data['username'],password=validated_data['password'])
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#
#
#
