from flask import Flask
from flask import render_template, redirect, url_for
#from apscheduler.scheduler import Scheduler #when I want it to update data automatically
import sys
import serial
from pyduino import *
import time
from array import array

app = Flask(__name__)

#opens serial connection to arduino/raspberry pi
#usbport = '/dev/cu.usbmodemfa131'
usbport = '/dev/cu.usbmodemfd121'
ser = serial.Serial(usbport,9600) #note the use of usbport variable

sensors = {
	0 : {'name' : 'pH', 'command' : '0:r', 'reading' : 'N/A'},
	1 : {'name' : 'Temp', 'command' : '1:r', 'reading' : 'N/A'},
	2 : {'name' : 'DO', 'command' : '2:r', 'reading' : 'N/A'},
	#3 : {'name' : 'Humidity', 'command' : '2:r', 'reading' : 'N/A'}
	#3 : {'name' : 'temp', 'command' : ['1','2','3'], 'reading' : 'N/A'},
#	2 : {'name' : 'temp_k', 'command' : '1:f', 'reading' : 'N/A'},
#	2 : {'name' : 'Humidity', 'command' : 'h', 'reading' : 'N/A'}
}

config = {
	1: {'response' : '1:response\r'},
}
def get_updates():
	for num in config:
		ser.write(config[num]['response'])

	for num in sensors:
		ser.write(sensors[num]['command'])
		if ser.readline() > 0:
			reading = ser.readline()
		#else 'N/A'
		#reading = ser.readline()
		sensors[num]['reading'] = reading
		time.sleep(1)

	return 0

@app.route('/')
def index():
	get_updates()
	data = {
    	'sensors' : sensors
	}
	return render_template('index.html', **data) #later, data will = reading


@app.route('/update')
def update():
	return redirect(url_for('index'))


app.run(debug = True, host = '0.0.0.0', port = 5000)
