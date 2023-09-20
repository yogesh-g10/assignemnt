
from django.urls import path
from rest_framework.routers import SimpleRouter

from blog.views import UserViewSet, EventViewSet

# from base.script import *

router = SimpleRouter()
router.register('api/user', UserViewSet, basename='user')
router.register('api/events', EventViewSet, basename='blog')

urlpatterns = router.urls