from nose.tools import *
from icinga2.downtime_handler import Handler
import requests

def test_api_connection():
	handler = Handler('https://test.test.com:5665/v1', 'root', 'mysecretpass')
	response = handler.get_status()
	assert_equal(f"{response}", "<Response [200]>")
