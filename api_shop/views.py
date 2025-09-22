from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import *
from .permissions import CustomPermissions, PaginationPage
from shop.models import Car, Brand, Model, Customer, Employee, Sale, TestDrive

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Car.objects.all()
        model = self.request.query_params.get('model', None)
        brand = self.request.query_params.get('brand', None)
        
        if model:
            queryset = queryset.filter(model__icontains=model)
        if brand:
            queryset = queryset.filter(brand__name__icontains=brand)
        
        return queryset

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Brand.objects.all()
        name = self.request.query_params.get('name', None)
        country = self.request.query_params.get('country', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        return queryset

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [AllowAny]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Model.objects.all()
        brand = self.request.query_params.get('brand', None)
        
        if brand:
            queryset = queryset.filter(brand__name__icontains=brand)
        
        return queryset

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Customer.objects.all()
        phone = self.request.query_params.get('phone', None)
        
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        
        return queryset

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Employee.objects.all()
        position = self.request.query_params.get('position', None)
        first_name = self.request.query_params.get('first_name', None)
        last_name = self.request.query_params.get('last_name', None)
        
        if position:
            queryset = queryset.filter(position__icontains=position)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        
        return queryset

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Sale.objects.all()
        car_vin = self.request.query_params.get('car_vin', None)
        customer_phone = self.request.query_params.get('customer_phone', None)
        sale_date = self.request.query_params.get('sale_date', None)
        
        if car_vin:
            queryset = queryset.filter(car__vin__icontains=car_vin)
        if customer_phone:
            queryset = queryset.filter(customer__phone__icontains=customer_phone)
        if sale_date:
            queryset = queryset.filter(sale_date=sale_date)
        
        return queryset

class TestDriveViewSet(viewsets.ModelViewSet):
    queryset = TestDrive.objects.all()
    serializer_class = TestDriveSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = TestDrive.objects.all()
        car_vin = self.request.query_params.get('car_vin', None)
        customer_phone = self.request.query_params.get('customer_phone', None)
        status = self.request.query_params.get('status', None)
        date = self.request.query_params.get('date', None)
        
        if car_vin:
            queryset = queryset.filter(car__vin__icontains=car_vin)
        if customer_phone:
            queryset = queryset.filter(customer__phone__icontains=customer_phone)
        if status:
            queryset = queryset.filter(status=status)
        if date:
            queryset = queryset.filter(date__date=date)
        
        return queryset 