
from django.urls import path
from rest_framework.routers import SimpleRouter

from blog.views import BlogViewSet, UserViewSet

# from base.script import *

router = SimpleRouter()
router.register('api/user', UserViewSet, basename='user')
router.register('api/posts', BlogViewSet, basename='blog')

urlpatterns = router.urls