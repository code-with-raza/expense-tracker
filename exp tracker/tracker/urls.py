from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns=[

path('', views.home_view, name='home'),
path('register/', views.register_view, name='register'),
path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path('add-income/', views.add_income_view, name='add_income'),
path('add-expense/', views.add_expense_view, name='add_expense'),

]