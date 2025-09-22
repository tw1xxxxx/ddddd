from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.utils import timezone
from .cart import Cart
from .models import Order, OrderItem

def is_admin(user):
    return user.is_authenticated and user.is_staff

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

@login_required
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

def how_to_find(request):
    return render(request, 'how_to_find.html')

def faq(request):
    return render(request, 'faq.html')

def support(request):
    return render(request, 'support.html')

def products(request):
    return render(request, 'products.html')

def categories(request):
    return render(request, 'categories.html')

def all_products(request):
    return render(request, 'all_products.html')

def cart(request):
    return render(request, 'cart.html')

class ClothesListView(ListView):
    model = Clothes
    template_name = 'clothes/clothes_list.html'
    context_object_name = 'clothes'

class ClothesDetailView(DetailView):
    model = Clothes
    template_name = 'clothes/clothes_detail.html'
    context_object_name = 'clothes'

class ClothesCreateView(CreateView):
    model = Clothes
    form_class = ClothesForm
    template_name = 'clothes/clothes_form.html'
    success_url = reverse_lazy('clothes_list')

class ClothesUpdateView(UpdateView):
    model = Clothes
    form_class = ClothesForm
    template_name = 'clothes/clothes_form.html'
    success_url = reverse_lazy('clothes_list')

class ClothesDeleteView(DeleteView):
    model = Clothes
    template_name = 'clothes/clothes_delete.html'
    success_url = reverse_lazy('clothes_list')

# Представления для Car
class CarListView(ListView):
    model = Car
    template_name = 'car/car_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        return Car.objects.select_related('model', 'model__brand').all()

class CarDetailView(DetailView):
    model = Car
    template_name = 'car/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = Customer.objects.get(user=self.request.user)
            cart = Cart(self.request)
            context['in_cart'] = str(self.object.id) in cart.cart
            context['in_wishlist'] = Wishlist.objects.filter(customer=customer, car=self.object).exists()
        return context

