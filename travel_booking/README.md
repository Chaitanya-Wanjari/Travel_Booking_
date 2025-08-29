
# Travel Booking Application

Quickstart (SQLite):
1. Create virtual env and install requirements:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
2. Run migrations & create superuser:
   python manage.py migrate
   python manage.py createsuperuser
3. Run server:
   python manage.py runserver
4. Visit http://127.0.0.1:8000/travels/

Password reset uses console email backend (emails printed to terminal).
