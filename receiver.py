import pika
import requests
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='input_queue')

def callback(ch, method, properties, body):

	# print(" [x] Received %r" % body)
	print(type(body)) #bytes
	#body = body.replace("\'", "\"")
	body = body.decode("utf-8")
	print(type(body)) #string
	# body = json.loads(body)
	# print(type(body))
	userid = json.loads(body)['userid']
	response = requests.post("http://localhost:8000/?userid={}".format(userid), data=body)
	# print(response)

channel.basic_consume(queue='input_queue', on_message_callback = callback, auto_ack=True)

print("Waiting for message..")

channel.start_consuming()
