from django.contrib import admin
from .models import *

# Модели одежды (существующие)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'color', 'is_exists', 'create_date']
    list_filter = ['is_exists', 'create_date', 'category']
    search_fields = ['name', 'color']
    readonly_fields = ['create_date']

# Модели автосалона
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'description']
    list_filter = ['country']
    search_fields = ['name', 'country']
    readonly_fields = []

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'get_brand_country']
    list_filter = ['brand']
    search_fields = ['name', 'brand__name']
    
    def get_brand_country(self, obj):
        return obj.brand.country
    get_brand_country.short_description = 'Страна марки'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['vin', 'model', 'color', 'price', 'year', 'mileage', 'is_available']
    list_filter = ['is_available', 'year', 'model__brand']
    search_fields = ['vin', 'model__name', 'model__brand__name']
    readonly_fields = []
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('model', 'vin', 'color', 'year')
        }),
        ('Цена и пробег', {
            'fields': ('price', 'mileage')
        }),
        ('Дополнительно', {
            'fields': ('image', 'is_available', 'features')
        }),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'phone', 'address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'phone', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at']
    
    def get_full_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return f"Клиент {obj.id}"
    get_full_name.short_description = 'Имя клиента'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position', 'phone', 'email']
    list_filter = ['position']
    search_fields = ['first_name', 'last_name', 'position', 'email']
    
    fieldsets = (
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'photo')
        }),
        ('Работа', {
            'fields': ('position', 'phone', 'email')
        }),
    )

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['car', 'customer', 'employee', 'sale_date', 'price']
    list_filter = ['sale_date', 'employee']
    search_fields = ['car__vin', 'customer__phone', 'employee__username']
    date_hierarchy = 'sale_date'
    
    fieldsets = (
        ('Продажа', {
            'fields': ('car', 'customer', 'employee', 'sale_date', 'price')
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration']
    search_fields = ['name']
    
    fieldsets = (
        ('Услуга', {
            'fields': ('name', 'description', 'price', 'duration')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'car', 'rating', 'date']
    list_filter = ['rating', 'date']
    search_fields = ['customer__phone', 'car__vin']
    readonly_fields = ['date']
    
    fieldsets = (
        ('Отзыв', {
            'fields': ('customer', 'car', 'rating', 'text', 'date')
        }),
    )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'car', 'added_date']
    list_filter = ['added_date']
    search_fields = ['customer__phone', 'car__vin']
    readonly_fields = ['added_date']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['customer', 'car', 'added_date']
    list_filter = ['added_date']
    search_fields = ['customer__phone', 'car__vin']
    readonly_fields = ['added_date']

@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = ['customer', 'car', 'date', 'status']
    list_filter = ['status', 'date']
    search_fields = ['customer__phone', 'car__vin']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Тест-драйв', {
            'fields': ('customer', 'car', 'date', 'status')
        }),
    )

# Заказы (существующие)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'status', 'get_total_price']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__user__username', 'id']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'car', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['order__id', 'car__vin']
    readonly_fields = ['created_at']