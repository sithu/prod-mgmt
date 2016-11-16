#### Run the App
```sh
export APP_SETTINGS="config.DevelopmentConfig"

./flask/bin/python run.py 
```

#### Create Test Data

```sh
./flask/bin/python manage.py create_admin
```

#### Employee Level

* 0 - Admin/CEO
* 1 - VP
* 2 - Director
* 3 - Manager
* 4 - Supervisor
* 5 - Skilled worker
