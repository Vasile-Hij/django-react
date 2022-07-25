from django.urls import path
from base.views import user_views as views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register/', views.registerUser, name='register'),

    # user paths
    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"),
    path('update/<str:pk>/', views.updateUser, name='user-update'),
   
    # admin paths
    path('all/', views.getUsers, name="users"),
    path('<str:pk>/', views.getUserById, name='user'),
    path('delete/<str:pk>/', views.deleteUser, name='user-delete'),
]