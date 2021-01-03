import pika
import requests
import json
import psycopg2
from datetime import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='final_queue')

def callback(ch, method, properties, body):
	print(type(body))
	body = json.loads(body)
	print(body)
	data = body['analysis']
	print(type(body))
	userid = body['userid']
	print(userid)

	del body['userid']
	date = datetime.now()
	print(date)
	# print(body)
	data = json.dumps(data)

	connection = psycopg2.connect(host = "localhost",user = "user12",password = "user",port = "5433",database = "analysis")
	cursor=connection.cursor()
	print("connection Established")

	insert = """ INSERT INTO result (data, calendar_date, userid) VALUES (%s,%s,%s)"""

	record_to_insert = (data,date,userid)
	# print(record_to_insert)
	cursor.execute(insert,record_to_insert)
	#cursor.executemany(insert_query, record_to_insert)
	connection.commit()
	print("Record Inserted")



channel.basic_consume(queue='final_queue', on_message_callback = callback, auto_ack=True)

print("Waiting for message..")

channel.start_consuming()