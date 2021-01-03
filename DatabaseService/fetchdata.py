from wsgiref.simple_server import make_server
import cgi
import requests
import psycopg2
import json
import ast
import os

filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'container_port.json')

with open(filepath) as outfile:
	url = json.load(outfile)

def app(environ, start_response):
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0

	# When the method is POST the variable will be sent
	# in the HTTP request body which is passed by the WSGI server
	# in the file like wsgi.input environment variable.
	
	# print(request_body_size)
	request_body = environ['wsgi.input'].read(request_body_size)
	request_body = request_body.decode("utf-8")
	#print(request_body)
	data = json.loads(request_body)
	#print(data)
	sequence = data['sequence']
	#print(sequence)
	json_data = data['data']
	# print(json_data)
	# print(type(json_data))

	#json_data = json_data.to_string()
	#print(json_data)
	#print(type(json_data))
	#json_data = json.dumps(json_data)
	#print(type(json_data))
	userid = data['userid']
	for row in json_data:
		row.update({'userid': userid})

	data_array = json_data
	# data_array.append(json_data)
	# print(json_data[0])
	# print(userid)
	# print(type(userid))
	response = {}
	try:
		#connection with db
		# connection = psycopg2.connect(host = "localhost",user = "docker",password = "docker",port = "5432",database = "node4")
		connection = psycopg2.connect(host = "postgres",user = "docker",password = "docker",port = "5432",database = "sales")
		cursor=connection.cursor()
		print("connection Established")


		# if sequence[2] == 'database':
		# 	# insert
		#insert_query = "INSERT INTO trend(userid,InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		record_to_insert = tuple(data_array)
		# print(record_to_insert)
		cursor.executemany("""INSERT INTO trend(InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country,userid) VALUES (%(InvoiceNo)s,%(StockCode)s,%(Description)s,%(Quantity)s,%(InvoiceDate)s,%(UnitPrice)s,%(CustomerID)s,%(Country)s,%(userid)s)""", record_to_insert)
		#cursor.executemany(insert_query, record_to_insert)
		connection.commit()
		print("Record Inserted")

		#next_service_endpoint_url = 'http://0.0.0.0:8002'
		try:
			if sequence[1] == 'database':
				temp={'data':json_data, 'userid': userid, 'sequence': sequence}
				# print(temp)
				response = requests.post(url['analytics_url']+"/?userid={}".format(userid), data=json.dumps(temp))
				# print(response)
			else:
				print("pass it to output")
		except Exception as e:
			print(e)
	except Exception as e:
		print("Eror occured " + str(e))
	finally:
		connection.close()

	data = b'Hello, World!\n'
	status = '200 OK'
	response_headers = [('Content-type', 'text/plain'),('Content-Length', str(len(data)))]
	start_response(status, response_headers)
	return iter([data])

