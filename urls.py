from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('about/contacts/', contacts, name='contacts'),
    path('about/how-to-find/', how_to_find, name='how_to_find'),
    path('about/faq/', faq, name='faq'),
    path('about/support/', support, name='support'),
    path('products/', products, name='products'),
    path('products/categories/', categories, name='categories'),
    path('products/all/', all_products, name='all_products'),

    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/create/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),

    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),
    path('brands/create/', BrandCreateView.as_view(), name='brand_create'),
    path('brands/<int:pk>/update/', BrandUpdateView.as_view(), name='brand_update'),
    path('brands/<int:pk>/delete/', BrandDeleteView.as_view(), name='brand_delete'),
 
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
  
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
 
    path('sales/', SaleListView.as_view(), name='sale_list'),
    path('sales/<int:pk>/', SaleDetailView.as_view(), name='sale_detail'),
    path('sales/create/', SaleCreateView.as_view(), name='sale_create'),
    path('sales/<int:pk>/update/', SaleUpdateView.as_view(), name='sale_update'),
    path('sales/<int:pk>/delete/', SaleDeleteView.as_view(), name='sale_delete'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:car_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:car_id>/', views.cart_remove, name='cart_remove'),
    path('cart/create-order/', views.create_order, name='create_order'),

    path('wishlist/', WishlistListView.as_view(), name='wishlist_list'),
    path('wishlist/add/<int:pk>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:pk>/', remove_from_wishlist, name='remove_from_wishlist'),

    path('testdrive/', TestDriveListView.as_view(), name='testdrive_list'),
    path('testdrive/schedule/<int:pk>/', ScheduleTestDriveView.as_view(), name='schedule_testdrive'),
    path('testdrive/cancel/<int:pk>/', views.testdrive_cancel, name='testdrive_cancel'),

    path('account/', views.account, name='account'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    path('ajax/load-models/', load_models, name='ajax_load_models'),

    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)