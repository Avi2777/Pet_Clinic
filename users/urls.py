from django.urls import path
from .views import ProfileUpdateView, ProfileDeleteView

app_name = 'users'


urlpatterns = [
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('user_delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile_delete'),

]