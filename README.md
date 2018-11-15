# Airtech Flight booking

[![Build Status](https://travis-ci.org/johnchuks/flight-booking.svg?branch=develop)](https://travis-ci.org/johnchuks/flight-booking)
[![Coverage Status](https://coveralls.io/repos/github/johnchuks/flight-booking/badge.svg?branch=master)](https://coveralls.io/github/johnchuks/flight-booking?branch=develop)


## Introduction
Airtech Flight booking releases a REST API that enables users to book, purchase, and reserve tickets for a flight. The system was built using the Python Django framework. Some other technologies such Celery and Redis were embedded to the system to handle cron jobs or concurrent tasks



## Technologies Utilized For The Project
- Python (Django)
- Celery (task management system)
- Redis (Message broker and caching)


## Project Setup
Setting up this project on your local machine is fairly simple and it is done with the following steps
To start the installation ensure you have `virtualenv` on your local machine. `virtualenv` is recommended for setting your `dev` environment for this application.

- Run `chmod +x ./setup.sh` to make the script executable.
- Run `source setup.sh` to setup your development environment.
- create a `.env` file following the sample given in the repo
- Ensure to add ```DB_NAME=flight-booking```, `DB_USER=YOUR POSTGRES USER`, `DB_PASSWORD=YOUR POSTGRES PASSWORD`and `DB_PORT=5432` or any other port depending on your local machine.
- Ensure you have a `SECRET_KEY` and `JWT_SECRET_KEY` in your env.
- To install the dependencies, simply run `pip install -r requirements.txt`
- Finally you can run `./manage.py runserver 0.0.0.0:8000` to start the server in port 8000.


## Testing
The API is well tested and it adhered to best practices for testing django applications. The API can be tested by simply running the `pytest` command or `python manage.py test` command.


