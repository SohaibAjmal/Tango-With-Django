from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',url(r'^$',views.index, name= 'index'),
                       url(r'^(?P<category_name_url>\w+)/edit_category/$',views.edit_category, name= 'edit_category'),
                       url(r'^about',views.about, name= 'about'),
                       url(r'^add_category/$',views.add_category, name = 'add_category'),
                       url(r'^category/(?P<category_name_url>\w+)/add_page/$',views.add_page, name = 'add_page'),
                       url(r'^category/(?P<category_name_url>\w+)/edit_page/$',views.edit_page, name = 'edit_page'),
                       url(r'^category/(?P<category_name_url>\w+)/$',views.category,name = 'category'),
                       url(r'^register/$', views.register, name='register'), 
                       #url(r'^edit_category/$', views.edit_category, name='edit_category'), 
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^restricted/', views.restricted, name='restricted'),
                       url(r'^login/$', views.user_login, name='login'), )