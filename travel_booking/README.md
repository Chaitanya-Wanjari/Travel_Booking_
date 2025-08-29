✈️ Travel Booking Web Application

A Django-based Travel Booking System that allows users to sign up, search for travel options (Flights, Trains, Buses), book tickets, manage bookings, and cancel if needed.
Includes authentication, pagination, search with suggestions, email-based password reset, and an admin panel for managing travel data.

🚀 Features

👤 User Management

Signup, Login, Logout

Profile Update

Password Reset (via email console backend)

🛫 Travel Options

Add & manage options (Flight / Train / Bus) via admin panel

Filter by type, source, destination, date

Search with auto-suggestions

Pagination for large lists

🎟️ Bookings

Book tickets with seat validation

View all bookings

Cancel bookings (seats automatically refunded)

⚙️ Admin Panel

Add/edit Travel Options

Manage Bookings

📂 Project Structure
travel_booking_complete/
│
├── travel_booking/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── booking/                 # Main app
│   ├── models.py            # TravelOption, Booking
│   ├── views.py             # Business logic
│   ├── urls.py              # Routes
│   ├── templates/           # HTML templates
│   └── ...
│
├── db.sqlite3               # Default SQLite database
├── manage.py
└── requirements.txt

🛠️ Setup Instructions
1. Clone the Repository
git clone https://github.com/Chaitanya-Wanjari/Travel-Booking.git
cd Travel-Booking

2. Create Virtual Environment
python -m venv .venv


Activate it:

Windows (PowerShell):

.venv\Scripts\activate


Linux/Mac:

source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Apply Migrations
python manage.py migrate

5. Create Superuser (for admin panel)
python manage.py createsuperuser

6. Run the Server
python manage.py runserver


Visit 👉 http://127.0.0.1:8000/travels/

🔑 Usage

Signup/Login → Create account at /signup/ or login at /accounts/login/.

Browse Travels → View travel options at /travels/.

Search/Filter → Use search box and filters for specific results.

Book Ticket → Select a travel option and book seats.

My Bookings → View all your bookings at /bookings/.

Cancel → Cancel booking (refund seats).

Password Reset → From login page → “Forgot Password?” → reset link appears in terminal (console backend).

Admin Panel → /admin/ (superuser only).
⚡ Tech Stack

Python 3.11+

Django 5.x

SQLite (default, MySQL config available)

Bootstrap 5 for UI
