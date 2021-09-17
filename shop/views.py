from django.shortcuts import render
from .models import Book, User, Cart, CartItem, Order, Delivery
from .serializers import BookSerializer, UserSerializer, CartSerializer, CartItemSerializer, OrderSerializer, DeliverySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from .filters import BookFilter
from .responses import ResponseSuccess, ResponseFail




def get_object(model, pk):
    try:
        return model.objects.get(id=pk)
    except:
        return None


class BooksViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Model = Book
        self.Serializer = BookSerializer
        self.Filter = BookFilter
        self.FILTER_FIELDS = [
            'title', 'price', 'book_type', 'author'
        ]


    def list(self, request):
        books = self.Model.objects.all()
        filtered_books = self.Filter(request.GET, queryset=books)
        books = filtered_books.qs
        serializer = BookSerializer(books, many=True)
        return ResponseSuccess(serializer.data, filter_fields=self.FILTER_FIELDS)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        return ResponseFail(serializer.errors)

    def retrieve(self, request, pk):
        query = get_object(self.Model, pk)
        if query:
            serializer = BookSerializer(query, many=False)
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail("Invalid Id was sent!")

    def update(self, request, pk):
        query = get_object(self.Model, pk)
        if query:
            serializer = BookSerializer(query, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseSuccess(serializer.data)
            else:
                return ResponseFail("Invalid Data")
        else:
            return ResponseFail("Invalid Id was sent!")

    def destroy(self, request, pk):
        query = get_object(self.Model, pk)
        if query:
            query.delete()
            return ResponseSuccess(data="Successfully deleted")
        else:
            return ResponseFail("Invalid Id was sent!")


class UserViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Model = User
        self.Serializer = UserSerializer

    def list(self, request):
        books = self.Model.objects.all()
        serializer = UserSerializer(books, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        query = get_object(self.Model, pk)
        if query:
            serializer = UserSerializer(query, many=False)
            return Response(serializer.data)
        else:
            return Response("Invalid Id was sent!")

    def update(self, request, pk):
        query = get_object(self.Model, pk)
        if query:
            serializer = UserSerializer(query, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response("Invalid Data")
        else:
            return Response("Invalid Id was sent!")

    def destroy(self, request, pk):
        query = get_object(self.Model, pk)
        if query:
            query.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Invalid Id was sent!")


class CartItemViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Model = CartItem
        self.Serializer = CartItemSerializer

    def list(self, request):
        cartitems = self.Model.objects.all()
        serializer = CartItemSerializer(cartitems, many=True)
        return ResponseSuccess(serializer.data)


    def create(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)


    def retrieve(self, request, pk):
        cart_item = get_object(self.Model, pk)
        serializer = CartItemSerializer(cart_item)
        return ResponseSuccess(serializer.data)


    def update(self, request, pk):
        cartitem = get_object(self.Model, pk)
        serializer = CartItemSerializer(instance=cartitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)

    def destroy(self, request, pk):
        cart_item = get_object(self.Model, pk)
        if cart_item:
            cart_item.delete()
            return ResponseSuccess(data="Cart items has been deleted!")
        else:
            return ResponseFail(data="Invalid id!")


class CartViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Model = Cart
        self.Serializer = CartSerializer


    def list(self, request):
        queryset = self.Model.objects.all()
        serializer = CartSerializer(queryset, many=True)
        return ResponseSuccess(serializer.data)


    def create(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)

    def retrieve(self, request, pk):
        query = get_object(self.Model, pk)
        serializer = BookSerializer(query, many=False)
        return ResponseSuccess(serializer.data)

    def update(self, request, pk):
        data = get_object(self.Model, pk)
        serializer = BookSerializer(instance=data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(serializer.data)
        else:
            return ResponseFail(serializer.errors)

    def destroy(self, request, pk):
        query = get_object(self.Model, pk)
        if query:
            query.delete()
            return ResponseSuccess(data="Cart has been deleted!")
        else:
            return ResponseFail(data="Invalid id!")


class OrderViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Model = Order
        self.Serializer = OrderSerializer


    def list(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return ResponseSuccess(serializer.data)


    def destroy(self, request, pk):
        order = get_object(self.Model, pk)
        if order:
            order.delete()
            return ResponseSuccess(data="Order has been deleted!")
        else:
            return ResponseFail(data="Invalid Id")


class DeliveryViewSet(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Model = Delivery
        self.Serializer = DeliverySerializer

    def list(self, request):
        queryset = self.Model.objects.all()
        serializer = DeliverySerializer(queryset, many=True)
        return ResponseSuccess(serializer.data)

    def destroy(self, request, pk):
        query = get_object(self.Model, pk)
        if query:
            query.delete()
            return ResponseSuccess(data="Delivery object has been deleted!")
        else:
            return ResponseFail(data="Invalid Id!")