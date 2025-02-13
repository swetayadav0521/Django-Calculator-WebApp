# django-calculator-app

### Project configuration
```bash
git clone https://github.com/Luko575/django-calculator-app.git
cd django-calculator-app

# -------------------------------------
# If you are on Windows
py -m venv env # or python -m venv env
.\env\Scripts\activate

# If you are on Linux or Mac
virtualenv env
source env/bin/activate
# -------------------------------------

pip install -r requirements.txt
py manage.py makemigrations # or python manage.py makemigrations
py manage.py migrate # or python manage.py migrate
py manage.py createsuperuser # or python manage.py createsuperuser
```

### Running the application
```bash
py manage.py runserver # or python manage.py runserver
```

> The development server will be running at http://127.0.0.1:8000/

> The administration panel can be found at http://127.0.0.1:8000/admin/