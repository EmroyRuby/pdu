from django.contrib.auth import login, logout, update_session_auth_hash
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from events import my_permissions
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, PasswordChangeSerializer
from .validations import custom_validation, validate_email, validate_password


class UserRegister(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        try:
            clean_data = custom_validation(request.data)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    ##
    def post(self, request):
        data = request.data
        try:
            assert validate_email(data)
            assert validate_password(data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = serializer.check_user(data)
                login(request, user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    ##
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UserEdit(APIView):
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerOrReadOnlyOrSuperuser]
    authentication_classes = [SessionAuthentication]

    ##
    def put(self, request):
        # Use the UserSerializer to validate the request data
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Return the updated user data
            return Response({'user': serializer.data}, status=status.HTTP_200_OK)

        # If the data is not valid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated, my_permissions.IsOwnerOrReadOnlyOrSuperuser)
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not request.user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            request.user.set_password(serializer.data.get('new_password'))
            request.user.save()
            # Updating the session hash to avoid logging the user out
            update_session_auth_hash(request, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccount(APIView):
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerOrReadOnlyOrSuperuser]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        # Retrieve the authenticated user
        user = request.user
        password = request.data.get('password')

        # If password is not provided, return a bad request
        if not password:
            return Response({"detail": "Password is required to delete account."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if provided password is correct
        if not user.check_password(password):
            return Response({"detail": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user has permissions to delete the account
        if request.user == user or request.user.is_superuser:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # In case the user does not have permission
        return Response({"detail": "You do not have permission to delete this account."}, status=status.HTTP_403_FORBIDDEN)
