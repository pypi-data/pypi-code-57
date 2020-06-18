import pika

# monitoring

host = "10.54.217.95"
creds = ('enugeojson_prod', 'geognss_prod')
vhost = "gpsdata"
queue_name = "gpsstream"

def connect(creds, host,vhost, queue_name, durable=True):
	credentials = pika.PlainCredentials(*creds)
	parameters = pika.ConnectionParameters(host = host,
												virtual_host = vhost,
												credentials = credentials)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	if durable:
		channel.queue_declare(queue_name, durable=durable)
	else:
		channel.queue_declare(queue_name)
	return channel
		
		
connect(creds, host, vhost, queue_name, durable=False)
