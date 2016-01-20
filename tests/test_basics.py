import unittest
from flask import current_app
from app import app

class BasicsTestCase(unittest.TestCase):
	"""docstring for BasicsTestCase"""
	def setUp(self):
		print "setUp"
		pass

	def tearDown(self):
		print "tearDown"
	