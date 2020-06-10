# import necessary library
import RPi.GPIO as GPIO   
import time   

# to use Raspberry Pi board pin numbers 
GPIO.setmode(GPIO.BCM)   

# set up pin 11 as an output 
GPIO.setup(26, GPIO.IN)

# enter while loop unitl exit 
while True:

# set up input value as GPIO.11
   inputValue = GPIO.input(26)

# when user press the btn
   if inputValue== False:

# show string on screen 
      print("Button pressed ")
      while inputValue ==  False:  
# Set time interval as 0.3 second delay 
            time.sleep(0.3) 
