from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_routes),
    path('get-average-rating/', views.get_rating),
    path('remove-fav/<slug:slug>/', views.remove_favorite),
    path('add-fav/<slug:slug>/', views.add_favorite),
    path('move-to-archive/<slug:slug>/', views.move_to_archive),
    path('remove-from-archive/<slug:slug>/', views.remove_from_archive),

]
