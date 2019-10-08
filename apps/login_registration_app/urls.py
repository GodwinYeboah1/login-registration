from django.conf.urls import url,include

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^users/new$', views.create_user),
    url(r'^logins/check$', views.login_user),
    url(r'^success$', views.display_success_page),
    url(r'^logout$', views.logout)
]
