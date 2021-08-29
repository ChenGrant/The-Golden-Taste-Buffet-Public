from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_english, name = 'webpage_home_english'),
    path('email_sent/', views.email_sent_english, name = 'email_sent_english'),
    path('email_failed/', views.email_failed_english, name = 'email_failed_english'),
    path('email_cancel/', views.email_cancel_english, name = 'email_cancel_english'),
    path('email_cancel_confirm/', views.email_cancel_confirm_english, name = 'email_cancel_confirm_english'),
    #path('english/', views.home_english, name = 'webpage_home_english'),
    #path('email_sent_english/', views.email_sent_english, name = 'email_sent_english'),
    #path('email_failed_english/', views.email_failed_english, name = 'email_failed_english'),
    #path('email_cancel_english/', views.email_cancel_english, name = 'email_cancel_english'),
    #path('email_cancel_confirm_english/', views.email_cancel_confirm_english, name = 'email_cancel_confirm_english')
]
