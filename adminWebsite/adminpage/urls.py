from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.admin_home, name="admin_home"),
    url(r'^billing$', views.admin_billing, name="admin_billing"),
    url(r'^archive$', views.admin_archive, name="admin_archive"),
    url(r'^order/(?P<order_id>[0-9]+)$', views.admin_orderDetail, name="admin_orderDetail"),
    url(r'^order/(?P<order_id>[0-9]+)/revision/$', views.admin_editPage, name="admin_editPage"),
    url(r'^manageProducts$', views.admin_manageProducts, name="admin_manageProducts"),
    url(r'^productEdition/(?P<product_id>[0-9]+)$', views.admin_productEdit, name="admin_productEdit"),
    url(r'^newProduct$', views.admin_newProduct, name="admin_newProduct"),

    # api call

    url(r'^api/orderRevise/(?P<order_id>[0-9]+)$', views.admin_orderRevise, name="admin_orderRevise"),
    url(r'^api/revision/$', views.admin_revise, name="admin_revise"),
    url(r'^api/autoDruglist$', views.admin_autoDruglist, name="admin_autoDruglist"),
    url(r'^productDelete/(?P<product_id>[0-9]+)$', views.admin_productDelete, name="admin_productDelete"),
]
