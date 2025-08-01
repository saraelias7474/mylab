from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password


from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # extra_fields.setdefault('username', email)  # لتجنب خطأ username فارغ
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    username = None
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='user')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name' , 'last_name' ]
    # Override default fields to match ERD naming
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True )
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True)

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True
    )
    objects=UserManager()
    class Meta:
        db_table = 'users'
        ordering = ['first_name', 'last_name']
    def save(self, *args, **kwargs):
        # إذا المستخدم جديد أو تم تغيير الباسورد كنص عادي → شفره تلقائيًا
        if self.pk is None or not self.password.startswith('pbkdf2'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Category Model - Following ERD specifications
class Category(models.Model):

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'categories'
        ordering = ['category_name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

class Authors(models.Model):

    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=255)
    author_photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    class Meta:
        db_table = 'authors'
        ordering = ['author_name']

    def __str__(self):
        return self.author_name



# Book Model - Following ERD specifications
class Book(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]

    book_id = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(Authors,  related_name='books')
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    publication_date = models.DateField()
    book_cover_photo = models.ImageField(upload_to='covers/')
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='in_stock'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    avg_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['avg_rating']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
            authors_names = ", ".join([author.author_name for author in self.authors.all()])
            return f"{self.title} - {authors_names}"

    @property
    def is_available(self):
        """Check if book is available for purchase"""
        return self.quantity > 0

    # @property
    # def is_digital(self):
    #     """Check if book is in digital format"""
    #     return self.format in ['PDF', 'EPUB', 'MOBI']

    def update_rating(self):
        """
        Update average rating and total reviews count
        Call this method when reviews are added/updated/deleted
        """
        reviews = self.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            self.avg_rating = total_rating / reviews.count()
            self.total_reviews = reviews.count()
        else:
            self.avg_rating = 0.00
            self.total_reviews = 0
        self.save(update_fields=['avg_rating', 'total_reviews'])



# Review Model - Following ERD specifications
class Review(models.Model):
    """
    Book reviews by users
    Fields from ERD: review_id (PK), user_id (FK), book_id (FK), rating, review_text
    """
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()


    class Meta:
        db_table = 'reviews'
        unique_together = ('user', 'book')  # One review per user per book

        indexes = [
            models.Index(fields=['book', 'rating']),
        ]

    def __str__(self):
        return f'{self.user.email} - {self.book.title} ({self.rating}/5)'

    def save(self, *args, **kwargs):
        """Override save to update book rating automatically"""
        super().save(*args, **kwargs)
        self.book.update_rating()

    def delete(self, *args, **kwargs):
        """Override delete to update book rating automatically"""
        book = self.book
        super().delete(*args, **kwargs)
        book.update_rating()

# Order Model - Following ERD specifications
class Order(models.Model):
    """
    Customer orders
    Fields from ERD: order_id (PK), user_id (FK), order_date, total_price, status
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')


    class Meta:
        db_table = 'orders'
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['order_date']),
        ]

    def __str__(self):
        return f'Order {self.order_id} by {self.user.email}'

    @property
    def items_count(self):
        """Get total number of items in this order"""
        return self.items.count()

    @property
    def can_be_cancelled(self):
        """Check if order can be cancelled"""
        return self.status in ['pending', 'confirmed']

# Order Items Model - Following ERD specifications
class OrderItem(models.Model):
    """
    Items within an order
    Fields from ERD: order_item_id (PK), order_id (FK), book_id (FK), quantity, price
    """
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    class Meta:
        db_table = 'order_items'
        indexes = [
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return f'{self.book.title} x{self.quantity}'

    @property
    def total_price(self):
        """Calculate total price for this order item"""
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        """Set price to current book price if not provided"""
        if not self.price:
            self.price = self.book.price
        super().save(*args, **kwargs)

# Create your models here.
