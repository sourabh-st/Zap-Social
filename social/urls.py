from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from social import views
from django.conf.urls.static import static


urlpatterns = [
    path('home/',views.profile_get,name='homepage'),
    path('connections/',views.HomeView,name='connections'),
    path('signup',views.Signup.as_view(), name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('feeds', views.feed_view, name='feeds'),

    
    path('follow/<str:username>',views.follow, name="follow"),

    # path('myprofile_edit',views.profile_edit, name='myprofile_edit'),
    path('myprofile',views.profile_get, name='myprofile'),

    path('mypost/create/',views.MyPostCreate.as_view(success_url="/social/home")),
    path('mypost/',views.MyPostListView.as_view()),
    path('mypost/delete/<int:pk>',views.MyPostDeleteView.as_view(success_url="/social/mypost")),
    path('',RedirectView.as_view(url='login')),

]
