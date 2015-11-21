from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
		url(r'^$', views.index),
		url(r'^addbusiness/$', views.add_business),
		url(r'^delbusiness_es/$', views.delete_business_es),
		url(r'^addespanol/$', views.add_business_es),
		url(r'^addcat/$', views.add_category),
		url(r'^getcats/$', views.get_categories),
		url(r'^getcatsfull/$', views.get_full_categories),
		url(r'^update_translate/$', views.translate_business),
		url(r'^editcat/$', views.edit_category),
		url(r'^updatecat/$', views.update_category),
		url(r'^deletecat/$', views.delete_category),
		url(r'^delete_from_cat/(?P<catbiz_id>.+)/$', views.delete_from_cat),
		url(r'^deletebusiness/(?P<bid>.+)/$', views.delete_business),

		#Category Stuff
		url(r'^get_cat_from_biz/$', views.get_categories_for_biz),

		#Find businesses
		url(r'^category/(?P<category_name>.+)/$', views.category_lookup),
		url(r'^product/(?P<product_id>.+)/$', views.product_lookup),

		#find business and products
		url(r'^search/$', views.search),
		url(r'^searchall/$', views.search_result), 

		#get businesses
		url(r'^getbusinesses/$', views.get_businesses),
		url(r'^getbusinesses_order/$', views.get_businesses_order),
		url(r'^getbusinesses_es/$', views.get_businesses_es),
		url(r'^getbusiness/$', views.get_one_business),
		url(r'^get_featured/$', views.get_featured_businesses),
		url(r'^update_featured/(?P<bid>.+)/$', views.update_featured_business),
		url(r'^get_num_featured/(?P<num_of_biz>.+)/$', views.get_number_featured_biz),

		#Edit businesses
		url(r'^editbusiness_es/$', views.edit_business_es),
		url(r'^editbusiness/$', views.edit_business),
		url(r'^updatebusiness/$', views.update_business),

		url(r'^get_english_from_name/$', views.get_english_from_name),

		url(r'^fish_prices/$', views.fish_prices),
    # Examples:
    # url(r'^$', 'sjdsdirectory.views.home', name='home'),
    # url(r'^sjdsdirectory/', include('sjdsdirectory.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

