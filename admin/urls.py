from django.conf.urls import patterns, url
from admin import views

urlpatterns = patterns('',
		url(r'^/$', views.index),
		url(r'^/espanol$', views.admin_espanol),
		url(r'^/espanol/edit$', views.admin_espanol_edit),
		url(r'^/translate$', views.admin_translate),
		url(r'^/espanol/edit$', views.admin_espanol_edit),
		url(r'^/cats/$', views.categories),
		url(r'^/manage_featured/$', views.manage_featured),
		url(r'^/cats/edit/(?P<cid>.+)/$', views.edit_category),
)

