# portal

A basic attempt at accessing data in Universidad Austral's portal.

Inspired by https://github.com/matimiodosky/Portal

### Running

This project uses pipenv to manage packages and pyquery to make the requests:

[Installing pipenv](https://docs.pipenv.org/en/latest/install/#installing-pipenv)

[Installing pyquery](https://pypi.org/project/pyquery/)

Currently it only prints the "grade point average" for the user and the ids of all the courses by running the following command:

```shell
pipenv run python portal.py [dni] [password]
```
