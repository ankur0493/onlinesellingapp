from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from rest_framework import views, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import LoginSerializer, SignupSerializer
from seller.models import Seller


class LoginAPIView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            password = serializer.data['password']
            if not email:
                return Response({'success': 'false', 'message': 'Email is Required'},
                                status=status.HTTP_401_UNAUTHORIZED)
            user = authenticate(email=email.lower(), password=password)
            if user:
                login(request, user)
                data = {
                    'email': user.email,
                    'id': user.id
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response({
                'success': 'false',
                'message': 'Username/Password combination is invalid'
                }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(views.APIView):
    permissions_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'success': 'true', 'status': status.HTTP_200_OK})


class SignupAPIView(views.APIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if User.objects.filter(email=serializer.data['email'].lower()).exists():
                message = _('This user already exists')
                raise ValidationError(message)
            if serializer.data['password'] != serializer.data['confirm_password']:
                message = _("'Password' and 'Confirm Password' should be same")
                raise ValidationError(message)
            try:
                user = User.objects.create(
                           email=serializer.data['email'].lower(),
                           username=serializer.data['email'].lower())
                user.set_password(serializer.data['password'])
                seller = Seller.objects.create(user=user, communication_email=user.email)
                data = {
                    'email': user.email,
                    'username': user.username,
                    'id': user.id
                }
                return Response(data, status=status.HTTP_200_OK)
            except Exception, e:
                return Response({'message': 'Some error occured. Please contact support team'},
                                status=status.HTTP_400_BAD_REQUEST)
