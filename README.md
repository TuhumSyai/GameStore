# GameStore 🎮

GameStore — это онлайн-магазин видеоигр, разработанный на Django. Пользователи могут просматривать каталог игр, фильтровать и сортировать их, оплачивать покупки через Stripe и видеть список приобретённых игр. Игры импортируются через [RAWG API](https://rawg.io/apidocs).

## 📦 Возможности

- ✅ Каталог игр с фильтрацией по жанрам и сортировкой
- 🛒 Оплата игр через Stripe Checkout
- 👤 Пользовательская регистрация и авторизация
- 📃 Страница "Мои покупки" с купленными играми
- 🔄 Импорт данных из RAWG API
- 🔐 Stripe Webhook для фиксации покупок

## 🚀 Установка

1. **Клонируйте репозиторий**:

git clone https://github.com/yourusername/gamestore.git
cd gamestore

2. **Создайте и активируйте виртуальное окружение**:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3. **Установите зависимости**:

pip install -r requirements.txt

4. **Создайте файл .env и укажите ключи**:

STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret

5. **Примените миграции и создайте суперпользователя:**:

python manage.py migrate
python manage.py createsuperuser

6. **Запустите сервер:**:

python manage.py runserver

7. **Запустите Stripe CLI (для webhook)**:

stripe login
stripe listen --forward-to localhost:8000/payment/webhook/

## 🧪 Тестовая оплата

Вы можете использовать тестовые карты Stripe, например:
Номер карты: 4242 4242 4242 4242
Срок действия: Любой в будущем
CVC: Любой
ZIP: Любой

## 📁 Структура проекта

GameStore/
├── store/                  # Приложение магазина
│   ├── services/           
│   │   ├── tasks.py           
│   │   ├── utils.py           
│   ├── models.py           
│   ├── views.py            
│   ├── templates/store/    
├── static/                 
│   ├── css
│   ├── img
│   ├── js
├── media/                  
│   ├── avatars/
├── manage.py
├── .env
.gitignore
requirements.txt
README.md
stripe.exe
