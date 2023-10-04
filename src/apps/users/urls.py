from django.urls import include, path

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api.views import RegisterOwnerAPIClient, VerifyNewAccountAPIView, \
    GetAuthRecoverCodeAPIView, VerifyRecoverCodeAPIView, CreateNewPasswordAPIView, \
        SignInAPIView, LogoutAPIView, RefreshTokenAPIView


urlpatterns = [ 
    path('sign-in/', SignInAPIView.as_view(), name='sign-in'),
    path('sign-up/', RegisterOwnerAPIClient.as_view(), name='sign-up'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='refresh-token'),
    path('sign-up/verify/', VerifyNewAccountAPIView.as_view(), name='verify_registration_code'),
    path('recover/get-code/', GetAuthRecoverCodeAPIView.as_view(), name='recover_get_code'),
    path('recover/check-code/', VerifyRecoverCodeAPIView.as_view(), name='recover_check_code'),
    path('recover/edit-password/', CreateNewPasswordAPIView.as_view(), name='recover_edit_password'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout')
]