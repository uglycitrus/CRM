import os

from django.conf.urls.defaults import *
from myproject import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('myproject.opmlist.views',
	url(r'^contacts/$', 'contact_list', name = 'contact_list'),
	url(r'^contacts/new/$', 'contact_new', name = 'contact_new'),
	url(r'^contacts/new_popup/', 'contact_new_popup', name = 'contact_new_popup'),
	url(r'^contacts/edit/(\d+)/$', 'contact_edit', name = 'contact_edit'),
	url(r'^contacts/view/(\d+)/$', 'contact_view', name = 'contact_view'),
	url(r'^contacts/add_popup/(.*)/$', 'contact_add_popup', name = 'contact_add_popup'),
	url(r'^projects/$', 'project_list', name = 'project_list'),
	url(r'^projects/edit/(\d+)/$', 'project_edit', name = 'project_edit'),
	url(r'^projects/view/(\d+)/$', 'project_view', name = 'project_view'),
	url(r'^projects/new/$', 'project_new', name = 'project_new'),
	url(r'^batteries/$', 'battery_list', name = 'battery_list'),
	url(r'^batteries/battery_new/$', 'battery_new', name = 'battery_new'),
	url(r'^batteries/battery_edit/(\d+)/$', 'battery_edit', name = 'battery_edit'),
	url(r'^batteries/pack_new/$', 'pack_new', name = 'pack_new'),
	url(r'^batteries/(?P<value>\w+)/(?P<selection>\w+)/$', 'battery_list', name = 'battery_list'),
	url(r'^packs/(?P<type_number>\w+)/$', 'pack_list', name = 'pack_list'),
	url(r'^pack/(?P<vkb_number>\w+)/$', 'pack_edit', name = 'pack_edit'),
	url(r'^samples/$', 'sample_list', name = 'sample_list'),
	url(r'^samples/new/(\d+)/$', 'sample_new', name = 'sample_new'),
	url(r'^samples/new/independent/$', 'sample_new_independent', name = 'sample_new_independent'),
	url(r'^samples/(\d+)/$', 'sample_edit_or_view', name = 'sample_edit_or_view'),
	url(r'^quotes/$', 'quote_list', name = 'quote_list'),
	url(r'^quote/new/(\d+)/$', 'quote_new', name = 'quote_new'),
	url(r'^spr/$', 'spr_list', name = 'spr_list'),
	url(r'^spr/new/(\d+)/$', 'spr_new', name = 'spr_new'),
	url(r'^sprs/(\d+)/$', 'spr_edit_or_view', name = 'spr_edit_or_view'),
	url(r'^uploads/$', 'upload_list', name = 'upload_list'),
	url(r'^uploads/new_popup/', 'upload_new_popup', name = 'upload_new_popup'),
	url(r'^uploads/new/$', 'upload_new', name = 'upload_new'),
	url(r'^quotes/(\d+)/$', 'quote_edit_or_view', name = 'quote_edit_or_view'),
	url(r'^uploads/edit/(?P<id>\d+)/$', 'upload_edit', name = 'upload_edit'),
	url(r'^uploads/view/(?P<file_name>.*)/$', 'upload_view', name = 'upload_view'),
	url(r'^uploads/link/(?P<link_type>.*)/(?P<id>\d+)/$', 'link_a_file', name = 'link_a_file'),
	url(r'^uploads/confirm/link/(?P<link_type>.*)/(?P<id>\d+)/(?P<upload_id>\d+)/$', 'link_a_file_confirm', name = 'link_a_file_confirm'),
	url(r'^accounts/login/$', 'login_view', name = 'login'),
	url(r'^logout/$', 'logout_view', name = 'logout'),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/(.*)', admin.site.root),
)

urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.split(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])[0]+'/static_media'}),
    )
