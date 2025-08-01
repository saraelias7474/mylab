from rest_framework import serializers
from .models import Category,Authors,Book,Review,Order,OrderItem,User
# from django.contrib.auth.models import User
# #user serializer
class RegisterSerializer( serializers.ModelSerializer ) :
    password = serializers.CharField( write_only = True , style = { "input_type" : "password" } )
    password_confirm = serializers.CharField( write_only = True , style = { "input_type" : "password"})

    class Meta :
        model = User
        fields = [ 'first_name' , 'last_name' , 'email' , 'password' , 'password_confirm' ]

    def validate( self , data ) :
        if data[ 'password' ] != data[ 'password_confirm' ] :
            raise serializers.ValidationError( 'password do not match' )
        return data

    def create( self , validated_data ) :
        validated_data.pop( 'password_confirm' )
        password = validated_data.pop( 'password' )

        user = User.objects.create( **validated_data )
        user.set_password( password )
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name','last_name','email','role']
#category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('category_id','category_name')
#authors serializer
class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Authors
        fields=('author_id','author_name','author_photo')
#book serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=('book_id','ISBN','title','authors','description',
                'price','publication_date','book_cover_photo','availability'
                ,'category','avg_rating','total_reviews','created_at','updated_at')

class BookListSerializer( serializers.ModelSerializer ) :

    authors = AuthorsSerializer(many=True)
    # authors = serializers.SlugRelatedField( read_only = True  , slug_field = 'author_name' , many = True )
    class Meta :
        model = Book
        fields = [ 'book_id' , 'title' , 'authors' , 'price' , 'book_cover_photo',]

#Review serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=('review_id','user','book','rating','review_text')
#Order serializzer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=('order_id','user','order_date','total_price','status')
#OrderItem serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=('order_item_id','order','book','quantity','price')


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        # استدعاء الكود الأصلي لتوليد التوكنات
        data = super().validate(attrs)
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
        }
        return data
