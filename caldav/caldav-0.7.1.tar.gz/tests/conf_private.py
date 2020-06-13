if True:
    test_xandikos = False
    test_radicale = False
    xandikos_port = None
    xandikos_host = None
    radicale_port = None
    radicale_host = None
    from . import compatibility_issues
    rl_zimbra = {'url': 'https://tobias%40redpill-linpro.com:%2Fr3g3l3n3%40Zimbra.@zimbra.redpill-linpro.com/dav/', 'incompatibilities': compatibility_issues.zimbra} 
    home = {'url': 'http://tobias:%2Ffamily.@calendar.bekkenstenveien53c.oslo.no:80/caldav.php/', 'incompatibilities': compatibility_issues.davical}
   
    caldav_servers = [home]
    #caldav_servers = [rl_zimbra]
else:
    caldav_servers = []
    test_xandikos = True
    test_radicale = True



#caldav_servers.append({'url': 'https://caldav.icloud.com/', 'username': 'python-caldav@xam.dk', 'password': 'rEAWketv4jjw'})
#caldav_servers.pop(0)
#caldav_servers.append({'url': 'https://nextcloud-fi.webo.hosting/remote.php/dav/', 'username': 't-caldav-nextcloud@tobixen.no', 'password': '/Test4Caldav.'})

#caldav_servers = []





####### BROKEN STUFF
## broken owncloud installation, I think
#caldav_servers.append({'url': 'https://oppetid.no/owncloud/remote.php/caldav/', 'username': 'tobixen', 'password': 'ZyWretshEl'})
## Spews tracebacks in some of the responses
#caldav_servers.append({'url': 'http://dav.cladmi.eu/cal.php/calendars/tbrox/default/', 'username': 'tbrox', 'password': 'testdigestauthenticationtbrox'})

#caldav_servers.append({'url': 'https://cloud.rebattu.fr/remote.php/caldav/calendars/nantas/defaultcalendar', 'username': 'nantas', 'password': 'nantas1954', 'ssl_verify_cert': False})
#caldav_servers.append({'url': 'https://caldav.icloud.com/', 'username': 'bramblecucumber@icloud.com', 'password': '97x4GxTl', 'load_balanced_host': True})
#caldav_servers.append({'url': "https://greyspammer.strangled.net:8443/owncloud/remote.php/caldav/", "username": "tobixen", "password": "9NZdpoZwDqhjfCBs", "ssl_verify_cert": False})


##  / 

