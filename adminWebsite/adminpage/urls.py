from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.admin_home, name="admin_home"),
    url(r'^billing$', views.admin_billing, name="admin_billing"),
    url(r'^archive$', views.admin_archive, name="admin_archive"),
    url(r'^(?P<order_id>[0-9]+)$', views.admin_orderDetail, name="admin_orderDetail"),
]
