from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from account.api.serializers import (
    CreateAirtechUserSerializer,
    JSONWebTokenSerializer,
    AirtechLoginSerializer,
    AirtechUserSerializer,
    FileUploadSerializer
)
from account.models import User, get_user

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AirtechUserSignup(APIView):
    """ Persists user information for signup """

    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        if email and password and first_name:
            serializer = CreateAirtechUserSerializer(data=request.data)
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
        return Response(dict(message="email, password and firstname are required"), status=400)


class AirtechUserLogin(APIView):
    permission_classes = (AllowAny,)

    def validate_email_password(self, request, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        if email and password:
            user = authenticate(request, email=email, password=password)
            return user
        msg = 'Must include an email and password to login'
        raise exceptions.ValidationError(msg)

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
        response = dict(message="Invalid request")
        return Response(response, status=400)


class AirtechUserViewSet(viewsets.ViewSet):
    def list(self, request):
        if not request.user.is_staff:
            response = dict(message='You are not authorized to view this information')
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        queryset = User.objects.all()
        serializer = AirtechUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = AirtechUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if str(request.user.pk) != pk:
            response = dict(message="You are not authorized to edit this information")
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        update_set = {'first_name', 'last_name'}
        request_set = set(request.data.keys())

        if request_set.issubset(update_set):
            for key, value in request.data.items():
                setattr(user, key, value)
            user.save()
            serializer = AirtechUserSerializer(user)
            return Response(serializer.data)
        response = dict(message="Some of the fields provided are not permitted for this action")
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    def upload(self, request):
        try:
            file = request.data.get('file')
        except KeyError: # pragma: no cover
            print('we here')
            return ParseError('Empty Content: No file attached')
        user = request.user
        user.profile_photo = file
        user.save()
        serializer = FileUploadSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_photo(self, request):
        user = request.user
        user.profile_photo.delete(save=True)
        response = dict(message="Photo deleted successfully")
        return Response(response, status=status.HTTP_204_NO_CONTENT)
