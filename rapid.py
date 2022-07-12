import sys
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages') # Lien vers tm1637
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages/python-mercuryapi') # Lien vers python-mercuryapi
import mercury
import RPi.GPIO as GPIO

GPIO.setup(8, GPIO.OUT)
GPIO.setup(8, GPIO.HIGH)

try:
    while True:
        pass

except KeyboardInterrupt:
    GPIO.cleanup()
