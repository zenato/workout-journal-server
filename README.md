# Workout journal

Python based workout journal API server toy project.

## Getting Started

### Create your own configuration `.env` in project root.
```
DB_NAME = db_name
DB_USER = user_name
DB_PASSWORD = user_password
DB_HOST = 127.0.0.1
DB_PORT = 5432
```

### Configure virtual environment
`python3 -m venv venv`

### Activate virtual environment
`source venv/bin/activate`

### Install requirement modules
`pip install -r requirements.txt`

### Run server
`python manage.py runserver`

You may need to migrate DB.


## Deployment
If you use now.sh
```sh
now secret add workout-journal-db-host "db host"
now secret add workout-journal-db-port "5432"
now secret add workout-journal-db-name "default_database"
now secret add workout-journal-db-user "db_user"
now secret add workout-journal-db-password "password"
now
```


## Related project
* [Web client](https://github.com/zenato/workout-journal-web) - React based web client toy project.
* [Mobile client] - Progressive.
