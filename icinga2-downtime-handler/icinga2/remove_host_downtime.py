from downtime_handler import Handler
import sensitive_data
from sys import argv

script, host = argv

hostname=sensitive_data.hostname
username=sensitive_data.username
password=sensitive_data.password

Handler(hostname, username, password).remove_host_downtime(host)
