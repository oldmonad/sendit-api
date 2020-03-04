## Sendit Courier App

[![Build Status](https://travis-ci.org/dbytecoderc/sendit-api.svg?branch=develop)](https://travis-ci.org/dbytecoderc/sendit-api) [![Coverage Status](https://coveralls.io/repos/github/dbytecoderc/sendit-api/badge.svg?branch=develop)](https://coveralls.io/github/dbytecoderc/sendit-api?branch=develop)

[Postman API documentation](https://documenter.getpostman.com/view/6057580/SWE6bJZD)

[![Download and use collections in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/505dc360f139e2bbc52b)

## Description

The **sendit-app** is a courier service that helps users deliver parcels to different destinations.SendIT provides courier quotes based on weight categories. and the API is built with **Django(DRF) - Python**.

- Key Application features

1. Delivery order management

   - Creation a parcel delivery order
   - Updating parcel delivery order status
   - Real time tracking of parcel delivery using google maps
   - Removing parcel delivery order
   - Filtering parcel delivery orders based on delivery status

I created a test user to ease the process of testing the application

## Test User

- email - testuser@test.com
- password - password

## Technology Stack

- Django
- DRF
- Docker

### Setting Up For Local Development

- Check that python 3 is installed:

  ```
  python --version
  >> Python 3.7.0
  ```

- Install pipenv:

  ```
  brew install pipenv
  ```

- Check pipenv is installed:

  ```
  pipenv --version
  >> pipenv, version 2018.10.13
  ```

- Clone the favorite-thing repo and cd into it:

  ```
  git clone https://github.com/dbytecoderc/sendit_api.git
  ```

- Install dependencies from requirements.txt file:

  ```
  pip install -r requirements.txt
  ```

- Make a copy of the .env.sample file in the app folder and rename it to .env and update the variables accordingly:

  ```
  SECRET_KEY=generate a random django key # https://www.miniwebtool.com/django-secret-key-generator/
  DB_NAME=dbname
  DB_USER=dbuser
  DB_PASSWORD=secretpassword
  DB_HOST=yourdatabasehost
  ```

```

- Activate a virtual environment:

```

pipenv shell

```

- Apply migrations:

```

cd into the app folder and run python manage.py migrate

```

- If you'd like to seed initial data to the database:

```

Run python manage.py loaddata seed.py to seed user roles

```

* Run the application with the command

```

python manage.py runserver

````

* Should you make changes to the database models, run migrations as follows

- make migration

  ```
  python manage.py makemigrations
  ```

- Migrate:
  ```
  python manage.py migrate
  ```

* Deactivate the virtual environment once you're done:
````

exit

```

## Running tests

cd into the app folder and run

```

python manage.py test

```

To run test with coverage and coverage report

```

coverage run --source="." manage.py test

```

after the above command run this to get coverage report

```

coverage report

```

## Set Up Development With Docker

1. Download Docker from [here](https://docs.docker.com/)
2. Set up an account to download Docker
3. Install Docker after download
4. Go to your terminal run the command `docker login`
5. Input your Docker email and password

To setup for development with Docker after cloning the repository please do/run the following commands in the order stated below:

- `cd <project dir>` to check into the dir
- `docker-compose build`
- `docker-compose up -d` to start the api after the previous command is successful

The `docker-compose build` command builds the docker image where the api and its postgres database would be situated.
Also this command does the necessary setup that is needed for the API to connect to the database.

To run test run `docker-compose run app sh -c "python manage.py test"`

To run test with coverage and coverage report

```

docker-compose run app sh -c "coverage run --source="." manage.py test"

```

after the above command run this to get coverage report

```

docker-compose run app sh -c "coverage report"

```

The `docker-compose up -d` or `make start` command starts the application while ensuring that the postgres database is seeded before the api starts.

To stop the running containers run the command `docker-compose down`
```

## API Endpoints

<table>
  <tr>
      <th>Request</th>
      <th>End Point</th>
      <th>Action</th>
  </tr>
    <tr>
      <td>POST</td>
      <td>/api/v1/users/</td>
      <td>Register a User</td>
  </tr>
</table>

#### I will appreciate any feedback on this project :)
