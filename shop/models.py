from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        self.phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    GENDER = (
        ('M', "Male"),
        ("F", "Female"),
    )

    USER_TYPES = (
        ('1', 'Customer'),
        ('2', 'Seller')
    )

    username = None
    email = None
    phone = PhoneNumberField(_('phone number'), unique=True)
    image = models.ImageField(upload_to="user-images/", default="default-user.png")
    gender = models.CharField(max_length=100, choices=GENDER)
    type = models.CharField(max_length=100, choices=USER_TYPES)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.phone)


class Book(models.Model):
    BOOK_TYPE = (
        ('Audio', 'E-BOOK'),
        ('Traditional', 'Paper BOOK')
    )

    image = models.ImageField(upload_to="images/books/", blank=True)
    title = models.CharField(max_length=100, null=True)
    price = models.PositiveIntegerField()
    book_type = models.CharField(max_length=100, choices=BOOK_TYPE)
    description = models.TextField()
    author = models.CharField(max_length=100, null=True)
    pub_date = models.DateField()

    def __str__(self):
        return self.title + " | " + str(self.price)


class CartItem(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return "Number of books " + str(self.quantity)

    @property
    def total_price(self):
        return self.book.price * self.quantity

    def remove_cart(self, pk):
        book = Book.objects.get(id=pk)
        book.store_quantity += self.quantity
        book.save()
        super(CartItem, self).remove_cart(pk)


class Cart(models.Model):
    cartItems = models.ManyToManyField(CartItem)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return " | number of books:> " + str(self.customer.phone)

    @property
    def total_price(self):
        total = 0
        for item in self.cartItems.all():
            total += item.total_price
        return total


class Delivery(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Delivered', 'Delivered'),
    )
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=50)
    status = models.CharField(max_length=100, choices=STATUS)

    def __str__(self):
        return self.status + " | " + self.address


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order date at " + str(self.order_date.date()) + " by " + str(self.customer.phone)
