from flask import Flask
from flask import render_template, redirect, url_for
#from apscheduler.scheduler import Scheduler #when I want it to update data automatically
import sys
import serial
import time

app = Flask(__name__)

#opens serial connection to arduino
usbport = '/dev/cu.usbmodemfa131'
#usbport = '/dev/cu.usbmodemfd121'
ser = serial.Serial(usbport,9600)

sensors= {
	1 : {'name' : 'Temp', 'command' : 't', 'reading' : 0},
	2 : {'name' : 'pH', 'command' : 'h', 'reading' : 0}
}

def get_updates():
	for num in sensors:
			ser.write(sensors[num]['command'])
			reading = ser.readline()
			sensors[num]['reading'] = reading
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


app.run(debug = True, host = '0.0.0.0', port = 8000)
