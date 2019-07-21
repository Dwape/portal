# portal

A basic attempt at accessing data in Universidad Austral's portal.

Inspired by https://github.com/matimiodosky/Portal

### Running

This project uses pipenv to manage packages:

[Installing pipenv](https://docs.pipenv.org/en/latest/install/#installing-pipenv)

Install dependencies by running:

```shell
pipenv install
```

Currently it only prints the "grade point average" for the user and the ids of all the courses by running the following command:

```shell
pipenv run python portal.py [dni] [password]
```

**MySQL**  
To run MySQL perform the following commands from the project directory
```shell
cd portal/docker_compose/
docker-compose up
```
To shutdown the database run: 
```shell
docker-compose down
```
To reset and shutdown the database run:
```shell
docker-compose down -v
```