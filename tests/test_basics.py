import unittest
from flask import current_app
from app import app

class BasicsTestCase(unittest.TestCase):
	"""docstring for BasicsTestCase"""
	def setUp(self):
		# creates a test client
		self.app = app.test_client()
		# propagate the exceptions to the test client
		self.app.testing = True

	def tearDown(self):
		pass
	
	def test_home_status_cdoe(self):
		result = self.app.get('/')
		self.assertEqual(result.status_code, 200)

	def test_create_schedule(self):
		data = { }
		result = self.app.post('/prodmgmt/Schedules', data,
			content_type='application/json')
		self.assertEqual(result.status_code, 201)