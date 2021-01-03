from django.shortcuts import render, redirect
from djusers.functions.functions import handle_uploaded_file
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.template import context
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import ast
from .forms import UserLoginForm, UserRegisterForm, StudentForm
import pika
import subprocess
import os
import os.path
import sys
from timeloop import Timeloop
from datetime import timedelta
import re
import psycopg2
import pandas as pd
import time

tl = Timeloop()
global jsondata 
jsondata = {
    "data" :'',
    "userid" : 0
}
global userglobalid
userglobalid = 0

def viewdata(request):
    userdata = {}
    connection = psycopg2.connect(user='user12',password="user",host='localhost',port='5433',database='analysis')
    cursor=connection.cursor()
    sql_select_Query = "select data from result where userid = %s order by calendar_date limit 10"
    print(request.user.id)
    useridtuple = (str(request.user.id),)
    cursor.execute(sql_select_Query,useridtuple)
    records = cursor.fetchall()
    for row in records:
        print(row)
    # print(records)
    userdata = {
        "data" : records
    }

    # userdata = djusers.objects.using('userdata').get()

    return render(request, "UserData.html", userdata)

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if request.user.is_superuser:
            return redirect('admin2/')

        if next:
            return redirect('UserDashboard/')

        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "signup.html", context)


def logout_view(request):
    global jsondata 
    jsondata = {
        "data" :'',
        "userid" : 0
    }
    logout(request)
    return redirect('/')

def getutilzationvalues(name):
    filepath = '../../' + name + 'Service/input_instances.sh'
    filepath1 = './input_instance.txt'

    print(filepath)
    wd = os.getcwd()
    process = subprocess.run(filepath,shell='true')

    # file getting created inside dashboar
    with open(filepath1, 'r') as file:
        data = file.read().replace('\n','')
        
    data = re.split('@|<|>@|',data)
    response={}
    for i in range(0,len(data)):
        print(data[i])
        response.update({name + str(i) : data[i]})
    print(response)
    return response

def admin2(request):
    jsondata = {}
    stats = getutilzationvalues("Input")
    jsondata.update(stats)
    stats = getutilzationvalues("Database")
    jsondata.update(stats)
    stats = getutilzationvalues("Analytics")
    jsondata.update(stats)
    stats = getutilzationvalues("Output")
    jsondata.update(stats)
    # jsondata = {
    #     "Input_CPU_Utilization" : 1,
    #     "Input_Memory_Utilization": 2,
    #     "Input_NoofInstances": 3,
    #     "Input_Service_Time" : 4,
    #     "Database_CPU_Utilization" : 1,
    #     "Database_Memory_Utilization": 2,
    #     "Database_NoofInstances": 3,
    #     "Database_Service_Time" : 4,
    #     "Analytics_CPU_Utilization" : 1,
    #     "Analytics_Memory_Utilization": 2,
    #     "Analytics_NoofInstances": 3,
    #     "Analytics_Service_Time" : 4,
    #     "Output_CPU_Utilization" : 1,
    #     "Output_Memory_Utilization": 2,
    #     "Output_NoofInstances": 3,
    #     "Output_Service_Time" : 4,

    # }
    print(jsondata)
    return render(request, "AdminDashboard.html",jsondata)

@csrf_exempt
def displaydataonUI(request):
    # print(request[body)
    # queryresult += request.body
    global jsondata
    value = "abc"
    jsondata.update({"data": jsondata["data"] + value})
    print(jsondata)
    # return render(request, "UserDashboard.html", jsondata)

@method_decorator(csrf_exempt, name='dispatch')
def acceptdata(request):
    print(request.body.decode("utf-8"))
    json_data = json.loads(request.body.decode("utf-8"))
    print(type(json_data))

    # data = {
    #     "sequence" : json_data,
    #     "userid" : request.user.id
    # }
    # print(type(data))
    # # call rabbitmq sender from here
    
    # #Create a new instance of the Connection object
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # #Create a new channel with the next available channel number or pass in a channel number to use
    # channel = connection.channel()
    # #Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
    # channel.queue_declare(queue='test_queue2')
    # channel.basic_publish(exchange='', routing_key='test_queue2', body=json.dumps(data))    

    # print("Sent JSON data")

    # connection.close()

    # response = {
    #     "success" : True
    # }


    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    #Create a new channel with the next available channel number or pass in a channel number to use

    channel = connection.channel()

    #Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.

    channel.queue_declare(queue='input_queue')

    df = pd.read_csv("Online Retail.csv")
    start_index = 0
    end_index = 99

    print(userglobalid)

    jsondata ={
        "userid" : str(userglobalid),
        "data" :[],
        "sequence" : json_data
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
    response = {
        "body" : "dfhjah"
    }

    return JsonResponse(response)

def index(request):
    # if request.method == 'POST':
    #     answer = request.POST['dropdown12']
    #     print(answer)

    #     # value = request.POST['dd1']
    #     # print(value)
    #     return HttpResponse("hello")
    # else:
    #     print(jsondata)
    #     # student = StudentForm()
    #     # jsondata = {
    #     #     "a" : "a1234",
    #     #     "b" : "b123",
    #     #     "c" : "nasb1",
    #     #     "data" : "sdbhasd"
    #     # }
    # get
    print(request.user.id)
    global userglobalid
    userglobalid = request.user.id
    return render(request, "UserDashboard.html", jsondata)
