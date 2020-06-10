import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
BUTTON = 17

print ("Distance Measurement In Progress")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN)

prev_input = 1
i = 0

try:
    while True:

        input_state = GPIO.input(BUTTON)

        if (input_state == False):
           
            GPIO.output(TRIG, False)
            print ("Waiting For Sensor To Settle")
            time.sleep(1)
            
            GPIO.output(TRIG, True)
            time.sleep(0.000001)
            GPIO.output(TRIG, False)
            
            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()
                
            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()
                
            pulse_duration = pulse_end - pulse_start
            
            distance = pulse_duration * 17150
            
            distance = round(distance, 2)
            
            print ("Distance:", distance, "cm")

            prev_input = input
            
            time.sleep(0.05)

except KeyboardInterrupt:  
    
    print("STOP")
  
except:  
    
    print("Other error or exception occurred!" )
  
finally:  
    GPIO.cleanup()
        
