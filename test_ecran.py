import sys
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages') # Lien vers le dossier de stockage des packages pip3
import tm1637
import time
import RPi.GPIO as GPIO
from TS_f import millis, millis_to_hhmmss

GPIO.setwarnings(False)

# Constantes
LED_JAUNE = 4
LED_BLEU = 27
BOUTTON = 17
CLK_VERT = 2
DIO_VERT = 3
CLK_BLEU = 23
DIO_BLEU = 24
T_UPDATE_SCREEN = 20

# Initialisation des GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_JAUNE, GPIO.OUT)
GPIO.setup(LED_BLEU, GPIO.OUT)
GPIO.setup(BOUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(LED_BLEU, GPIO.LOW)
GPIO.output(LED_JAUNE, GPIO.LOW)

t1 = millis()
t_initial = t1

# Initialisation des écrans
tmd = tm1637.TM1637(clk=CLK_VERT, dio=DIO_VERT) #GPIO NUM, écran vert, en haut
tmt = tm1637.TM1637(clk=CLK_BLEU, dio=DIO_BLEU) #GPIO NUM, écran bleu, en bas

tmt.brightness(2) # luminosité (de 1 à 7)
tmd.brightness(7)

tmt.write([0,0,0,0,0,0]) # valeurs initiales (écran vide)
tmd.write([0,0,0,0,0,0])

# Main
try:
    while True:
        if millis() - t1 > T_UPDATE_SCREEN:
            t1 = millis()
            tmt.write(tmt.encode_string(millis_to_hhmmss(t_initial, millis())))

except KeyboardInterrupt:
    GPIO.cleanup()
