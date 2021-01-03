from wsgiref.simple_server import make_server
import cgi
import requests
import json
import pika

def app(environ, start_response):

	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0

	# When the method is POST the variable will be sent
	# in the HTTP request body which is passed by the WSGI server
	# in the file like wsgi.input environment variable.
	request_body = environ['wsgi.input'].read(request_body_size)
	data = json.loads(request_body)
	print(data)


	credentials = pika.PlainCredentials('admin', 'admin')
	connection = pika.BlockingConnection(pika.ConnectionParameters('172.18.16.73','5672','/',credentials))
	channel = connection.channel()
	print("Connecion with rabbitmq done")

	channel.queue_declare(queue='final_queue')
	channel.basic_publish(exchange='', routing_key='final_queue', body=json.dumps(data))

	print("Data sent to queue")
	start_response("200 OK", [
		("Content-Type", "application/json"),
	])
	response = json.dumps(data)
	response = response.encode('utf-8')
	# print(response)
	return [response]


