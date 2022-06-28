import sys
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages')

import tm1637
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

# Fonctions
def milis():
    return int(time.time()*1000)

# Initialisation
GPIO.setmode(GPIO.BCM)

dT = 1000
t1 = milis()
i = 1

LED_JAUNE = 4
LED_BLEU = 27
BOUTTON = 17
CLK_VERT = 2
DIO_VERT = 3
CLK_BLEU = 23
DIO_BLEU = 24

GPIO.setup(LED_JAUNE, GPIO.OUT)
GPIO.setup(LED_BLEU, GPIO.OUT)
GPIO.setup(BOUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Déclaration des pins I/O
tmd = tm1637.TM1637(clk=CLK_VERT, dio=DIO_VERT) #GPIO NUM, écran vert, en haut
tmt = tm1637.TM1637(clk=CLK_BLEU, dio=DIO_BLEU) #GPIO NUM, écran bleu, en bas

# Luminosité 
tmt.brightness(2)
tmd.brightness(7)

# Initialisation à 0 des écrans et LEDs
tmt.write([0,0,0,0,0,0])
tmd.write([0,0,0,0,0,0])
GPIO.output(LED_BLEU, GPIO.LOW)
GPIO.output(LED_JAUNE, GPIO.LOW)


# Main
try:
    while True:
        
        
        
        if (milis() - t1 > dT):
            t1 = milis()
            tmt.write(tmt.encode_string(str(i)))
            i += 1


except KeyboardInterrupt:
    GPIO.cleanup()
