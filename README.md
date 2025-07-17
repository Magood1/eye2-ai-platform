# Eye2 - Backend Diagnostic Platform

This is the backend for the Eye2 medical diagnostic platform, built with Django and Django Rest Framework.

## Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Magood1/eye2-ai-platform
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
    cp .env .env.example
    ```

5.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```


## Running Tests

To run the test suite:
```bash
pytest
