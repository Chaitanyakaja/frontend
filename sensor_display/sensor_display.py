from flask import Flask
from flask import render_template, redirect, url_for
import sys
import serial
import time

app = Flask(__name__)

#opens serial connection to arduino
usbport = '/dev/cu.usbmodemfd121'
ser = serial.Serial(usbport,9600)

sensors= {
	1 : {'name' : 'temp', 'reading' : 0},
	2 : {'name' : 'ph', 'reading' : 0},
    3 : {'name' : 'do', 'reading' : 0}
	#3 : {'name' : 'THREE', 'state' : GPIO.LOW}
}

def get_temp():
	ser.write('t')
	reading  = ser.readline()
	sensors[1]['reading']= reading
	return sensors


def get_ph():
    #takes reading from EC sensor
    ser.write('h')
    reading  = ser.readline()
    sensors[2]['reading'] = reading
    return sensors

def get_do():
    #takes reading from EC sensor
    #ser.write('1:r')
    #reading  = ser.readline()
    #mgL,percentsat = reading.split(",") #??
    sensors[3]['reading'] = 1
    return sensors

@app.route('/')
def index():
    data = {
        'sensors' : sensors
    }
    return render_template('index.html', **data) #later, data will = reading

@app.route('/update')
def update():

    temp = get_temp()
    ph = get_ph()
    #do = get_do()

    return redirect(url_for('index'))


app.run(debug = True, host = '0.0.0.0', port = 8000)
