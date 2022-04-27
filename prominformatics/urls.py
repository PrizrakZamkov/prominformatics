"""prominformatics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db.models import Model
from django.urls import path, re_path
from django.conf.urls import include
import main.views
from rest_framework import routers, serializers, viewsets
from main.models import Project
from main.views import ProjectViewSet
from django.contrib.staticfiles.views import serve
def return_static(request, path, insecure=True, **kwargs):
  return serve(request, path, insecure, **kwargs)


router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'recent_projects', main.views.RecentProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.index_page),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/filter_params/', main.views.send_filter_params),
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
]
