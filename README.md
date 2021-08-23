# Tandora Changelog Development Setup

Developed using Python, Django and Django Rest Framework

## Prerequisites

- Docker [Download from here for mac](https://download.docker.com/mac/stable/Docker.dmg).

## Setup

- Clone this repo
    `git clone https://github.com/tandoraco/changelog.git`
- cd to this repo in terminal
    - `cd changelog`
- Copy the contents of file sample.env to .env
    - `cp sample.env .env`
- Start the service by using the following command
    - `docker-compose -f dev.yml up`
- After the server starts, type the following commands to run migrations and populate initial data
    - `docker exec -it changelog_web_1 /bin/sh`
    - `python manage.py migrate`
    - `python manage.py dev_setup`
        - Closely watch the output of terminal logs. There will be a line containing Click this (some url) to verify your url.
        - Copy that verification url and paste in browser to activate your user account.
- Now visit [http://localhost:8000](http://localhost:8000) in browser.
- For credentials to login refer this file tandoramaster/management/commands/dev_setup.py


## Running locally after setup
- Issue this command in terminal at the root of repo
    - `docker-compose -f dev.yml up -d`

## Running tests locally

Run the following commands to run test suite.
- `docker exec -it changelog_web_1 /bin/sh`
- `pytest`

## Activating admin
-  If you hit http://localhost:8000/admin/ without performing the steps, the default credentials would not take you
to admin page. You should make yourselves a super user to access admin.
- Perform the following
    - `docker exec -it changelog_web_1 /bin/sh`
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

- When you up the container using `docker-compose -f dev.yml up` ipdb cannot be used. So stop the container using `docker-compose -f dev.yml stop` and then start the containers in detached mode. `docker-compose -f dev.yml up -d`
- Now attach to the web container. `docker attach changelog_web_1`
- Now ipdb can be used in the attached container.

## Setup GIT Hooks

- Flake8 is used as a linter and pre-commit hooks.
- Add flake8 as a pre-commit hook so that code is checked for pep8 conventions. If this is not followed, the code may fail the style check test in pipeline.
- `flake8 --install-hook git`

## Other useful links

- [Writing DB migrations](https://github.com/tandoraco/changelog/wiki/DB-Migrations)
- [Adding a new integration](https://github.com/tandoraco/changelog/wiki/How-to-add-a-new-Integration-%3F)
