from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views, chart_views


urlpatterns = [
    path('', views.index, name='home_page'),  
    path('initial_views/login_page/', views.login, name='login_page'),
    path('initial_views/signup_page/', views.signup, name='signup_page'),
    path('logged_in_views/user_home_screen/', views.home, name='user_home_screen'),
    path('logged_in_screen/create_account/', views.create_account, name='create_account'),
    path('logged_in_screen/account_selection_deposit/', views.account_selection_deposit, name='account_selection_deposit'),
    path('logged_in_screen/account_selection_withdrawal/', views.account_selection_withdrawal, name='account_selection_withdrawal'),
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('logged_in_screen/close_account/', views.close_account, name='close_account'),
    path('logged_in_screen/transfer_money/', views.transfer_money, name='transfer_money'),
    path('data_display/<int:id>/', chart_views.account_details, name='account_details'),
    path('aggregate-values/<str:account_holder_name>/<str:account_balance_currency>/', chart_views.aggregate_values_display, name='aggregate_values_display'),
]