from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.home, name='browser-home'),
    path('browser/', views.browser, name='browser-browser'),
    path('panel/', views.panel, name='give-panel'),
    path('addviz/', views.addViz, name='viz'),
    path('delete/', views.delete, name='delete'),
    path('reset/', views.reset, name='reset'),
    path('data/', views.data, name='browser-data'),
    re_path('download/(?P<id>\d+)', views.file_down,name = "download"),
    path('find/', views.find, name='browser-find'),
    path('contact/', views.contact, name='browser-contact'),
]