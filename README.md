# Eye2 - Backend Diagnostic Platform

This is the backend for the Eye2 medical diagnostic platform, built with Django and Django Rest Framework.

## Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd eye2_project
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup environment variables:**
    ```bash
    cp .env.example .env
    # Edit .env with your local settings
    ```

5.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  **Run Celery worker (in a separate terminal):**
    ```bash
    celery -A eye2_project worker -l info
    ```

## Running Tests

To run the test suite:
```bash
pytest