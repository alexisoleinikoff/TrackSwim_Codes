
from __future__ import print_function
import sys
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages') # Lien vers tm1637
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages/python-mercuryapi') # Lien vers python-mercuryapi

import mercury
import tm1637
from datetime import timedelta
import time
import RPi.GPIO as GPIO
from TS_f import millis, millis_to_hhmmss, millis_to_mmssms

GPIO.setwarnings(False)

# Constantes
LED_JAUNE = 4
LED_BLEU = 27
BOUTON = 17
BOUTON2 = 22
BUZZER = 18
LED_RGB_R = 10
LED_RGB_G = 9
LED_RGB_B = 11
CLK_VERT = 3
DIO_VERT = 2
CLK_BLEU = 24
DIO_BLEU = 23
T_UPDATE_SCREEN = 20 #ms
ANTI_REBOND = 50 #ms

# Initialisation des GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_JAUNE, GPIO.OUT)
GPIO.setup(LED_BLEU, GPIO.OUT)
GPIO.setup(LED_RGB_R, GPIO.OUT)
GPIO.setup(LED_RGB_G, GPIO.OUT)
GPIO.setup(LED_RGB_B, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(BOUTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOUTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(LED_BLEU, GPIO.LOW)
GPIO.output(LED_JAUNE, GPIO.LOW)
#buzz = GPIO.PWM(BUZZER, 100000)
#buzz.start(10)

GPIO.output(LED_RGB_R, GPIO.LOW)
GPIO.output(LED_RGB_B, GPIO.LOW)
GPIO.output(LED_RGB_G, GPIO.LOW)

# Initialisation des écrans
tmd = tm1637.TM1637(clk=CLK_VERT, dio=DIO_VERT) #GPIO NUM, écran vert, en haut
tmt = tm1637.TM1637(clk=CLK_BLEU, dio=DIO_BLEU) #GPIO NUM, écran bleu, en bas

tmt.brightness(1) # luminosité (de 1 à 7)
tmd.brightness(7)

tmt.write([0,0,0,0,0,0]) # valeurs initiales (écran vide)
tmd.write([0,0,0,0,0,0])

# Variables
t1 = millis()
t2 = t1
t_initial = t1
state_timer = t1
state = False

# Test read
reader = mercury.Reader("tmr:///dev/ttyS0", baudrate=115200)
reader.set_region("EU3")
reader.set_read_plan([1], "GEN2", read_power=1900)
print(reader.read())

# Main
try:
    while True:
        # Gestion de l'input
        if not GPIO.input(BOUTON2):
            state_timer = millis()
            state = True
        elif millis() - state_timer > ANTI_REBOND:
            state = False
        else:
            pass

        if(state):
            t_initial = millis()

        # Mise à jour de l'écran
        if millis() - t1 > T_UPDATE_SCREEN:
            t1 = millis()
            tmd.write(tmd.encode_string(millis_to_mmssms(t_initial, millis())))
            tmt.write(tmt.encode_string(millis_to_hhmmss(t_initial, millis())))


except KeyboardInterrupt:
    GPIO.cleanup()

