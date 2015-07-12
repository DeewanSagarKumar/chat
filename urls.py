from django.conf.urls import patterns, include, url
import socketio.sdjango
from chat import views
from django.contrib.auth import views as auth_view
socketio.sdjango.autodiscover()
urlpatterns = patterns("",
    url("^socket\.io", include(socketio.sdjango.urls)),
    url(r'^rooms/$', views.rooms, name="rooms"),
    url(r'^create/$', views.create, name="create"),
    url(r'^room/(?P<slug>[-\w]+)/$', views.room, name="room"),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view, name='auth_view'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^loggedin/$', views.loggedin, name='loggedin'),
    url(r'^incorrect/$', views.incorrect, name='incorrect'),
    url(r'^register/$', views.register_user, name='register_user'),
    url(r'^register_success/$', views.register_success, name='register_success'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^reset_done/$', views.reset_done, name='reset_done'),
     url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            views.reset_confirm, name='reset_confirm'),
    url(r'^reset_complete/$', views.reset_complete, name='reset_complete'),
    url(r'^confirm/(?P<activation_key>\w+)/',views.register_confirm,name='register_confirm'),
    url(r'^profile/(?P<slug>.*)/$', views.profile, name='profile'),
    
)

