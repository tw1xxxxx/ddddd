from rest_framework import serializers
from django.contrib.auth.models import User
from shop.models import Car, Brand, Customer, Employee, Sale, TestDrive, Model

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country', 'description', 'logo']

class ModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), write_only=True, source='brand')

    class Meta:
        model = Model
        fields = ['id', 'name', 'brand', 'brand_id']

class CarSerializer(serializers.ModelSerializer):
    model = ModelSerializer(read_only=True)
    model_id = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all(), write_only=True, source='model')

    class Meta:
        model = Car
        fields = ['id', 'model', 'model_id', 'vin', 'color', 'price', 'mileage', 'image', 'is_available', 'year', 'features']

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='user', required=False)
    
    class Meta:
        model = Customer
        fields = ['id', 'user', 'user_id', 'phone', 'address', 'created_at']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'position', 'phone', 'email', 'photo']

class SaleSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    employee = serializers.StringRelatedField(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True, source='car')
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, source='customer')
    employee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='employee', required=False)

    class Meta:
        model = Sale
        fields = ['id', 'car', 'car_id', 'customer', 'customer_id', 'employee', 'employee_id', 'sale_date', 'price']

class TestDriveSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True, source='car')
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, source='customer')

    class Meta:
        model = TestDrive
        fields = ['id', 'car', 'car_id', 'customer', 'customer_id', 'date', 'status'] 