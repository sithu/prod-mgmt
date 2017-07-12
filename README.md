
### Start the app

```sh
gunicorn --access-logfile - --log-file /tmp/app.log --bind 0.0.0.0:5000 --workers 1 --log-level info --capture-output  run:app
```

### Prepare Dev Env

```sh
virtualenv --no-site-packages flask 
flask/bin/pip list
flask/bin/pip list
flask/bin/pip install -r requirements.txt 
flask/bin/pip list | wc -l
pip list | wc -l
./flask/bin/python run.py 

```
