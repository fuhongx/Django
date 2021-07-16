
from django.contrib import admin
from django.urls import path, include


from App import views

app_name = 'App'
urlpatterns = [
    path('',views.shouye,name='shouye'),
    path('index/',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='resgiter'),
    path('logout/',views.logout,name='logout'),
    path('confirm/', views.user_confirm),


]
