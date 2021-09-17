from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("books", views.BooksViewSet, basename="books")
router.register("users", views.UserViewSet, basename="users")
router.register('add_to_cart', views.CartItemViewSet, basename="add_to_cart")
router.register("cart", views.CartViewSet, basename="cart")
router.register("orders", views.OrderViewSet, basename="orders")
router.register("delivery", views.DeliveryViewSet, basename="delivery")

urlpatterns = [
    path('api/', include(router.urls))
]