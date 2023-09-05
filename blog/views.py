import json

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.renderers import BrowsableAPIRenderer, BaseRenderer

from blog.email import trigger_email
from blog.models import Blog, AppUser
from blog.serializers import BolgSerializer, LoginSerializer, UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()

    @action(detail=False, methods=['post'], permission_classes=(AllowAny,), authentication_classes=())
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: AppUser = serializer.save()
        headers = self.get_success_headers(serializer.data)
        token = RefreshToken.for_user(user)
        token['sub'] = user.username

        data = {'token': {'refresh': f'{token}', 'access': f'{token.access_token}'},
                'user': UserSerializer(user, context={"request": request}).data}
        return Response(data, status=status.HTTP_200_OK, headers=headers)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BolgSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(author=user)

    def perform_create(self, serializer):
        instance = serializer.save()
        send_email = {'subject': "Welcome", 'body': "This is my first blog", "recipients": instance.author.email}
        trigger_email(send_email)
