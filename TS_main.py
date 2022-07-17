#!/usr/bin/env python3
from __future__ import print_function
from pickle import TRUE
import sys
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages') # Lien vers tm1637
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages/python-mercuryapi') # Lien vers python-mercuryapi

# Modules standards
from threading import active_count
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
    ENABLE =  8
    BUZZER = 18
    CLK_GREEN = 3
    DIO_GREEN = 2
    CLK_BLUE = 24
    DIO_BLUE = 23

    T_UPDATE_SCREEN = 30 #ms
    T_BLANK_SCREEN = 1000 #ms
    ANTI_BOUNCE = 200 #ms
    SECONDE = 1000 #ms
    MINUTE = 60000 #ms

    MAX_READ_POWER = 2700 #cdB
    READ_POWER = 2500 #cdB
    MIN_READ_POWER = 1000 #cdB

    V_MAX = 2.39 # vitesse moyenne du record du monde de natation 50m en 20.91s (google)

    # Variables
    t1 = millis()
    t_initial = t1
    stock_tag = []
    start_new_thread = True

    ### Initialisation des GPIO
    GPIO.setmode(GPIO.BCM)

    # Pin enable, permettant de contrôler on/off le module RFID
    GPIO.setup(ENABLE, GPIO.OUT)
    GPIO.setup(ENABLE, GPIO.LOW)

    # Leds
    TS_var.led_wifi= rgb(10, 9, 11)
    GPIO.setup(LED_YELLOW, GPIO.OUT)
    GPIO.setup(LED_BLUE, GPIO.OUT)
    GPIO.output(LED_BLUE, GPIO.LOW)
    GPIO.output(LED_YELLOW, GPIO.LOW)

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

    # Configuration initiale config.ini
    config('config.ini')

    # Initialisation des écrans et variables de stockage
    ecrans = six_digits(CLK_BLUE, DIO_BLUE, CLK_GREEN, DIO_GREEN)
    main_data = data()
    tag_data = Tag_to_DB()

    # Calcul du temps minimal pour un aller retour de module[l_piscine] mètres
    # Si un utilisateur réalise un temps plus petit que celui-ci, il n'est pas compté
    t_min = int(2*float(TS_var.module[2])/V_MAX)

    # Main
    try:
        while True:
            ### CLEANUP ###
            # Si un changement d'état dans le module -> cleanup avant de changer
            # Au lancement du module, commence toujours entrer dans la 1ère condition config->continu
            if TS_var.etat_module != TS_var.old_etat_module:
                TS_var.old_etat_module = TS_var.etat_module # Mise à jour de l'état du module

                if TS_var.etat_module: # False -> True : Config -> Continu
                    # Crée un nouveau thread si les valeurs de la queue ont été récupérés
                    # et que le nombre de thread actif == 1 (== seul le main est actif)
                    if active_count() == 1:
                        t = read_continuous(ENABLE, LED_BLUE, READ_POWER)

                else: # True -> False : Continu -> Config
                    t.join() # attente de la fin du thread
                    TS_var.q.get() # clear la queue
                    GPIO.output(LED_YELLOW, GPIO.LOW)
                    ecrans.display_tmg('CONFIG')
                    ecrans.display_tmb(str(len(tag_data.stock_tag))+' EPC')


            ### FONCTIONEMENT ###
            # Fonctionnement continu
            if(TS_var.etat_module):
                # Vérifie si la queue est vide et récupére et traite les données si c'est le cas
                # Passe à vrai la valeur permettant de relancer un thread
                # /!\ D'abord vérifier si c'est vide, ensuite récupérer la données
                # q.get() met en pause le programme tant qu'il n'a rien dans la queue
                if TS_var.q.qsize() != 0:
                    # Relance un thread, en paralelle du traitement de données
                    if active_count() == 1:
                        t = read_continuous(ENABLE, LED_BLUE, READ_POWER)

                    r = TS_var.q.get()
                    if r: # Données reçues -> traitement + mise à jour des écrans
                        GPIO.output(LED_YELLOW, GPIO.HIGH)
                        main_data.data_treatment(r, t_min)
                        ecrans.update_displays(r, main_data)
                        #print('Tag(s) détecté(s). Sessions en cours : [', len(main_data.sessions_list), ']')

                    else:
                        GPIO.output(LED_YELLOW, GPIO.LOW)
                        if millis() - ecrans.blank_screen >= T_BLANK_SCREEN:
                            ecrans.time_switch_display = millis()
                            ecrans.display_state = True
                            ecrans.clear_screens()
                        

                # Vérification et clôture des sessions
                if millis() - main_data.time_to_close >= 2*MINUTE:
                    main_data.time_to_close = millis()

                    #print('Commence la clôture de session ...')
                    main_data.close_sessions()
                    #print('... [', len(main_data.sessions_to_upload), "] sessions ont été fermées et sont prêtes à l'envoi")
                    main_data.upload_closed_sessions()
                    #print('Envoi terminé. Sessions en cours : [',len(main_data.sessions_list), '] -- Sessions encore à envoyer : [' , len(main_data.sessions_to_upload), ']')

            # Mode configuration
            else: 
                tag_data.manage_tags(ENABLE, MIN_READ_POWER, ecrans)


            time.sleep(0.01) #dors 10 ms -> réduction de fréquence et gain en durée de vie de batterie
    except KeyboardInterrupt:
        GPIO.cleanup()

