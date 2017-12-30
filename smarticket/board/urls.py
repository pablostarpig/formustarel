from django.conf.urls import url
from . import views

app_name = 'board'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<project_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^ticket_(?P<ticket_id>[0-9]+)/$', views.ticket_detail, name='ticket_detail'),
    # url(r'^(?P<ticket_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    # url(r'^tickets/(?P<filter_by>[a-zA_Z]+)/$', views.tickets, name='tickets'),
    url(r'^create_project/$', views.create_project, name='create_project'),
    url(r'^(?P<project_id>[0-9]+)/create_ticket/$', views.create_ticket, name='create_ticket'),
    url(r'^(?P<project_id>[0-9]+)/delete_ticket/(?P<ticket_id>[0-9]+)/$', views.delete_ticket, name='delete_ticket'),
    # url(r'^(?P<project_id>[0-9]+)/favorite_project/$', views.favorite_project, name='favorite_project'),
    url(r'^(?P<project_id>[0-9]+)/delete_project/$', views.delete_project, name='delete_project'),
    url(r'^(?P<project_id>[0-9]+)/update/$', views.update_project, name='update_project'),
    url(r'^ticket_(?P<ticket_id>[0-9]+)/update/$', views.update_ticket, name='update_ticket'),
]