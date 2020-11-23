from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.behaviors import Protected


class Login(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data['username'], password=request.data['password'])

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})


class Protected(Protected):
    def get(self, request):
        return Response({'org': request.user.org.name})
