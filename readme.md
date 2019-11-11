# Admiral Markets - Python Test Assignment
##Start with Docker
Start app with docker-compose:

`docker-compose up`

Start tests with docker-compose:

`docker-compose -f docker-compose.tests.yml up categories_api_tests`

##For local start:

Install pipenv if not installed: `pip install pipenv`

Activate shell: `pipenv shell`

Install libs from Pipfile: `pipenv update`

Start tests: `make tests`

Start dev app: `src/manage.py runserver 127.0.0.1:8000`
 
For configuration use ENV variables:

- DB_NAME - default (categories_api) 
- DB_USER - default (categories_api)
- DB_PASSWORD - default (categories_api)
- DB_HOST - default (localhost)
- DB_PORT - default (5432)
- DEBUG - default (false)
