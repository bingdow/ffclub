from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='intro.home'),
)
