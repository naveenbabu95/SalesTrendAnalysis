import pandas as pd

df = pd.DataFrame(columns=['user','service','instances','successful','failed'])

columns=['status','pid','user']
input_df = pd.read_csv("InputService/logs/gunicorn-access.csv", names=columns)
print(input_df.head())

input_unique_pid = input_df.groupby(by='user', as_index=False).agg({'pid': pd.Series.nunique})

input_unique_status = input_df.groupby('user')['status'].value_counts().sort_index().to_frame(name='count').reset_index()

for index,row in input_unique_pid.iterrows():
	temp = {"user": row['user'],
	        "service": "input",
	        "instances": row['pid'],
	        "successful": 0,
	        "failed": 0}
	temp['successful'] = input_unique_status.loc[(input_unique_status['user']==row['user']) & (input_unique_status['status']==200)]['count'].values[0]
	try:
		temp['failed'] = input_unique_status.loc[(input_unique_status['user']==row['user']) & (input_unique_status['status']==500)]['count'].values[0]
	except:
		print("no failed requests!")
	temp = pd.DataFrame(data=temp, columns=['user','service','instances','successful','failed'], index=[index])
	df = pd.concat([temp, df])

analytics_df = pd.read_csv("AnalyticsService/logs/gunicorn-access.csv", names=columns)
analytics_unique_pid = analytics_df.groupby(by='user', as_index=False).agg({'pid': pd.Series.nunique})

analytics_unique_status = analytics_df.groupby('user')['status'].value_counts().sort_index().to_frame(name='count').reset_index()

for index,row in analytics_unique_pid.iterrows():
	temp = {"user": row['user'],
	        "service": "analytics",
	        "instances": row['pid'],
	        "successful": 0,
	        "failed": 0}
	temp['successful'] = analytics_unique_status.loc[(analytics_unique_status['user']==row['user']) & (analytics_unique_status['status']==200)]['count'].values[0]
	try:
		temp['failed'] = analytics_unique_status.loc[(analytics_unique_status['user']==row['user']) & (analytics_unique_status['status']==500)]['count'].values[0]
	except:
		print("no failed requests!")
	temp = pd.DataFrame(data=temp, columns=['user','service','instances','successful','failed'], index=[index])
	df = pd.concat([temp, df])

# print(analytics_df.columns)
database_df = pd.read_csv("DatabaseService/logs/gunicorn-access.csv", names=columns)

database_unique_pid = database_df.groupby(by='user', as_index=False).agg({'pid': pd.Series.nunique})

database_unique_status = database_df.groupby('user')['status'].value_counts().sort_index().to_frame(name='count').reset_index()

for index,row in database_unique_pid.iterrows():
	temp = {"user": row['user'],
	        "service": "database",
	        "instances": row['pid'],
	        "successful": 0,
	        "failed": 0}
	temp['successful'] = database_unique_status.loc[(database_unique_status['user']==row['user']) & (database_unique_status['status']==200)]['count'].values[0]
	try:
		temp['failed'] = database_unique_status.loc[(database_unique_status['user']==row['user']) & (database_unique_status['status']==500)]['count'].values[0]
	except:
		print("no failed requests!")
	temp = pd.DataFrame(data=temp, columns=['user','service','instances','successful','failed'], index=[index])
	df = pd.concat([temp, df])

# output_df = pd.read_csv("OutputService/logs/gunicorn-access.csv", names=columns)

# output_unique_pid = output_df.groupby(by='user', as_index=False).agg({'pid': pd.Series.nunique})

# output_unique_status = output_df.groupby('user')['status'].value_counts().sort_index().to_frame(name='count').reset_index()

# for index,row in output_unique_pid.iterrows():
# 	temp = {"user": row['user'],
# 	        "service": "database",
# 	        "instances": row['pid'],
# 	        "successful": 0,
# 	        "failed": 0}
# 	temp['successful'] = output_unique_status.loc[(output_unique_status['user']==row['user']) & (output_unique_status['status']==200)]['count'].values[0]
# 	try:
# 		temp['failed'] = output_unique_status.loc[(output_unique_status['user']==row['user']) & (output_unique_status['status']==500)]['count'].values[0]
# 	except:
# 		print("no failed requests!")
# 	temp = pd.DataFrame(data=temp, columns=['user','service','instances','successful','failed'], index=[index])
# 	df = pd.concat([temp, df])

df.to_csv("machine_24.csv")
