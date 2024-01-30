
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about_us/', views.about_us, name='about_us'),
    path('category/<slug:category_slug>/', views.home, name='category_wise_post'),
    path('account/', include("passenger.urls")),
    path('train/', include("train.urls")),
    path('station/', include("station.urls")),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)