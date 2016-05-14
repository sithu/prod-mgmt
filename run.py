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
app.run(debug = True)
