## Sendit Courier App

<!-- [![Codacy Badge](https://api.codacy.com/project/badge/Grade/f19588cd49244775994cdca6a5b28434)](https://www.codacy.com/manual/dbytecoderc/sendit_api?utm_source=github.com&utm_medium=referral&utm_content=dbytecoderc/sendit_api&utm_campaign=Badge_Grade) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/dbytecoderc/sendit_api.svg?branch=develop)](https://travis-ci.org/dbytecoderc/sendit_api) [![Coverage Status](https://coveralls.io/repos/github/dbytecoderc/sendit_api/badge.svg?branch=develop)](https://coveralls.io/github/dbytecoderc/sendit_api?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/a959c189a724330370e5/maintainability)](https://codeclimate.com/github/dbytecoderc/sendit_api/maintainability) -->

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


## API Endpoints

<table>
  <tr>
      <th>Request</th>
      <th>End Point</th>
      <th>Action</th>
  </tr>
    <tr>
      <td>POST</td>
      <td>/api/user/create/</td>
      <td>Register a User</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/api/user/login/</td>
    <td>Login a user</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/api/category/categories/</td>
    <td>Get all categories</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/api/category/categories/</td>
    <td>Create a new category</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/api/favorite/favorites/</td>
    <td>Create a favorite thing</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/api/favorite/favorites/</td>
    <td>Get all favorite things</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/api/favorite/favorites/{int:id}</td>
    <td>Get the details of a favorite thing</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/api/favorite/favorites/?category_id={int: categoryId}</td>
    <td>Get all favorite thing in category</td>
  </tr>
  <tr>
    <td>PUT</td>
    <td>/api/favorite/favorites/{int:id}</td>
    <td>Update a favorite thing</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/api/favorite/history/</td>
    <td>Get audit log for user</td>
  </tr>
</table>

- Entity Realtionship diagram

![entity relationship diagram (2)](https://user-images.githubusercontent.com/19865565/61914085-3217e680-af37-11e9-9982-0a0d09f2b36e.png)

## Other Links

1. Link to the description of myself is [myself.json](https://github.com/tonyguesswho/favorite-things/blob/update-readme/myself.json)
2. Link to the answers to the remaining technical questions is [answers.md](https://github.com/tonyguesswho/favorite-things/blob/update-readme/answers.md)

I will appreciate any feedback on this project :)
```
