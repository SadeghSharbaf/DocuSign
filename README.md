# DocuSign

A Django web application related to contract/document workflows.

## Tech Stack
- Python
- Django

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables and review the Django settings.
4. Run migrations and start the development server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Database
The local SQLite database is excluded from Git. Recreate it with migrations.

## Security
Do not commit private documents, credentials, secret keys, or real customer data.
