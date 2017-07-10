
### Start the app

```sh
gunicorn --access-logfile - --log-file /tmp/app.log --bind 0.0.0.0:5000 --workers 1 --log-level info --capture-output  run:app
```