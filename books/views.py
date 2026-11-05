from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import (
    BookSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)


def csrf_failure(request, reason=""):
    """Called by Django when a CSRF check fails on a non-DRF view (register/login)."""
    return JsonResponse({"detail": f"CSRF Failed: {reason}"}, status=403)


# --- Utility endpoints -----------------------------------------------------

@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok"})


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    """
    Hands out a CSRF token.  Calling get_token() also makes Django set the
    'csrftoken' cookie on the response.
    """
    return Response({"csrfToken": get_token(request)})


@api_view(["GET"])
def me(request):
    """Who am I?  Needs a valid session, otherwise 401."""
    return Response(UserSerializer(request.user).data)


# --- Authentication endpoints ----------------------------------------------
# Register and login are used by people who are NOT logged in yet, so DRF's
# session authentication would not check CSRF for them. We switch the check
# on explicitly with csrf_protect, so ALL unsafe requests need a token.

@method_decorator(csrf_protect, name="dispatch")
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # -> 400 with field errors
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            # Same message for "no such user" and "wrong password" on purpose.
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)  # creates the server-side session + Set-Cookie
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    # Default permission (IsAuthenticated) and default session authentication
    # (which enforces CSRF) apply here.
    def post(self, request):
        logout(request)  # deletes the server-side session
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Book endpoints --------------------------------------------------------

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.select_related("owner")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetailView(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.select_related("owner")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrStaffOrReadOnly]