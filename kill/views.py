from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from knox.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from kill.models import User, Profile, Product
from kill.serializers import CreateUserSerializer, ProfileSerializer, ProductSerializer

current_format = None


# Create your views here.
class APIRoot(APIView):
    """
    Kill the Brokers API Root
    - lists all the important endpoints of the API
    """

    def get(self, request):
        current_site = get_current_site(request)
        if current_site.name == 'localhost':
            ext = ''
        else:
            ext = 's'
        data = {
            "Auth Endpoints": [
                {
                    "Registration": f"http{ext}://{current_site}/client/register",
                    "Login": f"http{ext}://{current_site}/client/login",
                    "Logout": f"http{ext}://{current_site}/client/logout",
                }
            ],
            "Profile Endpoints": [
                {
                    "Current User Profile": f"http{ext}://{current_site}/client/profile/<id of current user>",
                }
            ],
            "Product Endpoints": [
                {
                    "All Products": f"http{ext}://{current_site}/client/products/all",
                    "Product Details": f"http{ext}://{current_site}/client/products/<id of product>",
                }

            ]
        }
        return Response(data)


class UserCreateView(generics.CreateAPIView):
    """
    Make a POST request with email and password.
    :param request: {"email":"foo@bar.com", "password":"somepassword"}
    :return: a success message if user created.
    """
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['type'] = 1
            serializer.save()
        return Response(serializer.data)


class UserLoginView(LoginView):
    """
    Login User
    - An example POST is {"email":"user@email.com","password":"some_password"}
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, request, format=current_format):
        try:
            email = request.data["email"]
            password = request.data["password"]
            if User.objects.filter(email=email).exists():
                serializer = AuthTokenSerializer(data={"username": email, "password": password})
                serializer.is_valid(raise_exception=True)
                account = serializer.validated_data["user"]
                login(request, account)
                json = super(UserLoginView, self).post(request, format=current_format)
                token = json.data["token"]
                return Response(
                    json.data,
                    status=status.HTTP_201_CREATED,
                    headers={"Authorization": "Token {0}".format(token)},
                )
            else:
                return Response(
                    {"error": "That account doesn't exist in our database"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            print("error is:", e.__str__())
            raise ValidationError(e.__str__(), code='authorization')


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response(
        {"message": "User successfully logged out"},
        status=status.HTTP_200_OK
    )


@api_view(["GET", "POST", "PUT", "DELETE"])
def profile(request, id):
    """
    Gets the profile details of the current user
    You can POST, UPDATE and DELETE the profile/details from here
    :param request:
    :param id: id of current user
    :return: profile details of current user
    """
    user = User.objects.get(id=id)
    if request.method == "GET":
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            profile = Profile.objects.create(user=user, email=user.email)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    if request.method == "PUT":
        return Response()
    if request.method == "POST":
        return Response()
    if request.method == "DELETE":
        return Response()


@api_view(["GET"])
def all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "PUT", "DELETE"])
def product(request, id):
    """
    Gets product detail
    You can POST, UPDATE and DELETE the product from here
    :param request:
    :param id: id of product
    :return: product details
    """
    product = Product.objects.get(id=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        return Response()
    if request.method == "POST":
        return Response()
    if request.method == "DELETE":
        return Response()
