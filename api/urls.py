from django.urls import path

from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # User URLs
    path( 'register/' , Register.as_view() , name = 'register-user' ) ,
    path( 'login/' , CustomLoginView.as_view() , name = 'login') ,
    path('users/', UserView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('category/', CategoryView.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('authors/', AuthorsView.as_view(), name='authors-list'),
    path('authors/<int:pk>/', AuthorsDetailView.as_view(), name='authors-detail'),
    path('books/', BookView.as_view(), name='books-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='books-detail'),
    path('review/', ReviewView.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('order/', OrderView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orderItems/', OrderItemView.as_view(), name='orderItems-list'),
    path('orderItems/<int:pk>/', OrderItemDetailView.as_view(), name='orderItems-detail'),

            ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
