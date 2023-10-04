import logging
from rest_framework import serializers, status
from rest_framework.response import Response
from apps.users.exceptions import UserException, UserVerificationFailed
# from apps.multilanding.ecxeptions import UserException
from apps.utils import get_or_none
from randevu.errors import safe_run, safe_api

from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.users.api.serializers import OwnerCreateSerializer, OwnerAccountVerifySerializer, UserJWTSerializer, \
                                        UserRecoveryCodeSerializer, UserRecoveryVerifyCodeSerializer, NewUserPasswordSerializer, \
                                            UserSiginSerializer, LogoutSerializer, RefreshJWTSerializer
from apps.users.models import User, AsyncCodeOperation
from apps.users.services import OwnerCreator, RecoveryCodeSender

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model

from rest_framework_simplejwt.tokens import RefreshToken, Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


logger = logging.getLogger()


class RefreshTokenAPIView(generics.CreateAPIView):
    serializer_class = RefreshJWTSerializer

    @swagger_auto_schema(responses={201: openapi.Response('Refresh Token', RefreshJWTSerializer)})
    @safe_run()
    def post(self, request):
        data = request.data
        serializer = UserSiginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, email=serializer.validated_data['login'])
        if make_password(user.password) != serializer.validated_data['password']:
            raise UserException('Wrong password')

        if user.email != serializer.validated_data['login']:
            raise UserException('Wrong login')

        if user.name != serializer.validated_data['name']:
            raise UserException('Wrong full name')

        refresh = RefreshToken.for_user(user)
        response_serializer = UserJWTSerializer(data={
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'pkid': user.pkid
        })
        response_serializer.is_valid(raise_exception=False)

        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.CreateAPIView):
    serializer_class = LogoutSerializer

    @safe_run()
    def post(self, request):
        try:
            serializer = LogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            refresh_token = serializer.validated_data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SignInAPIView(generics.CreateAPIView):
    serializer_class = UserSiginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: openapi.Response('Sign In', UserJWTSerializer)})
    @safe_api
    def post(self, request):
        data = request.data
        serializer = UserSiginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        authenticate_kwargs = {
            'email': serializer.validated_data['login'],
            "password": serializer.validated_data['password'],
        }
        try:
            authenticate_kwargs["request"] = request
        except KeyError:
            pass

        user = authenticate(**authenticate_kwargs)

        if not user:
            raise UserException('Password or login are incorrect.', x_code=200, status_code=401)

        refresh = RefreshToken.for_user(user)
        response_serializer = UserJWTSerializer(data={
            'user_role': user.role,
            'user_id': user.pkid,
            'jwt': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role
        })
        response_serializer.is_valid(raise_exception=False)

        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


class RegisterOwnerAPIClient(generics.CreateAPIView):
    serializer_class = OwnerCreateSerializer

    @swagger_auto_schema(responses={201: None})
    @safe_run()
    # @safe_run(exceptions=(SubdomainIsAlreadyUsed, IncorrectSubDomain))
    def post(self, request):
        data = request.data
        serializer = OwnerCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.pop('login')

        OwnerCreator(email=email, **serializer.validated_data)()

        return Response(status=status.HTTP_201_CREATED)
    
    
class VerifyNewAccountAPIView(generics.CreateAPIView):
    serializer_class = OwnerAccountVerifySerializer

    @swagger_auto_schema(responses={200: openapi.Response('Verify', UserJWTSerializer)})
    @safe_run(exceptions=(UserException, UserVerificationFailed))
    def post(self, request):
        serializer = OwnerAccountVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        user = get_object_or_404(User, email=data['login'])
    
        if user.is_active == True:
            raise UserVerificationFailed(text="User alredy veryfied")
                
        user_data = None
        for operation in user.get_async_operations():
            if operation.code == data['code']:
                refresh = RefreshToken.for_user(user)
                user.is_active = True
                user.save()

                operation.status = AsyncCodeOperation.SUCCEED
                operation.save()

                user_data = {
                    'jwt': str(refresh.access_token),
                    'refresh': str(refresh),
                    'pkid': user.pkid,
                    'role': user.role,
                    'user_id': user.pkid
                }
            
        if not user_data:
            raise UserVerificationFailed(text="Verification code cannot be matched.", x_code='x004')

        res_serializer = UserJWTSerializer(data=user_data)
        res_serializer.is_valid(raise_exception=True)

        return Response(data=res_serializer.data, status=status.HTTP_200_OK)
    
    
class GetAuthRecoverCodeAPIView(generics.CreateAPIView):
    serializer_class = UserRecoveryCodeSerializer
    
    @swagger_auto_schema(responses={200: None})
    @safe_run(exceptions=(UserException, ))
    def post(self, request):
        serializer = UserRecoveryCodeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        
        RecoveryCodeSender(serializer.validated_data['login'])()
        return Response(status=status.HTTP_200_OK)
    
    
class VerifyRecoverCodeAPIView(generics.CreateAPIView):
    serializer_class = UserRecoveryVerifyCodeSerializer
    
    @swagger_auto_schema(responses={200: None})
    @safe_run(exceptions=(UserException, ))
    def post(self, request):
        serializer = UserRecoveryVerifyCodeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        
        logger.info(f'Recovery password code verifying. {timezone.now()}')
        operation = get_or_none(AsyncCodeOperation, code=serializer.validated_data['code'], expire_date__gt=timezone.now())
        
        if not operation:
            raise UserVerificationFailed(text="Verification code cannot be matched.", x_code='x004')

        return Response(status=status.HTTP_200_OK)
    

class CreateNewPasswordAPIView(generics.CreateAPIView):
    serializer_class = NewUserPasswordSerializer
    
    @swagger_auto_schema(responses={200: None})
    @safe_run(exceptions=(UserException, ))
    def post(self, request):
        serializer = NewUserPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        logger.info('Edit new password.')

        email = serializer.validated_data['login'] 
        password = serializer.validated_data['password']   

        user = get_or_none(User, email=email)

        if not user:
            raise UserException(text=f"User with {email} doesn't exist.", x_code='x006')
        
        user.set_password(password)
        user.save()
    
        # send confirmation email

        return Response(status=status.HTTP_200_OK)
