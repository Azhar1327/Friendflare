from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('like_post', views.like_post, name='like_post'),
    path('broadcast', views.broadcast, name='broadcast'),
    path('broadcast_panel', views.broadcast_panel, name='broadcast_panel'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('chat', views.chat, name='chat'),
    path('chat/<str:pk>', views.chat_page, name='chat_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)