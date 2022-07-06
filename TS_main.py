#!/usr/bin/env python3
from __future__ import print_function
from pickle import TRUE
import sys
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages') # Lien vers tm1637
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages/python-mercuryapi') # Lien vers python-mercuryapi

# Modules téléchargés
import mercury #https://github.com/gotthardp/python-mercuryapi
import tm1637 #https://github.com/depklyon/raspberrypi-tm1637

# Modules standards
from datetime import timedelta
from threading import Thread, active_count
import time
import RPi.GPIO as GPIO

# Modules créés
import TS_var
from TS_function import *

if __name__ == '__main__':

    GPIO.setwarnings(False)

    ### Constantes
    # /!\ Valeurs correspondent au numéro GPIO du pin
    # et non pas au numéro du pin
    LED_YELLOW = 4
    LED_BLUE = 27
    BUTTON1 = 17
    BUTTON2 = 22
    BUTTON3 = 25
    BUZZER = 18
    led_wifi = rgb(10, 9, 11)
    CLK_GREEN = 3
    DIO_GREEN = 2
    CLK_BLUE = 24
    DIO_BLUE = 23

    T_UPDATE_SCREEN = 20 #ms
    ANTI_BOUNCE = 200 #ms
    SECONDE = 1000 #ms

    MAX_READ_POWER = 2700 #cdB
    MIN_READ_POWER = 1000 #cdB

    # Variables
    t1 = millis()
    t_initial = t1
    stock_tag = []
    session_list = []
    start_new_thread = True

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

    # Interuption sur le bouton 1 (bouton de gestion wifi/RàZ)
    GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON1, GPIO.FALLING, 
                callback=button1_callback, bouncetime=ANTI_BOUNCE)

    # Interuption sur le bouton 2 (bouton de gestion de l'ajout des tags dans la BD)
    GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON2, GPIO.BOTH, 
                callback=select_addTag_state, bouncetime=ANTI_BOUNCE)

    # Interuption sur le bouton 3 (bouton de gestion du mode "configuration" ou "continu")
    GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON3, GPIO.FALLING, 
                callback=switch_module_state, bouncetime=ANTI_BOUNCE)

    # Buzzer
    GPIO.setup(BUZZER, GPIO.OUT)
    #buzz = GPIO.PWM(BUZZER, 100000)
    #buzz.start(10)

    # Initialisation des écrans
    tmg = tm1637.TM1637(CLK_GREEN, DIO_GREEN) #GPIO NUM, écran vert, en haut
    tmb = tm1637.TM1637(CLK_BLUE, DIO_BLUE) #GPIO NUM, écran bleu, en bas
    tmb.brightness(1) # luminosité (de 1 à 7)
    tmg.brightness(7)
    tmb.write([0,0,0,0,0,0]) # valeurs initiales (écran vide)
    tmg.write([0,0,0,0,0,0])

    # Configuration initiale config.ini
    config('config.ini')

    # Main
    try:
        while True:

            # Si un changement d'état dans le module -> cleanup avant de changer
            if TS_var.etat_module != TS_var.old_etat_module:
                if TS_var.etat_module: # False -> True : Config -> Continu
                    print('Config -> Continu')
                else: # True -> False : Continu -> Config
                    print('Continu -> Config')


                    reader = ini_reader(MIN_READ_POWER)
                    tmg.write(tmg.encode_string('CONFIG'))

                TS_var.old_etat_module = TS_var.etat_module # Mise à jour de l'état du module



            # "Switch case" du mode de fonctionnement
            if(TS_var.etat_module): # Fonctionnement continu

                # Crée un nouveau thread si les valeurs de la queue ont été récupérés
                # et que le nombre de thread actif == 1 (== seul le main est actif)
                if start_new_thread and active_count() == 1:
                    t = Thread(target=read_continuous)
                    t.start()
                    start_new_thread = False

                # Vérifie si la queue est vide et récupére et traite les données si c'est le cas
                # Passe à vrai la valeur permettant de relancer un thread
                # /!\ D'abord vérifier si c'est vide, ensuite récupérer la données
                # q.get() met en pause le programme tant qu'il n'a rien dans la queue
                if TS_var.q.qsize() != 0:
                   print('Scan fini : Vide') if TS_var.q.get() else print('Scan fini : Valeurs obtenues')
                   start_new_thread = True

                # Mise à jour de l'écran
                if millis() - t1 > T_UPDATE_SCREEN:
                    t1 = millis()
                    tmg.write(tmg.encode_string(millis_to_mmssms(t_initial, millis())))
                    tmb.write(tmb.encode_string(millis_to_hhmmss(t_initial, millis())))
            
            
            else: # Mode configuration
                add_tag(reader, stock_tag)

                if millis() - t1 > T_UPDATE_SCREEN:
                    t1 = millis()
                    tmb.write(tmb.encode_string(str(len(stock_tag))+' EPC'))


    except KeyboardInterrupt:
        GPIO.cleanup()

