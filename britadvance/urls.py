from django.contrib import admin
from django.urls import path,include
from monday import urls as mee

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(mee))
]
