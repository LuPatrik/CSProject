from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('bank_account/', views.bank_account, name='bank_account'),
    path('logout/', views.logout, name='logout'),
    path('search-vulnerable/', views.search_users, name='search_vulnerable'),
    path('transfer_money/', views.transfer_money, name='transfer_money'),
]
