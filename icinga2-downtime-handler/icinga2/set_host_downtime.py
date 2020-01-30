from downtime_handler import Handler
from sys import argv

script, host, icinga2_hostname, icinga2_user, icinga2_pass = argv

Handler(icinga2_hostname, icinga2_user, icinga2_pass).set_host_downtime(host)
