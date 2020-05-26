# Tandora Development Setup

Developed using Python, Django and Django Rest Framework

## Prerequisites

- Docker [Download from here for mac](https://download.docker.com/mac/stable/Docker.dmg).

## Setup

- Clone this repo
    `git clone https://tandora@bitbucket.org/tandoraco/tandora-backend.git`
- cd to this repo in terminal
    - `cd tandora-backend`
- Copy the contents of file sample.env to .env
    - `cp sample.env .env`
- Start the service by using the following command
    - `docker-compose -f dev.yml up`
- After the server starts, type the following commands to run migrations and populate initial data
    - `docker exec -it tandora-backend_web_1 /bin/sh`
    - `python manage.py migrate`
    - `python manage.py dev_setup`
    - `python manage.py dev_setup_static_site`
        - Closely watch the output of terminal logs. There will be a line containing Click this (some url) to verify your url.
        - Copy that verification url and paste in browser to activate your user account.
- Now visit [http://localhost:8000](http://localhost:8000) in browser.
- For credentials to login refer this file tandoramaster/management/commands/dev_setup.py


## Running locally after setup
- Issue this command in terminal at the root of repo
    - `docker-compose -f dev.yml up`

## Running tests locally

Run the following commands to run test suite.
- `docker exec -it tandora-backend_web_1 /bin/sh`
- `pytest`

## Activating admin
-  If you hit http://localhost:8000/admin/ without performing the steps, the default credentials would not take you
to admin page. You should make yourselves a super user to access admin.
- Perform the following
    - `docker exec -it tandora-backend_web_1 /bin/sh`
    - `python manage.py shell`
    ```python
    In [1]: from v1.accounts.models import User
    In [2]: u=User.objects.get(id=1)
    In [3]: u.is_admin = True
    In [4]: u.is_superuser = True
    In [5]: u.save()
    ```
- After the above steps, visit the admin url in browser and use default credentials.

## Debugging in dev

- When you up the container using `docker-compose -f dev.yml up` ipdb cannot be used. So stop the container using `docker-compose -f dev.yml stop`
- Then start the container using the following command to use ipdb and other debuggers.
    - `docker-compose -f dev.yml run --service-ports web`
    - Bash shell of container cannot be used in this mode.

## Setup GIT Hooks

- Flake8 is used as a linter and pre-commit hooks.
- Add flake8 as a pre-commit hook so that code is checked for pep8 conventions. If this is not followed, the code may fail the style check test in pipeline.
- `flake8 --install-hook git`

## Other useful links

- [Writing DB migrations](https://bitbucket.org/tandoraco/tandora-backend/wiki/DB%20migrations)
- [Coding conventions](https://bitbucket.org/tandoraco/tandora-backend/wiki/Coding%20conventions)
- [Writing tests](https://bitbucket.org/tandoraco/tandora-backend/wiki/Writing%20tests)
- [App workflow](https://bitbucket.org/tandoraco/tandora-backend/wiki/Workflow%20of%20app)
- [Adding a new integration](https://bitbucket.org/tandoraco/tandora-backend/wiki/New%20Integration%20Guidelines)
