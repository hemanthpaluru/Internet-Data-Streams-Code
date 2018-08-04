from flask import Flask, render_template, send_from_directory
from tinydb import TinyDB, Query
import json
import private
import weather
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("default.html")

@app.route('/hello/<name>')
def get_hello(name):
    return render_template("hello.html", name=name)

@app.route('/greet/<guests>')
def get_greet(guests):
    guests = guests.split('-')
    return render_template("greet.html", guests=guests)

@app.route('/pizza')
def get_pizza():
    return render_template("pizza.html")

@app.route('/chart')
def get_chart():
    chart_name="Temp and Humidity over Time"
    x_name = "Time"
    y_names = ["Temp","Humidity"]
    data = [
        {'time':'1800',  'temp':28,   'humidity':87},
        {'time':'1900',  'temp':28,   'humidity':84},
        {'time':'2000',  'temp':27,   'humidity':82},
        {'time':'2100',  'temp':25,   'humidity':75},
        {'time':'2200',  'temp':28,   'humidity':87},
        {'time':'2300',  'temp':28,   'humidity':84},
        {'time':'2400',  'temp':27,   'humidity':82},
        {'time':'0000',  'temp':25,   'humidity':75}
    ]
    return render_template("chart.html",
                chart_name=chart_name,
                x_name=x_name, y_names=y_names,
                data=data
                )

@app.route('/barchart1')
def get_barchart1():
    db = TinyDB('data_buffer_cooler1.json')
    data = db.all()
    data = list(data)
    print(data)
    return render_template("barchart1.html",data=data)

@app.route('/barchart')
def get_barchart():
    return render_template("barchart.html")

@app.route('/map')
def get_map():
    return render_template("map.html",api_key=private.api_key)

@app.route('/map1')
def get_map1():
        # load the capitals information
    with open("us_state_capitals.json","r") as f:
        data = json.load(f)
        data = list(data.values())
    
    print(data)
    return render_template("map1.html",api_key=private.api_key,data=data)
	
@app.route('/map3')
def get_map3():
    # load the capitals information
    with open("us_state_capitals.json","r") as f:
        data = json.load(f)
        data = list(data.values())
    for item in data:
        w = weather.get_weather(lat=item['lat'],lon=item['lon'])
        temp = int(float(w['temp']) + 0.5)
        item['temp'] = str(temp)
        item['humidity'] = str(w['humidity'])
    print(data[0:2])
    return render_template("map3.html",api_key=private.api_key,data=data)

@app.route('/map4')
def get_map4():
    url = "http://hemanthpaluru.pythonanywhere.com"
    response = requests.get(url + "/query/example")
    assert response.status_code == 200
    data = list(response.json().values())
    for item in data:
        temp = int(float(item['temp']) + 0.5)
        item['temp'] = str(temp)
    print(data)
    return render_template("map4.html",api_key=private.api_key,data=data)


@app.route('/myhomemap')
def get_myhomemap():
    return render_template("myhomemap.html",api_key=private.api_key)

@app.route('/marker')
def get_marker():
    return render_template("marker.html",api_key=private.api_key)
	
@app.route('/icon/<path:path>')
def get_icon(path):
    return send_from_directory('icon', path)

@app.route('/js/<path:path>')
def get_js(path):
    return send_from_directory('js', path)

@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('static', path)

@app.route('/processing2/<int:diameter>')
def get_processing2(diameter=25):
    return render_template("processing2.html",diameter=diameter)

@app.route('/processing3')
def get_processing3():
    with open("us_state_capitals.json","r") as f:
        data = json.load(f)
        #data = list(data.values())
    print(data)
    states = list(data.keys())
    reds = []
    greens = []
    blues = []
    for state in states:
        item = data[state]
        w = weather.get_weather(lat=item['lat'],lon=item['lon'])
        print(w)
        temp = float(w['temp'])
        humidity = str(w['humidity'])
        red = int(temp * 5)
        if red < 0: 
            red = 0
        if red > 255:
            red = 255
        reds.append(red)
        greens.append(128)
        blues.append(128)
    return render_template("processing3.html",
                           states=states, 
                           reds=reds, 
                           greens=greens, 
                           blues=blues)

@app.route('/processing4')
def get_processing4():
    with open("us_state_capitals.json","r") as f:
        data = json.load(f)
        #data = list(data.values())
    print(data)
    states = list(data.keys())
    tem = []
    hum = []
    for state in states:
        item = data[state]
        w = weather.get_weather(lat=item['lat'],lon=item['lon'])
        print(w)
        temp = float(w['temp'])
        humidity = str(w['humidity'])
        tem.append(int(temp))
        hum.append(humidity)

    return render_template("processing4.html",
                           states=states, 
                           tem=tem,
                           hum=hum)

@app.route('/chartcooler1')
def get_chartcooler1():
    db = TinyDB('data_buffer_cooler1.json')
    data = db.all()
    data = list(data)
    print(data)
    return render_template("chartcooler1.html",data=data)

@app.route('/chartcooler2')
def get_chartcooler2():
    db = TinyDB('data_buffer_cooler2.json')
    data = db.all()
    data = list(data)
    print(data)
    return render_template("chartcooler2.html",data=data)

@app.route('/overallview')
def get_overallview():
    db1 = TinyDB('data_buffer_cooler1.json')
    db2 = TinyDB('data_buffer_cooler2.json')
    data1 = db1.all()
    data1 = list(data1)
    data2 = db2.all()
    data2 = list(data2)
    return render_template("overallview.html",data1=data1,data2=data2)

@app.route('/homepage')
def get_homepage():
    return render_template("homepage.html")




