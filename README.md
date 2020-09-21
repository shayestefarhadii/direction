Django-Mapbox
=======================

## Add your mapbox token in settings.py file
```bash
nano .\djmaps\settings.py
```

## Installation

```bash
virtualenv venv
```
Then:
```
.\venv\Scripts\activate
```
Then:
```
pip install -r requirements.txt
```
Then:
```
python manage.py migrate
Then:
```
python manage.py runserver
```

Then visit http://localhost:8000/
