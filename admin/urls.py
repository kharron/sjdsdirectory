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
		url(r'^/testsolr/$', views.testsolr),
		url(r'^/fish_prices/$', views.fish_prices),
		url(r'^/pescado_precios/$', views.fish_prices),
		url(r'^/addfish/$', views.add_fish_prices),
		url(r'^/biz_without_photo/$', views.missing_photo_list),
		url(r'^/delfish/(?P<fishid>.+)/$', views.del_fish_price),
)

