import pandas as pd 
import numpy as np
import datetime
import json, os
import psycopg2
from wsgiref.simple_server import make_server
import cgi, requests
import ast

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
	request_body = environ['wsgi.input'].read(request_body_size)
	request_body = request_body.decode("utf-8")
	data = json.loads(request_body)

	sequence = data['sequence']
	json_data = json.dumps(data['data'])

	# json_data = request_body['data'].value # Returns a list of rows.
	# print(json_data)
	# userid = request_body['userid'].value
	# sequence = request_body['sequence'].value
	#print(type(sequence))
	# sequence = sequence1.split(',')
	#sequence = ast.literal_eval(sequence)
	# Always escape user input to avoid script injection

	response = run_analysis(json_data, sequence)
	response.update({"userid": data["userid"]})
	# print(response)
	try:
		if sequence[2] == 'database':
			requests.post(url['database_url']+"/?userid={}".format(data['userid']),data = json.dumps(data))
		requests.post(url['output_url']+"/?userid={}".format(data['userid']),data = json.dumps(response))
	except Exception as e:
		print(e)
	# output_url = url['output_url']
	# print(output_url)
	# try:
	# 	requests.post(output_url, data={'data':response})
	# except Exception as e:
	# 	print(e)

	# data = b"Recieved Data!\n"
	start_response("200 OK", [
		("Content-Type", "application/json"),
	])
	response = json.dumps(response)
	response = response.encode('utf-8')
	return [response]

def run_analysis(data, sequence):
	pd.set_option('display.max_rows', 10000)
	pd.set_option('display.max_columns', 100)

	if sequence[1] == 'database':
		# connection = psycopg2.connect(host = "localhost",user = "docker",password = "docker",port = "5432",database = "node4")
		connection = psycopg2.connect(host = "postgres",user = "docker",password = "docker",port = "5432",database = "sales")
		# connection = psycopg2.connect(host = "localhost",user = "node3",password = "node3",port = "5432",database = "node3")
		query = "SELECT * FROM trend"
		df = pd.read_sql(query, con=connection)
		df = df.drop(['id'], axis=1)
		df.columns = ['invoice_num','stock_code','description', 'quantity','invoice_date','unit_price','cust_id','country', 'userid']
		# print(df.columns)
		connection.close()
	else:
		df = pd.read_json(data)
		df.columns = ['invoice_num','stock_code','description', 'quantity','invoice_date','unit_price','cust_id','country']


	df.isnull().sum().sort_values(ascending=False)
	df[df.isnull().any(axis=1)].head()

	# print(df.columns.values)
	df['invoice_date'] = pd.to_datetime(df.invoice_date, format='%m/%d/%y %H:%M')
	df['description'] = df.description.str.lower()
	df.head()

	df_new = df.dropna()
	df_new.isnull().sum().sort_values(ascending=False)
	df_new.info()

	df_new.quantity = df_new.quantity.astype('int64')
	df_new.unit_price = df_new.unit_price.astype('float64')
	
	df_new.head()
	df_new.info()
	df_new.describe().round(2)

	df_new = df_new[df_new.quantity > 0]
	df_new.describe().round(2)
	df_new['amount_spent'] = df_new['quantity'] * df_new['unit_price']

	df_new = df_new[['invoice_num','invoice_date','stock_code','description','quantity','unit_price','amount_spent','cust_id','country']]

	df_new.insert(loc=2, column='year_month', value=df_new['invoice_date'].map(lambda x: 100*x.year + x.month))
	df_new.insert(loc=3, column='month', value=df_new.invoice_date.dt.month)
	# +1 to make Monday=1.....until Sunday=7
	df_new.insert(loc=4, column='day', value=(df_new.invoice_date.dt.dayofweek)+1)
	df_new.insert(loc=5, column='hour', value=df_new.invoice_date.dt.hour)

	df_new.head()

	## How many orders made by the customers?
	orders = df_new.groupby(by=['cust_id','country'], as_index=False)['invoice_num'].count()

	### Check TOP 5 most number of orders
	most_orders = orders.sort_values(by='invoice_num', ascending=False)
	most_num_orders = most_orders.to_json(orient='records')
	# print(most_num_orders)

	## How much money spent by the customers?
	money_spent = df_new.groupby(by=['cust_id','country'], as_index=False)['amount_spent'].sum()

	### Check TOP 5 highest money spent
	highest_money_spent = money_spent.sort_values(by='amount_spent', ascending=False)
	highest_money_spent = highest_money_spent.to_json(orient='records')
	# print(highest_money_spent)

	## How many orders (per month)?
	orders_month_wise = df_new.groupby('invoice_num')['year_month'].unique().value_counts().sort_index().to_frame(name = 'count').reset_index()
	# print(orders_month_wise)
	orders_month_wise = orders_month_wise.to_json(orient='records')
	# print(orders_month_wise)

	## How many orders (per day)?
	orders_day_wise = df_new.groupby('invoice_num')['day'].unique().value_counts().sort_index().to_frame(name='count').reset_index()
	orders_day_wise = orders_day_wise.to_json(orient='records')
	# print(orders_day_wise)

	 ## How many orders (per hour)?
	order_hour_wise = df_new.groupby('invoice_num')['hour'].unique().value_counts().iloc[:-1].sort_index().to_frame(name='count').reset_index()
	order_hour_wise = order_hour_wise.to_json(orient='records')
	# print(order_hour_wise)

	## How many orders for each country?
	group_country_orders = df_new.groupby('country')['invoice_num'].count().sort_values().to_frame(name='count').reset_index()
	group_country_orders = group_country_orders.to_json(orient='records')
	# print(group_country_orders)

	## How much money spent by each country?
	group_country_amount_spent = df_new.groupby('country')['amount_spent'].sum().sort_values().to_frame(name='count').reset_index()
	group_country_amount_spent = group_country_amount_spent.to_json(orient='records')
	# print(group_country_amount_spent)

	analysis = {
	'most_num_orders': most_num_orders,
	'highest_money_spent': highest_money_spent,
	'orders_month_wise': orders_month_wise,
	'orders_day_wise': orders_day_wise,
	'order_hour_wise': order_hour_wise,
	'group_country_orders': group_country_orders,
	'group_country_amount_spent': group_country_amount_spent
	}

	response = {"analysis": analysis}
	#print(response)
	return response