class CarCreateView(AdminRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car/car_form.html'
    success_url = reverse_lazy('car_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        return context

class CarUpdateView(AdminRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car/car_form.html'
    success_url = reverse_lazy('car_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            if 'instance' in kwargs:
                car = kwargs['instance']
                if car.model:
                    kwargs['initial'] = {
                        'brand': car.model.brand.id,
                        'model': car.model.id
                    }
        return kwargs

class CarDeleteView(AdminRequiredMixin, DeleteView):
    model = Car
    template_name = 'car/car_delete.html'
    success_url = reverse_lazy('car_list')

class BrandListView(ListView):
    model = Brand
    template_name = 'brand/brand_list.html'
    context_object_name = 'brands'

    def get_queryset(self):
        return Brand.objects.prefetch_related('model_set').all()

class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brand/brand_detail.html'
    context_object_name = 'brand'

class BrandCreateView(AdminRequiredMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brand/brand_form.html'
    success_url = reverse_lazy('brand_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_form'] = self.get_form()
        context['model_form'] = ModelForm()
        return context

    def form_valid(self, form):
        brand = form.save()
        model_name = self.request.POST.get('model_name')
        if model_name:
            Model.objects.create(brand=brand, name=model_name)
        return super().form_valid(form)

class BrandUpdateView(AdminRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brand/brand_form.html'
    success_url = reverse_lazy('brand_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.get_object()
        context['brand_form'] = self.get_form()
        if brand.model_set.exists():
            context['model_form'] = ModelForm(instance=brand.model_set.first())
        else:
            context['model_form'] = ModelForm()
        return context

    def form_valid(self, form):
        brand = form.save()
        model_name = self.request.POST.get('model_name')
        if model_name:
            if brand.model_set.exists():
                model = brand.model_set.first()
                model.name = model_name
                model.save()
            else:
                Model.objects.create(brand=brand, name=model_name)
        return super().form_valid(form)

class BrandDeleteView(AdminRequiredMixin, DeleteView):
    model = Brand
    template_name = 'brand/brand_delete.html'
    success_url = reverse_lazy('brand_list')

class CustomerListView(AdminRequiredMixin, ListView):
    model = Customer
    template_name = 'customer/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.filter(user__is_staff=False)

class CustomerDetailView(AdminRequiredMixin, DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'
    context_object_name = 'customer'

class CustomerCreateView(AdminRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_form.html'

    def get_object(self, queryset=None):
        if self.kwargs.get('pk'): 
            return get_object_or_404(Customer, pk=self.kwargs['pk'])
        return self.request.user.customer  

    def get_success_url(self):
        if self.kwargs.get('pk'):  
            return reverse_lazy('customer_list')
        return reverse_lazy('account')  

class CustomerDeleteView(AdminRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customer/customer_delete.html'
    success_url = reverse_lazy('customer_list')

class EmployeeListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return User.objects.filter(is_staff=True)

class EmployeeDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'

    def get_queryset(self):
        return User.objects.filter(is_staff=True)

class EmployeeCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'employee/employee_form.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True
        user.save()
        return super().form_valid(form)

class EmployeeUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    template_name = 'employee/employee_form.html'
    success_url = reverse_lazy('employee_list')
    fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser']

    def get_queryset(self):
        return User.objects.filter(is_staff=True)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True  
        user.save()
        return super().form_valid(form)

class EmployeeDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'employee/employee_delete.html'
    success_url = reverse_lazy('employee_list')

    def get_queryset(self):
        return User.objects.filter(is_staff=True)

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/sale_list.html'
    context_object_name = 'sales'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Sale.objects.all()
        return Sale.objects.filter(customer__user=self.request.user)

class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sale/sale_detail.html'
    context_object_name = 'sale'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Sale.objects.all()
        return Sale.objects.filter(customer__user=self.request.user)

class SaleCreateView(AdminRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/sale_form.html'
    success_url = reverse_lazy('sale_list')

class SaleUpdateView(AdminRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/sale_form.html'
    success_url = reverse_lazy('sale_list')

class SaleDeleteView(AdminRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/sale_delete.html'
    success_url = reverse_lazy('sale_list')

class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'cart/cart_list.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        try:
            customer = Customer.objects.get(user=self.request.user)
            return Cart.objects.filter(customer=customer)
        except Customer.DoesNotExist:
            return Cart.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        context['total_price'] = sum(item.car.price for item in cart_items)
        return context

class TestDriveListView(LoginRequiredMixin, ListView):
    model = TestDrive
    template_name = 'testdrive/testdrive_list.html'
    context_object_name = 'testdrive_items'

    def get_queryset(self):
        return TestDrive.objects.filter(customer__user=self.request.user)

@login_required
def add_to_wishlist(request, pk):
    car = get_object_or_404(Car, pk=pk)
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if not Wishlist.objects.filter(customer=customer, car=car).exists():
        Wishlist.objects.create(customer=customer, car=car)
        messages.success(request, 'Автомобиль добавлен в избранное')
    else:
        messages.info(request, 'Автомобиль уже в избранном')
    
    return redirect('car_list')

@login_required
def add_to_cart(request, pk):
    car = get_object_or_404(Car, pk=pk)
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if not Cart.objects.filter(customer=customer, car=car).exists():
        Cart.objects.create(customer=customer, car=car)
        messages.success(request, 'Автомобиль добавлен в корзину')
    else:
        messages.info(request, 'Автомобиль уже в корзине')
    
    return redirect('car_list')

class ScheduleTestDriveView(LoginRequiredMixin, CreateView):
    model = TestDrive
    form_class = TestDriveForm
    template_name = 'testdrive/schedule_testdrive.html'
    success_url = reverse_lazy('testdrive_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = get_object_or_404(Car, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.customer = get_object_or_404(Customer, user=self.request.user)
        form.instance.car = get_object_or_404(Car, pk=self.kwargs['pk'])
        messages.success(self.request, 'Вы успешно записались на тест-драйв')
        return super().form_valid(form)

@login_required
def remove_from_wishlist(request, pk):
    wishlist_item = get_object_or_404(Wishlist, pk=pk, customer__user=request.user)
    wishlist_item.delete()
    messages.success(request, 'Автомобиль удален из избранного')
    return redirect('wishlist_list')

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, customer__user=request.user)
    cart_item.delete()
    messages.success(request, 'Автомобиль удален из корзины')
    return redirect('cart_list')

def load_models(request):
    brand_id = request.GET.get('brand_id')
    models = Model.objects.filter(brand_id=brand_id).order_by('name')
    models_data = [{'id': model.id, 'name': model.name} for model in models]
    return JsonResponse(models_data, safe=False)

class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'wishlist/wishlist_list.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return Wishlist.objects.filter(customer__user=self.request.user)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('account')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Регистрация успешна!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Ошибка при регистрации: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def car_list(request):
    cars = Car.objects.all()
    return render(request, 'car/car_list.html', {'cars': cars})

@login_required
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'car/car_detail.html', {'car': car})

@user_passes_test(is_admin)
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Автомобиль успешно добавлен!')
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'car/car_form.html', {'form': form})

@user_passes_test(is_admin)
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Автомобиль успешно обновлен!')
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'car/car_form.html', {'form': form})

@user_passes_test(is_admin)
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Автомобиль успешно удален!')
        return redirect('car_list')
    return render(request, 'car/car_confirm_delete.html', {'car': car})

@login_required
def testdrive_list(request):
    try:
        customer = Customer.objects.get(user=request.user)
        testdrives = TestDrive.objects.filter(customer=customer)
        return render(request, 'testdrive/testdrive_list.html', {'testdrives': testdrives})
    except Customer.DoesNotExist:
        messages.error(request, 'Пожалуйста, заполните свой профиль клиента.')
        return redirect('profile')

@login_required
def testdrive_create(request, car_id):
    try:
        customer = Customer.objects.get(user=request.user)
        car = get_object_or_404(Car, pk=car_id)
        if request.method == 'POST':
            form = TestDriveForm(request.POST)
            if form.is_valid():
                testdrive = form.save(commit=False)
                testdrive.customer = customer
                testdrive.car = car
                testdrive.save()
                messages.success(request, 'Тест-драйв успешно записан!')
                return redirect('testdrive_list')
        else:
            form = TestDriveForm()
        return render(request, 'testdrive/testdrive_form.html', {'form': form, 'car': car})
    except Customer.DoesNotExist:
        messages.error(request, 'Пожалуйста, заполните свой профиль клиента.')
        return redirect('profile')

@login_required
def testdrive_cancel(request, pk):
    try:
        customer = Customer.objects.get(user=request.user)
        testdrive = get_object_or_404(TestDrive, pk=pk, customer=customer)
        if testdrive.status == 'pending':
            testdrive.delete()
            messages.success(request, 'Тест-драйв отменен!')
        return redirect('testdrive_list')
    except Customer.DoesNotExist:
        messages.error(request, 'Пожалуйста, заполните свой профиль клиента.')
        return redirect('profile')

@login_required
def wishlist_list(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist_list.html', {'wishlist': wishlist})

@login_required
def wishlist_add(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    Wishlist.objects.get_or_create(user=request.user, car=car)
    messages.success(request, 'Автомобиль добавлен в избранное!')
    return redirect('car_detail', pk=car_id)

@login_required
def wishlist_remove(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    Wishlist.objects.filter(user=request.user, car=car).delete()
    messages.success(request, 'Автомобиль удален из избранного!')
    return redirect('wishlist_list')

@login_required
def cart_list(request):
    cart = Cart.objects.filter(user=request.user)
    return render(request, 'cart/cart_list.html', {'cart': cart})

@login_required
def cart_add(request, car_id):
    cart = Cart(request)
    car = get_object_or_404(Car, id=car_id)
    cart.add(car)
    messages.success(request, f'Автомобиль {car.model.brand.name} {car.model.name} добавлен в корзину')
    return redirect('cart_detail')

@login_required
def cart_remove(request, car_id):
    cart = Cart(request)
    car = get_object_or_404(Car, id=car_id)
    cart.remove(car)
    messages.success(request, f'Автомобиль {car.model.brand.name} {car.model.name} удален из корзины')
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def create_order(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Ваша корзина пуста')
        return redirect('cart_detail')

    for item in cart:
        if Sale.objects.filter(car__vin=item['car'].vin).exists():
            messages.error(request, f'Автомобиль с VIN-номером {item["car"].vin} уже продан')
            return redirect('cart_detail')

    order = Order.objects.create(customer=request.user.customer)

    employee = User.objects.filter(is_staff=True).first()
    if not employee:
        messages.error(request, 'Нет доступных сотрудников для оформления продажи')
        return redirect('cart_detail')

    for item in cart:
        OrderItem.objects.create(
            order=order,
            car=item['car'],
            price=item['price']
        )
        

        Sale.objects.create(
            car=item['car'],
            customer=request.user.customer,
            employee=employee,
            sale_date=timezone.now().date(),
            price=item['price']
        )
    
    cart.clear()
    
    messages.success(request, f'Заказ №{order.id} успешно создан')
    return redirect('cart_detail')

@login_required
def sale_list(request):
    if request.user.is_staff:
        sales = Sale.objects.all()
    else:
        sales = Sale.objects.filter(user=request.user)
    return render(request, 'sale/sale_list.html', {'sales': sales})

@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()
            messages.success(request, 'Продажа успешно оформлена!')
            return redirect('sale_list')
    else:
        form = SaleForm()
    return render(request, 'sale/sale_form.html', {'form': form})

@user_passes_test(is_admin)
def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продажа успешно обновлена!')
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'sale/sale_form.html', {'form': form})

@user_passes_test(is_admin)
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        messages.success(request, 'Продажа успешно удалена!')
        return redirect('sale_list')
    return render(request, 'sale/sale_confirm_delete.html', {'sale': sale})

@login_required
def checkout(request):
    try:
        customer = Customer.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(customer=customer)
        
        if not cart_items.exists():
            messages.warning(request, 'Ваша корзина пуста')
            return redirect('cart_list')
            
        total_price = sum(item.car.price for item in cart_items)
        
        if request.method == 'POST':
            for item in cart_items:
                Sale.objects.create(
                    car=item.car,
                    customer=customer,
                    sale_date=timezone.now(),
                    price=item.car.price
                )
                item.car.is_available = False
                item.car.save()

            cart_items.delete()
            
            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('sale_list')
            
        return render(request, 'cart/checkout.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'customer': customer
        })
    except Customer.DoesNotExist:
        messages.error(request, 'Пожалуйста, заполните свой профиль клиента.')
        return redirect('profile')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    return render(request, 'order/order_detail.html', {'order': order})

@login_required
def account(request):
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'address': ''
        }
    )
    return render(request, 'account/account.html', {'customer': customer})

