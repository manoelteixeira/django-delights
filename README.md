# django-delights
 A simple inventory system for a restaurant

## Setup
1. Install Project dependencies
```
pip install -r requirements.txt
``` 
2. Setup Database
```
cd restaurant
python manage.py makemigrations
python manage.py migrate
```
3. Create superuser
```
python manage.py createsuperuser
```
4. Run Server
```
python manage.py runserver 0.0.0.0:8000
```
