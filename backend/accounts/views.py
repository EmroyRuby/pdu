from django.contrib.auth import login, logout, update_session_auth_hash
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from events import my_permissions
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, PasswordChangeSerializer


class UserRegister(APIView):
    """
    post:
    Register a new user.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Create a new user account with email, username, and password.",
        request_body=UserRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: UserRegisterSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid input"
        },
        tags=['User Authentication']
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # Include 'id' in the response data
            response_data = serializer.data
            response_data['id'] = user.user_id
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    post:
    Authenticate a user and start a session.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        operation_description="Login a user.",
        request_body=UserLoginSerializer,
        responses={
            status.HTTP_200_OK: '{"id": "User ID", "email": "User Email", "username": "Username"}',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
        },
        tags=['User Authentication'],
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            login(request, user)
            # Include 'id' in the response data
            return Response({'id': user.user_id, 'email': user.email, 'username': user.username},
                            status=status.HTTP_200_OK)


class UserLogout(APIView):
    """
    post:
    End a user's session.
    """

    permission_classes = (permissions.AllowAny,)
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        operation_description="Logout a user.",
        responses={status.HTTP_200_OK: 'Successfully logged out.'},
        tags=['User Authentication'],
    )
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    """
    get:
    Retrieve the currently logged in user's information.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        operation_description="Get the current user's details.",
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_403_FORBIDDEN: 'Forbidden',
        },
        tags=['User Profile'],
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserEdit(APIView):
    """
    put:
    Update the currently logged in user's information.
    """
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerOrReadOnlyOrSuperuser]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        operation_description="Update current user's details.",
        request_body=UserSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
        },
        tags=['User Profile'],
    )
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
    """
    post:
    Change the password for the currently logged in user.
    """
    permission_classes = (permissions.IsAuthenticated, my_permissions.IsOwnerOrReadOnlyOrSuperuser)
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        operation_description="Change password for the current user.",
        request_body=PasswordChangeSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: 'Password changed successfully.',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
        },
        tags=['User Profile'],
    )
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
    """
    post:
    Delete the currently logged in user's account.
    """
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerOrReadOnlyOrSuperuser]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        operation_description="Delete the current user's account.",
        responses={
            status.HTTP_204_NO_CONTENT: 'Account deleted successfully.',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_403_FORBIDDEN: 'Forbidden',
        },
        tags=['User Profile'],
    )
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
        return Response({"detail": "You do not have permission to delete this account."},
                        status=status.HTTP_403_FORBIDDEN)
