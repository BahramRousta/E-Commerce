from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.token_blacklist.models import (OutstandingToken, BlacklistedToken)
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.utils import Util
from cart.models import Cart, CartItem, Coupon
from cart.serializers import (
    CartItemSerializer,
    CartItemUpdateSerializer, CouponSerializer, CouponPostSerializer, CartSerializer
)
from .custom_permission import (
    ProfileOwnerPermission,
    ChangePasswordPermission
)

from book.serializers import (
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    PublisherSerializer,
    FavoriteBookSerializer
)
from book.models import (
    Author,
    Book,
    Category,
    Publisher,
    FavoriteBook
)
from comment.serializers import CommentSerializer
from comment.models import Comment
from accounts.serializers import (
    ProfileSerializer,
    UserSerializer,
    LogInSerializer,
    ChangePasswordSerializer,
    ResetPasswordRequestEmailSerializer
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


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (ProfileOwnerPermission,)


class FavoriteBookView(APIView):
    permission_classes = ([IsAuthenticated])

    def get_object(self, pk):
        try:
            return FavoriteBook.objects.get(pk=pk)
        except FavoriteBook.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = FavoriteBookSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            book = serializer.validated_data['book']
            user = request.user
            book = Book.objects.filter(title=book).first()

            if book is None:
                return Response(data={'message': 'The information is invalid'},
                                status=status.HTTP_404_NOT_FOUND)

            if FavoriteBook.objects.filter(book=book, user=user).first():
                return Response(data={'message': 'The book is already exists in uor favorite list.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                favorite_book = FavoriteBook.objects.create(book=book, user=user)
                return Response(status=status.HTTP_201_CREATED, data={'book_id': favorite_book.pk})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemView(APIView):

    def get_cart(self, request=None):
        user = request.user
        cart = Cart.objects.get(user_id=user.id)
        return cart

    def get(self, request):
        items = CartItem.objects.filter(cart=self.get_cart(request))
        serializer = CartItemSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            book = serializer.validated_data['book']
            quantity = serializer.validated_data['quantity']

            if CartItem.objects.filter(book_id=book.id, cart=self.get_cart(request)).first():
                return Response(data={'The product is duplicate.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                item = CartItem.objects.create(book=book,
                                               cart=self.get_cart(request),
                                               price=book.price,
                                               quantity=quantity)
                return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=404)

    def patch(self, request, pk):
        serializer = CartItemUpdateSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                quantity = serializer.validated_data['quantity']
                item = CartItem.objects.get(id=pk, cart=self.get_cart(request))
                item.quantity = quantity
                item.save()
                return JsonResponse(serializer.data, status=200)
            except:
                return JsonResponse(serializer.errors, status=404)
        else:
            return JsonResponse(serializer.errors, status=404)

    def delete(self, request, pk, format=None):
        item = CartItem.objects.get(id=pk, cart=self.get_cart(request))
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):

    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        total_price = cart.cart_total_price()
        serializer = CartSerializer(total_price, many=False)
        return Response(data={'total_price': total_price},status=status.HTTP_204_NO_CONTENT)


class CouponView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        coupons = Coupon.objects.filter(cart__user=request.user,
                                        active=True)
        serializer = CouponSerializer(coupons, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        serializer = CouponPostSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                code = serializer.validated_data['code']
                coupon = Coupon.objects.get(code=code,
                                            cart__user=request.user,
                                            active=True)
                cart = Cart.objects.get(coupon=coupon, user=request.user)
                if coupon and cart:
                    total_price = cart.get_total_price_after_discount()
                    coupon.active = False
                    coupon.save()
                    return Response(data={'total_price': total_price})
            except:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.errors)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully registered a new user.'
            data['email'] = user.email
            data['username'] = user.username
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated, ChangePasswordPermission)


class ResetPasswordRequestEmail(GenericAPIView):
    serializer_class = ResetPasswordRequestEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        # try:
        user = User.objects.get(email__exact=email)

        # Generate token
        uid64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(request=request).domain
        relativelink = reverse(
            'password-reset-confirm', kwargs={'uid64': uid64, 'token': token}
        )
        redirect_url = request.data.get('redirect_url', '')
        absurl = 'http://' + current_site + relativelink
        email_body = 'Hello, \n Use link below to reset your password  \n' + \
                     absurl + "?redirect_url=" + redirect_url
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Reset your passsword'}
        Util.send_email(data)

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        # except:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
