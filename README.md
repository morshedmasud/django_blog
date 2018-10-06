# django_blog
Blog using django

## [Demo](http://morshed-bd.herokuapp.com/)

## Technology used
1. Django
2. Bootstrap

## Requirments
 * python >= 3.0
 * django >= 2.0
 * pipenv >= 1.0

## Setup in your local machine
1. First you need to clone this project from this project
```
git clone git@github.com:morshedmasud/django_blog.git
```

2. Install pipenv in your machine
```
pip install pipenv
```

3. Now run and install django by pipenv
```
pipenv install django
pipenv shell # Active pipenv
```
4. Apply database base migrations and migrate
```
python manage.py makemigrations
```
and
```
python manage.py migrate
```

5. Start django server locally
```
python manage.py runserver
```

6. Then create account and add post.

