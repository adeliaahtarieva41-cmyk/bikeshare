from django.urls import path
from women import views

urlpatterns = [
    path('', views.index, name='home'),
    path('all/', views.all_bikes, name='all_bikes'),
    path('bike/<slug:bike_slug>/', views.show_bike, name='bike'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag, name='tag'),
    path('addpage/', views.addpage, name='add_page'),
]