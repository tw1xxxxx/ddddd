#!/usr/bin/env python3
"""
Тестовый скрипт для проверки CRUD операций API AlphaTruck Shop
"""

import requests
import json
from datetime import datetime, date

# Базовый URL API
BASE_URL = "http://127.0.0.1:8000/api"

def test_api_endpoints():
    """Тестирование основных API endpoints"""
    
    print("🚗 Тестирование API AlphaTruck Shop")
    print("=" * 50)
    
    # Тест 1: Получение списка марок (не требует аутентификации)
    print("\n1. Тестирование Brands API...")
    try:
        response = requests.get(f"{BASE_URL}/brands/")
        if response.status_code == 200:
            brands = response.json()
            print(f"✅ Brands API работает. Найдено марок: {len(brands.get('results', brands))}")
        else:
            print(f"❌ Brands API ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Brands API недоступен: {e}")
    
    # Тест 2: Получение списка моделей
    print("\n2. Тестирование Models API...")
    try:
        response = requests.get(f"{BASE_URL}/models/")
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Models API работает. Найдено моделей: {len(models.get('results', models))}")
        else:
            print(f"❌ Models API ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Models API недоступен: {e}")
    
    # Тест 3: Получение списка автомобилей
    print("\n3. Тестирование Cars API...")
    try:
        response = requests.get(f"{BASE_URL}/cars/")
        if response.status_code == 200:
            cars = response.json()
            print(f"✅ Cars API работает. Найдено автомобилей: {len(cars.get('results', cars))}")
        else:
            print(f"❌ Cars API ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Cars API недоступен: {e}")
    
    # Тест 4: Тестирование фильтрации
    print("\n4. Тестирование фильтрации...")
    try:
        # Фильтрация марок по стране
        response = requests.get(f"{BASE_URL}/brands/?country=Germany")
        if response.status_code == 200:
            brands = response.json()
            print(f"✅ Фильтрация работает. Немецких марок: {len(brands.get('results', brands))}")
        else:
            print(f"❌ Фильтрация ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Фильтрация недоступна: {e}")
    
    # Тест 5: Тестирование пагинации
    print("\n5. Тестирование пагинации...")
    try:
        response = requests.get(f"{BASE_URL}/cars/?page_size=5")
        if response.status_code == 200:
            cars = response.json()
            if 'count' in cars:
                print(f"✅ Пагинация работает. Всего автомобилей: {cars['count']}, на странице: {len(cars['results'])}")
            else:
                print(f"✅ Пагинация работает. На странице: {len(cars)}")
        else:
            print(f"❌ Пагинация ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Пагинация недоступна: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Тестирование завершено!")
    print("\nДля полного тестирования CRUD операций:")
    print("1. Запустите сервер: python manage.py runserver")
    print("2. Получите токен: POST /api/token/")
    print("3. Тестируйте аутентифицированные endpoints")

def test_authentication():
    """Тестирование аутентификации"""
    print("\n🔐 Тестирование аутентификации...")
    
    # Попытка получить токен
    auth_data = {
        "username": "admin123",
        "password": input("Введите пароль для admin123: ")
    }
    
    try:
        response = requests.post(f"{BASE_URL}/token/", json=auth_data)
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Аутентификация успешна!")
            print(f"Access token: {token_data.get('access', 'Не получен')[:20]}...")
            return token_data.get('access')
        else:
            print(f"❌ Ошибка аутентификации: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return None

def test_authenticated_endpoints(token):
    """Тестирование аутентифицированных endpoints"""
    if not token:
        print("❌ Токен не получен, пропускаем тестирование аутентифицированных endpoints")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🔒 Тестирование аутентифицированных endpoints...")
    
    # Тест клиентов
    try:
        response = requests.get(f"{BASE_URL}/customers/", headers=headers)
        if response.status_code == 200:
            customers = response.json()
            print(f"✅ Customers API работает. Найдено клиентов: {len(customers.get('results', customers))}")
        else:
            print(f"❌ Customers API ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Customers API недоступен: {e}")
    
    # Тест сотрудников
    try:
        response = requests.get(f"{BASE_URL}/employees/", headers=headers)
        if response.status_code == 200:
            employees = response.json()
            print(f"✅ Employees API работает. Найдено сотрудников: {len(employees.get('results', employees))}")
        else:
            print(f"❌ Employees API ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Employees API недоступен: {e}")

if __name__ == "__main__":
    # Основное тестирование
    test_api_endpoints()
    
    # Опциональное тестирование аутентификации
    print("\n" + "=" * 50)
    test_auth = input("Хотите протестировать аутентификацию? (y/n): ").lower()
    if test_auth == 'y':
        token = test_authentication()
        if token:
            test_authenticated_endpoints(token)
