import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   17 : {'name' : 'ShopLight0', 'state' : GPIO.HIGH},
   27 : {'name' : 'ShopLight1', 'state' : GPIO.HIGH}
   }

# Create a separate dictionary called mompins to store "momentary" pin numbers, name, and pin state:
mompins = {
   05 : {'name' : 'GarageDoor0', 'state' : GPIO.HIGH},
   22 : {'name' : 'GarageDoor1', 'state' : GPIO.HIGH}
   }

# Set each pin as an output and make it high:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.HIGH)
   
# Set each mompin as an output and make it high:
for mompin in mompins:
   GPIO.setup(mompin, GPIO.OUT)
   GPIO.output(mompin, GPIO.HIGH)
   
@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
  
   # For each pin, read the pin state and store it in the pins dictionary:
   for mompin in mompins:
      mompins[mompin]['state'] = GPIO.input(mompin)
	  
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'mompins' : mompins,
      'pins' : pins
      }
	  
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):

   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
  
 # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.LOW)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.HIGH)
      message = "Turned " + deviceName + " off."
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."
   
 # Get the device name for the pin being changed:
   momdeviceName = mompins[changePin]['name']

 # If the action part of the URL is "push", execute the code indented below:
   if action == "push":
      GPIO.output(changePin, GPIO.LOW)
      time.sleep(0.2)
      GPIO.output(changePin, GPIO.HIGH)
      message = "The " + momdeviceName + " push."
	  
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # For each pin, read the pin state and store it in the pins dictionary:
   for mompin in mompins:
      mompins[mompin]['state'] = GPIO.input(mompin)

   # Along with the pin dictionary, put the message into the template data dictoinary:
   templateData = {
      'message' : message,
      'mompins' : mompins,
      'pins' : pins
   }
   
   return render_template('main.html', **templateData)
   
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
