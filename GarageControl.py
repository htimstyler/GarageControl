import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   22 : {'name' : 'ShopLight0', 'state' : GPIO.HIGH},
   05 : {'name' : 'ShopLight1', 'state' : GPIO.HIGH}
   }

# Create a separate dictionary called mompins to store "momentary" pin numbers, name, and pin state:
mompins = {
   22 : {'name' : 'GarageDoor0', 'state' : GPIO.HIGH},
   05 : {'name' : 'GarageDoor1', 'state' : GPIO.HIGH}
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
   for mompin in mompins:
      mompins[mompin]['state'] = GPIO.input(mompin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'mompins' : mompins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = mompins[changePin]['name']
   if action == "push":
      GPIO.output(changePin, GPIO.LOW)
      time.sleep(0.2)
      GPIO.output(changePin, GPIO.HIGH)
      message = "The " + deviceName + " push."
   # For each pin, read the pin state and store it in the pins dictionary:
   for mompin in mompins:
      mompins[mompin]['state'] = GPIO.input(mompin)

   # Along with the pin dictionary, put the message into the template data dictoinary:
   templateData = {
      'message' : message,
      'mompins' : mompins
   }

   return render_template('main.html', **templateData)
   
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
