from django.urls import path
from . import views

app_name = 'gpt'

urlpatterns = [
    path('', views.gpt_page, name='gpt_page'),
    path('ask/', views.gpt_ask, name='gpt_ask'),
]