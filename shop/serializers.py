from rest_framework import serializers
from .models import Book, User, Cart, CartItem, Order, Delivery, BookReview, BookRating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = "__all__"
        depth = 0


class BookReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookReview
        fields = "__all__"
        depth = 0


class BookSerializer(serializers.ModelSerializer):
    book_rates = serializers.SerializerMethodField()
    book_reviews = serializers.SerializerMethodField()
    book_type = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('image', 'title','book_type', 'price', 'description', 'author', 'pub_date', 'book_rates', 'book_reviews')
        depth = 3


    def get_book_rates(self, obj):
        rates = BookRating.objects.filter(book=obj).distinct()
        return BookRatingSerializer(rates, many=True).data


    def get_book_reviews(self, obj):
        reviews = BookReview.objects.filter(book=obj)
        return BookReviewSerializer(reviews, many=True).data


    def get_book_type(self, obj):
        types_dict = {}
        if obj.audio:
            types_dict['audio'] = obj.audio
        if obj.electronic:
            types_dict['electronic'] = obj.electronic
        if obj.paper:
            types_dict['paper'] = obj.paper
        return types_dict


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"
        depth = 2


    def get_total_price(self, obj):
        total = 0
        for item in obj.cartItems.all():
            total += item.total_price
        return total


class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False)
    class Meta:
        model = CartItem
        depth = 0


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 3


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"
        depth = 4
