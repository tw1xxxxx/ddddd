from decimal import Decimal
from django.conf import settings
from django.core.cache import cache
from .models import Car, Cart as CartModel, Customer

class Cart:
    def __init__(self, request):
        """Инициализация корзины"""
        self.user_id = request.user.id if request.user.is_authenticated else None
        self.cache_key = f'cart_{self.user_id}' if self.user_id else 'cart_anonymous'

        if self.user_id:
            try:
                customer = Customer.objects.get(user_id=self.user_id)
                cart_items = CartModel.objects.filter(customer=customer)
                self.cart = {
                    str(item.car.id): {
                        'price': str(item.car.price),
                        'model': f"{item.car.model.brand.name} {item.car.model.name}",
                        'vin': item.car.vin
                    } for item in cart_items
                }
            except Customer.DoesNotExist:
                self.cart = {}
        else:
            self.cart = cache.get(self.cache_key, {})

    def add(self, car):
        """Добавление автомобиля в корзину"""
        car_id = str(car.id)
        if car_id not in self.cart:
            self.cart[car_id] = {
                'price': str(car.price),
                'model': f"{car.model.brand.name} {car.model.name}",
                'vin': car.vin
            }
            if self.user_id:
                try:
                    customer = Customer.objects.get(user_id=self.user_id)
                    CartModel.objects.get_or_create(customer=customer, car=car)
                except Customer.DoesNotExist:
                    pass
            else:
                self.save()

    def remove(self, car):
        """Удаление автомобиля из корзины"""
        car_id = str(car.id)
        if car_id in self.cart:
            del self.cart[car_id]
            if self.user_id:
                try:
                    customer = Customer.objects.get(user_id=self.user_id)
                    CartModel.objects.filter(customer=customer, car=car).delete()
                except Customer.DoesNotExist:
                    pass
            else:
                self.save()

    def get_total_price(self):
        """Подсчет общей стоимости"""
        return sum(Decimal(item['price']) for item in self.cart.values())

    def clear(self):
        """Очистка корзины"""
        if self.user_id:
            try:
                customer = Customer.objects.get(user_id=self.user_id)
                CartModel.objects.filter(customer=customer).delete()
            except Customer.DoesNotExist:
                pass
        self.cart = {}
        if not self.user_id:
            self.save()

    def save(self):
        """Сохранение изменений в кэше (только для неавторизованных пользователей)"""
        if not self.user_id:
            cache.set(self.cache_key, self.cart, settings.CART_CACHE_TIMEOUT)

    def __iter__(self):
        """Перебор элементов в корзине и получение автомобилей из базы данных"""
        car_ids = self.cart.keys()
        cars = Car.objects.filter(id__in=car_ids)
        cart = self.cart.copy()
        
        for car in cars:
            cart[str(car.id)]['car'] = car

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        """Подсчет всех товаров в корзине"""
        return len(self.cart) 