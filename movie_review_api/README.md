Movie Review API
This is a Django-based RESTful API for movie reviews. Users can create accounts, log in, post reviews, comment on reviews, and like reviews. The API also features search, pagination, and secure authentication with JWT tokens.

Table of Contents
Features
Technologies
Setup Instructions
1. Clone the repository
2. Install dependencies
3. Set up environment variables
4. Set up the database
5. Run migrations
6. Create a superuser
7. Running the development server
Testing
API Documentation
Deployment
Future Improvements

Features

User Registration and Authentication: Users can sign up and log in using JWT-based authentication.
Review Management: Authenticated users can create, update, and delete reviews.
Comments: Users can comment on reviews.
Likes: Users can like reviews (one like per user per review).
Pagination & Search: Reviews are paginated, and users can search by movie title.
Swagger UI: Integrated Swagger UI for API documentation.
Secure Endpoints: JWT token-based authentication secures all the API endpoints.

Technologies

Django (Backend framework)
Django REST Framework (DRF) (API design)
PostgreSQL (Primary database) - Optional, you can use SQLite for local development.
Simple JWT (Authentication)
Swagger (drf-yasg package for API documentation)

Setup Instructions

1. Clone the repository
Clone this repository to your local machine:
git clone <repository-url>
cd movie_review_api

2. Install dependencies
Ensure you have Python 3.8+ installed. Set up a virtual environment to isolate the project’s dependencies:
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install django
pip install django
pip install django

3. Set up database
# Database settings (mySQL)
DATABASE_NAME=reviewdb
DATABASE_USER=root
DATABASE_PASSWORD=*password*
DATABASE_HOST=localhost
DATABASE_PORT=3306

# JWT Token settings
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=5

4. Set up the database
If using SQLite (default in development), you don't need to configure anything.
If using mySQL, ensure that it's installed and running. Create a database for the project:

# Access mySQL shell
mysql

# Create database
CREATE DATABASE reviewdb;

5. Run migrations
After configuring the database, run the migrations to set up the database schema:

python manage.py makemigrations
python manage.py migrate

6. Create a superuser
Create an admin user to access the Django admin panel:

python manage.py createsuperuser
You will be prompted for an email, username, and password.

7. Running the development server
Run the Django development server:

python manage.py runserver
The API will be available at http://127.0.0.1:8000/

Testing
To run unit tests for the project, use Django’s test framework:

python manage.py test
Ensure you’ve written tests for views, serializers, and models.

API Documentation
The API is documented with Swagger UI. To access the API documentation:

Start the server and visit http://127.0.0.1:8000/swagger/.
You can interact with the API directly via this interface to test all the endpoints.

Deployment
For deployment, here are the steps:

Heroku (or another cloud platform):

Ensure you have Procfile and requirements.txt for the deployment process.
Add mysql as the database in your cloud platform settings.
Push the code to your Heroku app and run migrations using:
bash
Copy code
heroku run python manage.py migrate
