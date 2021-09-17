from django.contrib import admin
from .models import Book, User, Cart, CartItem, Delivery, Order, BookRating, BookReview

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(BookRating)
admin.site.register(BookReview)