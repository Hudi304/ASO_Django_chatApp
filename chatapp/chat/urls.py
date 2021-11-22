from django.urls import path
from . import views

# ? first place for the dumbest way I spent an hour goes to:
#  ! BAD
# urlpatterns = [
#     path('', views.home, 'home')
# ]

# *  GOOD
urlpatterns = [
    # OK so rdirects in django use the name defined in path or the relative path from root
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('home/', views.home, name='home'),

    path('<str:room>/', views.room, name='room'),
    
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages<str:room>/', views.getMessages, name='getMessages')
]
