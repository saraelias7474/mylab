from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import User, Category, Authors, Book, Review, Order, OrderItem
from .serializers import (
    UserSerializer,
    CategorySerializer,
    AuthorsSerializer,
    BookSerializer,
    BookListSerializer ,
    ReviewSerializer,
    RegisterSerializer ,
    OrderSerializer,
    OrderItemSerializer
)

class Register( APIView ) :
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post( self , request : Request ) :
        serializer = RegisterSerializer( data = request.data )
        if serializer.is_valid() :
            serializer.save()
            return Response( data = serializer.data , status = status.HTTP_201_CREATED )
        return Response( data = serializer.errors , status = status.HTTP_400_BAD_REQUEST )

class UserView(APIView):
 def get(self,request):
    users=User.objects.all()
    serializer=UserSerializer(users,many=True)
    return Response(serializer.data)
@swagger_auto_schema(request_body=UserSerializer)
def post(self,request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#GET/PUT/DELETE

class UserDetailView(APIView):
  def get_object(self,pk):
    try:
            return User.objects.get(pk=pk)
    except User.DoesNotExist:
            return None

  def get(self,request,pk):
      user=self.get_object(pk)
      if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
      return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)
  @swagger_auto_schema(request_body=UserSerializer)
  def put(self, request, pk):
        user = self.get_object(pk)
        if user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

  def delete(self, request, pk):
        user = self.get_object(pk)
        if user:
            user.delete()
            return Response({"message":"user deleted successfuly"},status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)

######################################################################################
class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=CategorySerializer)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  GET / PUT / DELETE single category
class CategoryDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#########################################################################################################
class AuthorsView(APIView):
    def get(self,request):
        authors=Authors.objects.all()
        serializer=AuthorsSerializer(authors,many=True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=AuthorsSerializer)
    def post(self,request):
          serializer=AuthorsSerializer(data=request.data)
          if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#GET/PUT/DEL
class AuthorsDetailView(APIView):
    def get_object(self,pk):
        return get_object_or_404(Authors,pk=pk)
    def get(self,request,pk):
        authors=self.get_object(pk)
        serializer=AuthorsSerializer(authors)
        return Response(serializer.data)
    def put(self,request,pk):
        authors=self.get_object(pk)
        serializer=AuthorsSerializer(authors,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete (self,request,pk):
        authors=self.get_object(pk)
        authors.delete()
        return Response({'message': 'Author deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    ############################################################################################

class BookView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#GET/PUT/DEL
class BookDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
###################################################################################################
class ReviewView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#GET/PUT/DEL
class ReviewDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Review, pk=pk)

    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = self.get_object(pk)
        review.delete()
        return Response({'message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

######################################################################################################
class OrderView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#GET/PUT/DEL
class OrderDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Order, pk=pk)

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        order.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#####################################################################################################
class OrderItemView(APIView):
    def get(self, request):
        items = OrderItem.objects.all()
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#GET/PUT/DEL
class OrderItemDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(OrderItem, pk=pk)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = OrderItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response({'message': 'Order item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomLoginSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer






# Create your views here.
