from rest_framework import serializers
from account.models import User


class AirtechUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')



class CreateAirtechUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
    
    def create(self, validated_data):
        password = validated_data.get('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AirtechLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')



class JSONWebTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=225)

