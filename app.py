
#connor.aitken@gmail.com


import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

#create a dictionary called pins to store the pin number, name, and pin state:

pins = {
	2 : {'name' : 'ONE', 'state' : GPIO.LOW},
	3 : {'name' : 'TWO', 'state' : GPIO.LOW},
	4 : {'name' : 'THREE', 'state' : GPIO.LOW},
	17 : {'name' : 'FOUR', 'state' : GPIO.LOW},
	27 : {'name' : 'FIVE', 'state' : GPIO.LOW},
	22 : {'name' : 'SIX', 'state' : GPIO.LOW},
	10 : {'name' : 'SEVEN', 'state' : GPIO.LOW},
	9 : {'name' : 'EIGHT', 'state' : GPIO.LOW}
	}
# set each pin as an output and make it low:
for pin in pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
	#for each pin, read the pin state and store it in the pins dictionary:
	for pin in pins:
		pins[pin]['state'] = GPIO.input(pin)
	#put the pin dictionary into the template data dictionary:
	templateData = {
	'pins' : pins
	}
	# pass the template data into the template main.html and return it to the user
	return render_template('index.html', **templateData)

#the function below is executed when someone requests a url with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):

   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']

   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : pins
   }

   return render_template('index.html', **templateData)
if __name__ == "__main__":
	app.run('10.0.0.145',port=5000, debug=True)
