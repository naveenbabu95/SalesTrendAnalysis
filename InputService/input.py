from wsgiref.simple_server import make_server
import cgi
import json
import requests
import os, time

filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'container_port.json')

with open(filepath) as outfile:
	url = json.load(outfile)

def app(environ, start_response):
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0
	
	# print(request_body_size)
	request_body = environ['wsgi.input'].read(request_body_size)
	# print(request_body)
	data = json.loads(request_body)
	# print(data)
	userid = data['userid']
	json_data = data['data']
	# print(json_data)
	sequence = data['sequence']
	# print(sequence)

	sequence1 = data['sequence'][1]
	# print(sequence1)
	if sequence1 == 'database':
		try:
			print("Database service called..!")
			print(url['database_url'])
			temp={'data':json_data, 'userid':userid, 'sequence':sequence}
			# print(temp)
			response = requests.post(url['database_url']+"/?userid={}".format(userid), data=json.dumps(temp))
			# response = requests.post('http://0.0.0.0:8004', data=json.dumps(temp))
			# time.sleep(10)
			#return response
			print(response)
		except Exception as e:
			print(e)
	elif sequence1 == 'analytics':
		try:
			print("Analytics service called..!")
			temp={'data':json_data, 'userid':userid, 'sequence':sequence}
			response = requests.post(url['analytics_url']+"/?userid={}".format(userid), data=json.dumps(temp))
			# response = requests.post('http://0.0.0.0:8002', data=json.dumps(temp))
			time.sleep(10)
			#return response
			print(response)
		except Exception as e:
			print(e)

	data = b'Hello, World!\n'
	status = '200 OK'
	response_headers = [('Content-type', 'text/plain'),('Content-Length', str(len(data)))]
	start_response(status, response_headers)
	return iter([data])