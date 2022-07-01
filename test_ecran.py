#!/usr/bin/env python3
from __future__ import print_function
import sys
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages') # Lien vers tm1637
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages/python-mercuryapi') # Lien vers python-mercuryapi

# Modules téléchargés
import mercury #https://github.com/gotthardp/python-mercuryapi
import tm1637 #https://github.com/depklyon/raspberrypi-tm1637

# Modules standards
from datetime import timedelta
import time
import RPi.GPIO as GPIO

# Modules créés
import config
from TS_f import button1_callback, button2_callback, millis, millis_to_hhmmss, millis_to_mmssms, rgb

GPIO.setwarnings(False)

### Constantes
# /!\ Valeurs correspondent au numéro GPIO du pin
# et non pas au numéro du pin
LED_YELLOW = 4
LED_BLUE = 27
BUTTON1 = 17
BUTTON2 = 22
BUZZER = 18
led_wifi = rgb(r=10, g=9, b=11)
CLK_GREEN = 3
DIO_GREEN = 2
CLK_BLUE = 24
DIO_BLUE = 23
T_UPDATE_SCREEN = 20 #ms
ANTI_BOUNCE = 100 #ms

### Initialisation des GPIO
GPIO.setmode(GPIO.BCM)

# Leds
GPIO.setup(LED_YELLOW, GPIO.OUT)
GPIO.setup(LED_BLUE, GPIO.OUT)
GPIO.setup(led_wifi.r, GPIO.OUT)
GPIO.setup(led_wifi.g, GPIO.OUT)
GPIO.setup(led_wifi.b, GPIO.OUT)

GPIO.output(LED_BLUE, GPIO.LOW)
GPIO.output(LED_YELLOW, GPIO.LOW)
GPIO.output(led_wifi.r, GPIO.LOW)
GPIO.output(led_wifi.g, GPIO.LOW)
GPIO.output(led_wifi.b, GPIO.LOW)

# Boutons
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON1, GPIO.FALLING, 
            callback=button1_callback, bouncetime=ANTI_BOUNCE)

GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON2, GPIO.FALLING, 
            callback=button2_callback, bouncetime=ANTI_BOUNCE)

# Buzzer
GPIO.setup(BUZZER, GPIO.OUT)
#buzz = GPIO.PWM(BUZZER, 100000)
#buzz.start(10)

# Initialisation des écrans
tmg = tm1637.TM1637(clk=CLK_GREEN, dio=DIO_GREEN) #GPIO NUM, écran vert, en haut
tmb = tm1637.TM1637(clk=CLK_BLUE, dio=DIO_BLUE) #GPIO NUM, écran bleu, en bas
tmb.brightness(1) # luminosité (de 1 à 7)
tmg.brightness(7)
tmb.write([0,0,0,0,0,0]) # valeurs initiales (écran vide)
tmg.write([0,0,0,0,0,0])

# Variables
t1, t_initial = millis()

# Test read
#reader = mercury.Reader("tmr:///dev/ttyS0", baudrate=115200)
#reader.set_region("EU3")
#reader.set_read_plan([1], "GEN2", read_power=1900)
#print(reader.read())

# Main
if __name__ == '__main__':
    try:
        while True:

            if(config.flagButton1 or config.flagButton2):
                t_initial = millis()
                config.flagButton1 = False
                config.flagButton2 = False

            # Mise à jour de l'écran
            if millis() - t1 > T_UPDATE_SCREEN:
                t1 = millis()
                tmg.write(tmg.encode_string(millis_to_mmssms(t_initial, millis())))
                tmb.write(tmb.encode_string(millis_to_hhmmss(t_initial, millis())))

    except KeyboardInterrupt:
        GPIO.cleanup()

