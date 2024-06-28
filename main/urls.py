from django.urls import path
from main import views
from .views import (UserRegistrationAPIView,UserLoginAPIView,LogoutView,
                    UserProfileAPIView,PasswordResetRequestView, PasswordResetView,OwnerRegistrationView,
                    ChangePasswordView,CustomTokenObtainPairView
                    )

urlpatterns = [

   path('user-register/', UserRegistrationAPIView.as_view(), name='register-user'),
   path('owner-register/', OwnerRegistrationView.as_view(), name='owner-user'),
   path('login/', UserLoginAPIView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
   path('reset-password/<uidb64>/<token>/', PasswordResetView.as_view(), name='password_reset_confirm'),
   path('change-password/', ChangePasswordView.as_view(), name='change-password'),
   path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
   path('token/',views.csrf_token_view , name='csrf-tocken'),
   path('dropdown/list/',views.property_dropdown , name='dropdown'),
   path('filters/',views.filter_set , name='get-filters'),
   path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
   
]
