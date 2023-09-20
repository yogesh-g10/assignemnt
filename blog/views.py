import json

from django.contrib.auth.models import AnonymousUser
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django_q.models import Schedule
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.renderers import BrowsableAPIRenderer, BaseRenderer

from blog.email import trigger_email
from blog.models import AppUser, Event, Employee
from blog.serializers import LoginSerializer, UserSerializer, EventSerializer


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

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        return []

    @action(detail=False, methods=['POST'])
    def send_mail(self, serializer):
        queryset = Event.objects.all()

        for instance in queryset:
            execution_time = instance.date
            instance_type = instance.event_type
            sc_instance = Schedule.objects.create(func='blog.task.send_email',
                                                  # args=instance.id,
                                                  kwargs={'event_type': instance_type, "instance_id": instance.id},
                                                  schedule_type='O',
                                                  next_run=execution_time,
                                                  repeats=1,
                                                  )
            print(sc_instance.id)
        return Response({'message': 'All mails have been scheduled'}, status=200)
