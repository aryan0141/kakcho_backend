# Kakcho Project

## Features
- Google Auth
- Upload CSV
- Filter Data on the basis of Type
- Filter data on the basis of content category
- Created rounded rating coloumn
- Download the CSV file

## Tech

- Django
- PostgreSQL

## Procedure

- Navigate to the cloned repository.
    ```
    cd <project_directory_name>     #   kakcho_backend
    ```
- Create a new virtual environment and activate it.
    ```
    python -m venv env
    .\env\Scripts\activate
    ```
- Use pip to install other dependencies from `requirements.txt`
    ```
    pip install -r requirements.txt
    ```
- Copy .env file
   ```
   cp .env.example .env
   ```
- Make database migrations
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
- Create a superuser
    ```
    python manage.py createsuperuser
    ```
- Run development server on localhost
    ```
    python manage.py runserver
    ```
