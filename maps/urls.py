from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('a_dir', views.app_dir, name='a_dir'),
    url('home', views.home, name='home'),
    url('b_add', views.app_add, name='b_add'),
    url('app_amenity', views.app_amenity, name='app_amenity'),
    url(r'^ajax/add/$', views.answer_me, name='add'),
    url(r'^ajax/dir/$', views.dir_map, name='dir'),
    url(r'^ajax/amenity/$', views.amenity, name='amenity'),


              ]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


