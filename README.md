# Casting Agency API

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

## Database Setup
With Postgres running, run the following command to create a new database for the project:
```bash
createdb casting-agency
```

#### Export Environment Variables

Run the following statement to export environment variables

```bash
source ./setup.sh
```

This will export all environment variables needed for the application to run

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies and run application with

```bash
make all
```

This will install all of the required packages we selected within the `requirements.txt` file and run the application.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is the extension used to handle database migration. 

- [flask-restplus](https://flask-restplus.readthedocs.io/en/stable/) is the extension used to build documented apis. 

##### Swagger Documentation
- https://fremfi-casting-agency.herokuapp.com/
