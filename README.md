# django-realty: Django realty app

## Project environment

Create .env file in the root of project(/realty) where settings.py located and set the variables:

```dotenv
SECRET_KEY=YOUR_SECRET_KEY
DB_NAME=YOUR_DB_NAME
DB_USER=YOUR_DB_USERNAME
DB_PASSWORD=YOUR_DB_PASSWORD
DB_HOST=YOUR_HOST(e.g. localhost)
DB_PORT=YOUR_PORT(default=5432)
Project local settings
Install requirements:
```

```bash
pip install -r requirements.txt
```

Migrate database:

```bash
python manage.py migrate
```

And finally, run server.

```bash
python manage.py runserver
```