from downtime_handler import Handler
from sys import argv

script, host, icinga2_hostname, icinga2_user, icinga2_pass, icinga2_comment = argv

Handler(icinga2_hostname, icinga2_user, icinga2_pass, icinga2_comment).remove_host_downtime(host)
