"""ShenasaSolution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from Shenasa import views
from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from .views import start_support, stop_support
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _

admin.site.site_header = _('Shenasa Administration Site')
admin.site.site_title = _('Welcome to Shenasa administration control panel')

router = routers.DefaultRouter()
router.register('news', views.NewsViewSets, basename='news')

urlpatterns = [
    path('', lambda request: redirect('/fa/admin/', permanent=False)),
    path('api/', include(router.urls)),
]

urlpatterns += i18n_patterns(
    path('admin/start_support/', start_support, name='start_support'),
    path('admin/stop_support/', stop_support, name='stop_support'),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
