from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('profile/favorites/', views.profile, name='profile'),
    path('profile/info/', views.profile_info, name='profile_info'),
    path('profile/messages/', views.profile_messages, name='profile_msgs'),
    path('profile/archive/', views.profile_archive, name='profile_archive'),
    path('profile/add-object/', views.add_object, name='profile_add_object'),
    path('reviews/', views.reviews, name='reviews'),

    # path('item/<str:pk>/', views.item, name='item'),
    path('objects/<slug:slug>/', views.item, name='item'),

    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('privacy/', views.privacy, name='privacy'),
    path('FAQ/', views.faq, name='faq'),
    path('TOS/', views.tos, name='tos'),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
    path('logout/', views.log_out, name='logout')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
