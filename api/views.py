from django.contrib import auth
from django.contrib.auth import login
from rest_framework import generics, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .custom_permission import IsOwner

from book.serializers import (
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    PublisherSerializer
)
from book.models import (
    Author,
    Book,
    Category,
    Publisher
)
from comment.serializers import CommentSerializer
from comment.models import Comment
from accounts.serializers import (
    ProfileSerializer,
    UserSerializer,
    LogInSerializer
)
from accounts.models import Profile


@csrf_exempt
@api_view(['GET', 'POST'])
def books_list(request):
    if request.method == 'GET':
        books = Book.objects.filter(available=True)
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=404)


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class NewPublishBookView(generics.ListAPIView):
    queryset = Book.objects.filter(new_publish=True)
    serializer_class = BookSerializer


class BestSellerBookView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('count_sold')[:8]
    serializer_class = BookSerializer


@api_view(http_method_names=['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def authors_list(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=404)


class BookCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class BookPublisherView(generics.ListAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class SearchView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name', 'category__name', 'publisher__name']


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UserProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwner,)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully registered a new user.'
            data['email'] = user.email
            data['username'] = user.username

            return Response(data)
        else:
            data = serializer.errors
        return Response(data)


class LogInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = auth.authenticate(username=username,
                                     password=password)
            if user is None:
                raise AuthenticationFailed("User Not Found")

            login(request, user)
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access_token': str(refresh.access_token)
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class LogOut(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_205_RESET_CONTENT)
