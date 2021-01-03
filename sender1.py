import pika
import json
import pandas as pd
import time
#Create a new instance of the Connection object

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

#Create a new channel with the next available channel number or pass in a channel number to use

channel = connection.channel()

#Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.

channel.queue_declare(queue='input_queue')

df = pd.read_csv("Online Retail.csv")
start_index = 0
end_index = 99

jsondata ={
	"userid" : "104",
	"data" :[],
	"sequence" : ["inputservice","database","analytics","output"]
}

print(jsondata)

t0 = time.time()
while(time.time()-t0 < 40):
	print(start_index, end_index)
	jsondata['data'] = json.loads(df[start_index:end_index].to_json(orient='records'))
	# print(jsondata['data'])
	channel.basic_publish(exchange='', routing_key='input_queue', body=json.dumps(jsondata))
	start_index = end_index + 1
	end_index = start_index + 99
	time.sleep(10)    
	
connection.close()