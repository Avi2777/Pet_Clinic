from django.urls import path
from .views import login_view, logout_view, CustomSignupView, dashboard_view, landing_view, user_profile_view


app_name = 'core'


urlpatterns = [
    path('', landing_view, name='landing'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', CustomSignupView.as_view(template_name='core/signup.html'), name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/', user_profile_view, name='my_profile'),
]