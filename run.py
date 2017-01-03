'''
Deprecated: old app startup file.
See@app.py
'''
from app import app

import logging
from logging import Formatter, FileHandler

file_handler = FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s'))

app.logger.addHandler(file_handler)

################ Flask-APScheduler #################
## http://stackoverflow.com/questions/32424148/how-to-use-flask-apscheduler-in-existed-flask-app
class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:job1',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 3600
        },
        {
            'id': 'startup_job',
            'func': '__main__:startup_job',
            'args': ["Hello"]
        }
    ]

    SCHEDULER_VIEWS_ENABLED = True

def job1(a, b):
    print(str(a) + ' ' + str(b))

def startup_job(text):
    print('Running startup job:' + text)

from flask_apscheduler import APScheduler
scheduler = APScheduler()
app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()


### Global Variables ###
AUTO_SCHEDULING_NUM_DAYS=7

app.run(host="0.0.0.0", debug = True)
