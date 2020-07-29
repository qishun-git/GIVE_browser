from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='browser-home'),
    path('browser/', views.browser, name='browser-browser'),
    path('panel/', views.panel, name='give-panel'),
]