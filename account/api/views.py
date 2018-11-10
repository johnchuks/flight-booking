from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_jwt.settings import api_settings
from account.models import User, get_user
from account.api.serializers import AirtechUserSerializer, JSONWebTokenSerializer, AirtechLoginSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class AirtechUserSignup(APIView):
    """ Persists user information for signup """
    
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AirtechUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token_serializer = JSONWebTokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(get_user(serializer.data.get('id')))
                )
            })
            if token_serializer.is_valid():
                response = {
                    'token': token_serializer.data.get('token'),
                    'id': serializer.data.get('id'),
                    'first_name': serializer.data.get('first_name'),
                    'last_name': serializer.data.get('last_name'),
                    'email': serializer.data.get('email')
                }
                return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AirtechUserLogin(APIView):

    permission_classes = (AllowAny,)

    def validate_email_password(self, request, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
        else:
            msg = 'Must include a username and password to login'
            raise exceptions.ValidationError(msg)
        return user


    def post(self, request):
        authenticated_user = self.validate_email_password(request, request.data)
        if authenticated_user:
            serializer = AirtechLoginSerializer(authenticated_user)
            token_serializer = JSONWebTokenSerializer(data={
            "token": jwt_encode_handler(
                jwt_payload_handler(get_user(serializer.data.get('id')))
            )
            })
            if token_serializer.is_valid():
                response = {
                    'token': token_serializer.data.get('token'),
                    'id': serializer.data.get('id'),
                    'first_name': serializer.data.get('first_name'),
                    'last_name': serializer.data.get('last_name'),
                    'email': serializer.data.get('email')
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







    
            

