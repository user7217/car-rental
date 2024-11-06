from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('add_car/', views.add_car_view, name='add_car'),
    path('rent_car/<int:car_id>/', views.rent_car_view, name='rent_car'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)