from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

MAX_LENGTH = 255

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    

    





class Collection(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'



class Clothes(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='цена')
    color = models.CharField(max_length=MAX_LENGTH, verbose_name='цена')
    min_size = models.PositiveIntegerField(default=36, verbose_name='минимальный размер')
    max_size = models.PositiveIntegerField(default=52, verbose_name='максимальный размер')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления на сайт')
    is_exists = models.BooleanField(default=True, verbose_name='в наличии?')



    collection = models.ManyToManyField(Collection, verbose_name='Коллекция')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f'{self.name} - {self.price} руб'
    
    class Meta:
        verbose_name = 'Одежда'
        verbose_name_plural = 'Вещи'
    

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название марки')
    country = models.CharField(max_length=100, verbose_name='Страна производитель')
    description = models.TextField(verbose_name='Описание')
    logo = models.ImageField(upload_to='brands/', verbose_name='Логотип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Марка')
    name = models.CharField(max_length=100, verbose_name='Название модели')

    def __str__(self):
        return f"{self.brand.name} {self.name}"

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

class Car(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name='Модель')
    vin = models.CharField(max_length=17, unique=True, verbose_name='VIN номер')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    mileage = models.IntegerField(verbose_name='Пробег')
    image = models.ImageField(upload_to='cars/', verbose_name='Фото автомобиля')
    is_available = models.BooleanField(default=True, verbose_name='Доступен для продажи')
    year = models.IntegerField(verbose_name='Год выпуска', default=2024)
    features = models.TextField(verbose_name='Особенности', blank=True)

    def __str__(self):
        return f"{self.model} - {self.vin}"

    def get_absolute_url(self):
        return reverse('car_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return f"Customer {self.id}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Employee(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    position = models.CharField(max_length=100, verbose_name='Должность')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    photo = models.ImageField(upload_to='employees/', verbose_name='Фото')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class Sale(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сотрудник', limit_choices_to={'is_staff': True}, null=True, blank=True)
    sale_date = models.DateField(verbose_name='Дата продажи')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи')

    def __str__(self):
        return f"Продажа {self.car} клиенту {self.customer}"

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    duration = models.DurationField(verbose_name='Длительность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    rating = models.IntegerField(verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    date = models.DateField(auto_now_add=True, verbose_name='Дата отзыва')

    def __str__(self):
        return f"Отзыв от {self.customer} на {self.car}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    added_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f"{self.customer} - {self.car}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    added_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f"{self.customer} - {self.car}"

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

class TestDrive(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    date = models.DateTimeField(verbose_name='Дата и время')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен')
    ], default='pending', verbose_name='Статус')

    def __str__(self):
        return f"Тест-драйв {self.car} клиентом {self.customer}"

    class Meta:
        verbose_name = 'Тест-драйв'
        verbose_name_plural = 'Тест-драйвы'

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'В обработке'),
            ('confirmed', 'Подтвержден'),
            ('completed', 'Завершен'),
            ('cancelled', 'Отменен')
        ],
        default='pending',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ №{self.id} от {self.created_at.strftime("%d.%m.%Y")}'

    def get_total_price(self):
        return sum(item.price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.car.model.brand.name} {self.car.model.name} в заказе №{self.order.id}'
