from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'dir_browse'
urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='dir_browse:login'), name='logout'),
    path("login/", views.MyLoginView.as_view(template_name="dir_browse/login.html"), name='login'),
    path("", views.index, name="index"),
    path('delete_dir/<int:pk>/', views.delete_dir, name='delete_dir'),
    path('dir_detail/<int:pk>/', views.dir_detail, name='dir_detail'),
    path("add_file/<int:pk>/", views.add_file, name="add_file"),
    path("add_dir/<int:pk>/", views.add_dir, name="add_dir"),
    path('delete_file/<int:pk>/', views.delete_file, name='delete_file'),
    path('file_detail/<int:pk>/', views.file_detail, name='file_detail'),
    path('choose_standard', views.choose_standard, name='choose_standard'),
    path('choose_processor', views.choose_processor, name='choose_processor'),
    path('choose_optimizations', views.choose_optimizations,
         name='choose_optimizations'),
    path('choose_dependant', views.choose_dependant, name='choose_dependant'),
    path('compile/<int:pk>/', views.compile, name='compile')
]
