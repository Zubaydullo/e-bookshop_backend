from rest_framework import serializers
from .models import Book, User, Cart, CartItem, Order, Delivery


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


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
        depth=1


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"
        depth=4
