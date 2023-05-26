from django.urls import path,include
from rest_framework import routers
from .views import JobsViewSet,JobsLocationViewSet


routes=routers.DefaultRouter()
routes.register(r'jobTitle',JobsViewSet,basename='jobTitle')
routes.register(r'joblocation',JobsLocationViewSet,basename='jobLocation')
# routes.register(r'job',JobsViewSet)
# routes.register(r'jobs',JobViewSet)

urlpatterns = [
    path('',include(routes.urls))
]