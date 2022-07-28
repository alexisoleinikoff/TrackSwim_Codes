### FICHIER DES FONCTIONS ET CLASSES ###

# Modules standards
from datetime import timedelta
from datetime import datetime
from threading import Thread
import time
import os
import pymysql
import shutil
import configparser
import RPi.GPIO as GPIO

# Modules installés
import mercury #https://github.com/gotthardp/python-mercuryapi
import tm1637 #https://github.com/depklyon/raspberrypi-tm1637

# Modules créés
import TS_var

### Constantes (dupliquées de TS_main.py)
LED_YELLOW = 4
LED_BLUE = 3

BUTTON1 = 5
BUTTON2 = 6
BUTTON3 = 13
BUTTON4 = 19

SECONDE = 1000 #ms
MINUTE = 60000 #ms

### FONCTIONS DE TRAITEMENT DES MESURES ###
def millis():
    """Fonction renvoyant le temps écoulé, en milisecondes, depuis le 01.01.1970\n
    Arguments : NULL
    Retourne : INTEGER, temps en millisecondes """

    return int(time.time()*1000)

class read_continuous(Thread):
    """Classe régissant le multi-threading du capteur RFID. A passer dans une variable ex : t = read_continus(arg1, 2, 3)
    afin de pouvoir utiliser les fonctions intéressantes de la threading librairie (principalement active_count())."""
    def __init__(self, enable_pin, blue_led_pin, read_pow):
        Thread.__init__(self)
        self.enable_pin = enable_pin
        self.blue_led_pin = blue_led_pin
        self.read_pow = read_pow
        GPIO.setup(self.enable_pin, GPIO.OUT)
        self.daemon = False
        self.start()

    def run(self):
        time.sleep(0.4) # Attendre pour le duty cycle
        GPIO.output(self.blue_led_pin, GPIO.HIGH) # Allumer led bleue
        reader = ini_reader(self.enable_pin, self.read_pow) # Initialiser le reader
        r = reader.read() # Effectuer une mesure
        time.sleep(0.1) # pause de 0.1 s afin de soulager le reader (évite des crash)
        GPIO.output(self.enable_pin, GPIO.LOW) # Eteindre le reader
        GPIO.output(self.blue_led_pin, GPIO.LOW) # Eteindre la led bleue
        TS_var.q.put(False) if not r else TS_var.q.put(r) # Mettre les informations récupérées dans la queue (= False si rien détecté)


def ini_reader(enable_pin, read_pow):
    """ Initialise le lecteur RFID avec la puissance de lecture passée en argument\n
    Arguments : INT puissance de lecture
    Retourne : MERCURY reader"""

    if read_pow < 1:
        read_pow = 1
    if read_pow > 2700:
        read_pow = 2700

    GPIO.output(enable_pin, GPIO.HIGH)
    time.sleep(0.1) # délai d'attente après la sortie de la mise en veille ~28ms
    reader = mercury.Reader("tmr:///dev/ttyS0", baudrate=115200)
    reader.set_region("EU3")
    reader.set_read_plan([1], "GEN2", read_power=read_pow)

    return reader

class tag_to_DB():
    """Classe régissant les procédures de récolte et d'envoi de nouveaux tags dans la base données.
    Cette classe ne doit être utilisé que pour le rajout de tag et non pas la réception et envoi de données (voir data())"""
    def __init__(self):
        self.stock_tag = [] 

    def manage_tags(self, enable_pin, read_pow, ecrans):
        """Fonction principale de la classe Tag_to_DB. À passer dans le main,
        là où l'on souhaite traiter la configuration de nouveaux tags.
        La variable globale TS_var.etat_ajout_tag permet de dicter (switch case 3 cas) la façon dont le code doit se comporter\n
        Arguments : soit-même, MERCURY reader à initialiser en dehors de la fonction avec ini_reader()
        Retourne : NULL"""
        if not TS_var.etat_ajout_tag: # cas 0 : ne rien faire
            pass
        elif TS_var.etat_ajout_tag == 1: # cas 1 : scanner une fois et enregister les tags dans une liste temporaire
            self.read_tags(enable_pin, read_pow)
            ecrans.display_tmb(str(len(self.stock_tag))+' EPC')
        else: # cas 2 : Mettre à jour la base de données
            self.upload_tags()
            ecrans.display_tmb(str(len(self.stock_tag))+' EPC')

    def read_tags(self, enable_pin, read_pow):
        """Fonction effectuant une seule lecture des tags environnants. Cette dernière trie aussi et n'enregistre
        que les tags qui n'ont pas encore été détectés, empêchant ainsi les doublons de tags dans la BD. Le tout est stocké dans self.stock_tag[]\n
        Arguments : soit-même, MERCURY reader à obtenir de add_tag()
        Retourne : NULL"""
        GPIO.output(LED_BLUE, GPIO.HIGH)
        reader = ini_reader(enable_pin, read_pow)
        r = reader.read()
        time.sleep(0.1)
        for tag in r:
            print('EPC : ', tag.epc)
            if self.stock_tag:
                if not tag.epc in self.stock_tag:
                    self.stock_tag.append(tag.epc)
            else:
                self.stock_tag.append(tag.epc)
        GPIO.output(enable_pin, GPIO.LOW)
        GPIO.output(LED_BLUE, GPIO.LOW)

        TS_var.etat_ajout_tag = 0


    def upload_tags(self):
        """Fonction permettant de charger sur la base de données tout les tags stockés dans self.stock_tag[].
        Pour chaque tag, vérifie si le tag n'est pas déjà présent dans la base de données et empêche l'envoi.
        Supprime la liste une fois qu'elle a été traitée\n
        Arguments : soit-même
        Retourne : False si la connexion SQL n'est pas établie, sinon Vrai"""
        if self.stock_tag != 0: # Au moins 1 tag à uploader
            # Transformation en string pour lecture DB
            for i in range(len(self.stock_tag)):
                self.stock_tag[i] = str(self.stock_tag[i])

            # Connexion à la BD
            sql = DB_connect(TS_var.DB_connect)
            if not sql:
                return False

            with sql:
                with sql.cursor() as cursor:
                    cursor.execute('SELECT * FROM tag')
                    r = cursor.fetchall() # Récupération de tout les tags déjà présents dans la DB
                    for ligne in r: # Éliminer les tags à double
                        self.stock_tag.remove(ligne[0]) if ligne[0] in self.stock_tag else False

                    for epc in self.stock_tag: # Insérer une nouvelle ligne pour chaque tag non présent
                        cursor.execute('INSERT INTO tag (EPC) VALUES (%s)', epc)

                    self.stock_tag.clear() # Nettoyer la liste

        TS_var.etat_ajout_tag = 0
        return True

class data():
    """ Class régissant toutes les données récupérées lors du fonctionnement du module.\n
    Variables importantes : \n
    LIST self.sessions_list : Contient toutes les sessions qui n'ont pas encore été traitées.\n
    LIST self.sessions_to_upload : Contient toutes les sessions fermées qui n'ont pas encore été téléchargées\n
    """
    def __init__(self):
        self.sessions_list = []
        self.sessions_to_upload = []

        self.sessions_total = 0
        self.time_to_close = millis()
    
    ### Fonctions d'ajouts / suppressions de sessions ###
    def add_sessions_total(self):
        """Ajoute +1 au compteur du nombre de session fermée depuis le lancement du programme\n
        Arguments : soit-même
        Retourn : NULL"""
        self.sessions_total += 1


    def add_session(self, session):
        """ Ajoute une session à la liste des sessions
        Arguments : soit-même, SESSION session à ajouter
        Retourne : NULL"""
        self.sessions_list.append(session)

    def remove_session(self, session):
        """ Supprime une session de la liste des sessions
        Arguments : soit-même, SESSION session à supprimer (/!\ Valeur et non pas index)
        Retourne : NULL"""
        self.sessions_list.remove(session)


    def add_sessions_to_upload(self, session):
        """Ajoute une session à la liste de sessin à sauvegarder
        Arguments : soit-même, SESSION session à ajouter
        Retourne : NULL"""
        self.sessions_to_upload.append(session)

    def clear_sessions_to_upload(self):
        """Supprime totalement la liste des session closes. À appeler une fois la sauvegarde terminée
        Arguments : soit-même
        Retourne : NULL"""
        self.sessions_to_upload.clear()

    ### Fonctions de traitement et envoi de données ###
    def data_treatment(self, TagReadData, THRESHOLD):
        """Fonction principale du traitement de données. Pour chaque TagReadData (contenant epc et timestamp),
        vérifie si une session valide existe et en ouvre une nouvelle si ce n'est pas le cas.
        Si une session correcte existe, détermine si la valeur du temps obtenue lors de la détection
        du tag est valide et enregistre un départ ou arrivée selon l'ordre : départ -> arrivée -> départ -> ...
        Se référer au schéma de fonctionnement disponible dans le rapport du projet pour plus d'information\n
        Arguments : soit-même, LIST TagReadData contenant epc et timestamp, CONST THRESHOLD permettant de déterminer
        si la valeur de temps obtenu est valide ou non
        Retourne : NULL"""
        i = 0

        for tag in TagReadData:
            for session in self.sessions_list: # Peut être en resverse ? gain de temps ?
                if session.is_EPC_and_active(tag.epc): #tag + session_end == none
                    if len(session.depart) <= len(session.arrivee):
                        session.add_depart(tag.timestamp)
                    elif tag.timestamp - session.depart[len(session.depart)-1] >= THRESHOLD:
                        session.add_arrivee(tag.timestamp) # ajoute la valeur d'arrivée
                        session.add_depart(tag.timestamp) # ajoute la valeur de départ
                    elif TS_var.module[3] == 'Pause': # Remettre à jour la valeur du départ si en mode "avec pauses"
                        session.depart[len(session.depart)-1] = tag.timestamp

                    break
                i += 1 # Incrémenter en dehors du break -> ne pas incrémenter lorsque session valide trouvée
    
            if i == len(self.sessions_list): # Testé tout les tags sans aucune session valide -> nouvelle session
                self.add_session(data.session(tag.epc, tag.timestamp))

            i = 0

    def close_sessions(self):
        """Fonction de clôture des sessions qui n'ont pas reçus de mise à jour depuis un certains temps.
        À appeler périodiquement dans le programme, juste avant la sauvegarde des données\n
        Arguments : soit-même
        Retourne : NULL"""
        t = time.time()

        for session in self.sessions_list:
            # Si la dernière valeur de départ a été pris il y a plus de 2 minutes et que la session est encore ouverte -> fermer session
            if session.session_end == None:
                if t - session.depart[len(session.depart) - 1] >= 3*MINUTE/1000:
                    session.session_end = session.depart.pop() # retirer la dernière valeur de départ et la mettre en tant que fin de session
            
            if session.session_end != None:
                self.remove_session(session)
                if len(session.depart) != 0: # ajouter la session à envoyer seulement si elle contient au moins une valeur de départ
                    self.add_sessions_to_upload(session)
                    self.add_sessions_total() # Incrémente le total de sessions fermées

    def upload_closed_sessions(self):
        """Fonction d'envoi des données des sessions fermées à la base de données. Se connecte à la base de données
        et effectue une série de requête SQL afin d'envoyer les données.
        Pour chaque session, crée une ligne dans la table session. Ensuite, pour chaque paire départ-arrivee,
        crée une ligne dans la table perf\n
        Arguments : soit-même
        Retourne : False si la connexion ne s'est pas établie correctement, Vrai si l'écriture s'est correctement déroulée"""
        if not self.sessions_to_upload:
            return True

        sql = DB_connect(TS_var.DB_connect)
        if not sql:
            return False

        with sql:
            with sql.cursor() as cursor:
                for session in self.sessions_to_upload:
                    # Etape 1 : Trouver l'ID_tag correspondant à EPC
                    cursor.execute("SELECT ID_tag FROM tag WHERE EPC=%s", str(session.EPC))
                    if not cursor.rowcount:
                        continue
                    r = cursor.fetchone()[0] #normalement pas de doublon, prend le premier unqiuement index 0

                    # Etape 2 : Trouver l'ID_utilisateur correspondant à ID_tag
                    cursor.execute("SELECT ID_utilisateur FROM association_utilisateur_tag WHERE ID_tag=%s", r)
                    if not cursor.rowcount:
                        continue
                    r = cursor.fetchone()[0] #normalement pas de doublon, prend le premier unqiuement index 0
                    

                    # Etape 3 : Insérer une nouvelle session pour cet ID_utilisateur et récupérer l'ID_session
                    command = "INSERT INTO session (Debut, Fin, ID_piscine, ID_utilisateur) VALUES (%s, %s, %s, %s)"
                    cursor.execute(command, (datetime.fromtimestamp(session.session_start),
                                            datetime.fromtimestamp(session.session_end),
                                            TS_var.module[1], r))
                    cursor.execute("SELECT @@IDENTITY") # Récupération de l'ID propre de la nouvelle session qui vient d'être créée
                    ID_session = cursor.fetchone()[0] 

                    # Etape 4 : Insérer toutes les performances [depart, arrivee] avec l'ID_session de la nouvelle session
                    for i in range(len(session.depart)):
                        command = "INSERT INTO perf (Depart, Arrivee, ID_session) VALUES (%s, %s, %s)"
                        cursor.execute(command, (session.depart[i], session.arrivee[i], ID_session))
        
        self.sessions_to_upload.clear()
        return True

    class session():
        """ Sous classe de data. Une session contient les éléments clés comme l'EPC du tag auquel
        elle est associée, sa date et temps de fin ainsi qu'une liste de départs et d'arrivées. 
        La différence entre arrivee[i] et depart[i] donne le temps d'un aller-retour.
        La valeur de fin de session "session_end" est initialisée à None et est modifiée par la suite,
        lors de la clôture de la session"""
        def __init__(self, EPC, session_start, session_end=None):
            self.EPC = EPC

            self.session_start = session_start
            self.session_end = session_end

            self.depart = [session_start, ]
            self.arrivee = []

        def add_depart(self, temps):
            """Ajoute une valeur de temps à la fin de la liste de départ\n
            Arguments : soit-même, INT temps
            Retourne : NULL"""
            self.depart.append(temps)
        
        def add_arrivee(self, temps):
            """Ajoute une valeur de temps à la fin de la liste d'arrivée\n
            Arguments : soit-même, INT temps
            Retourne : NULL"""
            self.arrivee.append(temps)

        def add_session_end(self, temps):
            """Met à jour la valeur de fin de session\n
            Arguments : soit-même, INT temps
            Retourne : NULL"""
            self.session_end = temps

        # Vérifie si une session existe déjà pour un EPC donné et qu'elle est active
        def is_EPC_and_active(self, EPC):
            """ Vérifie si une session existe déjéà pour un EPC donné et qu'elle est active\n
            Arguments : soit-même, STRING EPC d'un tag
            Retourne : True si EPC de la session correrspondant au EPC donné en argument
            et si elle n'est pas encore terminée. Dans le cas contraire, False"""
            return True if self.EPC == EPC and self.session_end == None else False

### FONCTIONS DE CONTRÔLE DU MODULE ###
def button1_callback(channel):
    """ Fonction d'appel lors d'une detection d'interuption sur le bouton 1.
    Ne renvoi rien mais modifie la variable globale correspondante\n
    Arguments : channel (interrupt)
    Retourne : NULL """
    TS_var.flagButton1 = True

def select_addTag_state(channel):
    """ Fonction d'appel lors d'une detection d'interuption sur le bouton 2.
    Ne renvoi rien mais modifie la variable globale correspondante\n
    Arguments : channel (interrupt)
    Retourne : NULL """
    if not TS_var.etat_module:
        if not GPIO.input(BUTTON2): # Bouton appuyé ?
            TS_var.button2timer = millis() # Si oui, temps actuel retenu
        else:
            if millis() - TS_var.button2timer >= SECONDE: # Quand relâché, compare le temps actuel et celui pris lors de l'appui
                TS_var.etat_ajout_tag = 2 # Si >= 1 seconde -> envoyer les données
            else:
                TS_var.etat_ajout_tag = 1 # Si < 1 seconde -> scanner un tag

def switch_module_state(channel):
    """ Fonction d'appel lors d'une detection d'interuption sur le bouton 3.
    Ne renvoi rien mais modifie la variable globale correspondante\n
    Arguments : channel (interrupt)
    Retourne : NULL """

    TS_var.etat_module = not TS_var.etat_module

def quit_script(channel):
    """ Fonction d'appel lors d'une detection d'interuption sur le bouton 4 (on/off).
    Modifie la variable globale permettant de quitter le script python3
    Arguments : channel (interrupt)
    Retourne : NULL """
    TS_var.quit_var = True

class six_digits():
    """ Classe régissant les afficheurs 6 digit à 7 segments. Dans cette classe, devrait être regroupé
    tout les écrans utilisés dans le programme. Ses sous fonctions permettent d'écrire et supprimer des informations
    sur les afficheurs."""
    def __init__(self, CLK_BLUE, DIO_BLUE, CLK_GREEN, DIO_GREEN):
        self.blank_screen = millis()
        self.time_switch_display = millis()
        self.display_state = True # Vrai : affiche la distance parcourue, Faux : durée totale de la session

        self.tmg = tm1637.TM1637(CLK_GREEN, DIO_GREEN) #GPIO NUM, écran vert, en haut
        self.tmb = tm1637.TM1637(CLK_BLUE, DIO_BLUE) #GPIO NUM, écran bleu, en bas

        self.tmb.brightness(1) # luminosité (de 1 à 7)
        self.tmg.brightness(7)

        self.tmb.write([0,0,0,0,0,0]) # valeurs initiales (écran vide)
        self.tmg.write([0,0,0,0,0,0])

    def update_displays(self, TagReadData, data):
        """Met à jour les valeurs à afficher sur les écrans selon les informations reçues du thread paralèlle (read).
        La puissance renvoyée par le tag (rssi) permet de déterminer quel nageur est le plus proche du module\n
        Arguments : LIST TagReadData contenant epc et rssi, LIST data de toutes les sessions en cours
        Retourne : False si aucun tag n'a été détecté, sinon NULL"""
        rssi_list = []

        for tag in TagReadData: # stocker tout les rssis des tags scannés
            rssi_list.append(tag.rssi)

        if not rssi_list: # vide ou pas
            return False # si vide, -> pas de donnée -> quitter la fonction

        index_max = rssi_list.index(max(rssi_list)) # trouver indexe où est la valeur max
        EPC_to_display = TagReadData[index_max].epc

        for session in data.sessions_list: 
            if session.is_EPC_and_active(EPC_to_display): # Vérifier l'EPC correspondant pour une session ouverte
                if session.arrivee:
                    l = len(session.arrivee)
                    self.display_tmg(self.millis_to_mmssms(1000*session.depart[l - 1],
                                                            1000*session.arrivee[l - 1]))
                    if self.display_state: # Afficher distance totale ou temps de session
                        self.display_tmb(str(l*2*int(float(TS_var.module[2])))) # distance totale
                    else:
                        self.display_tmb(self.millis_to_hhmmss(1000*session.session_start, millis()))  # temps de session
                else: # cas 'initiale' premier tag pas encore d'arrivée
                    self.time_switch_display = millis()
                    self.display_state = True
                    self.display_tmg('0')
                    self.display_tmb('0')
        

        # Gestion de changement de l'affichage (change chaque 5 secondes)
        if millis() - self.time_switch_display >= 5*SECONDE:
            self.time_switch_display = millis()
            self.display_state = not self.display_state

        self.blank_screen = millis()

    def display_tmg(self, string):
        """Affiche une chaîne de charactère sur l'écran vert. Pour une complète des charactères tolérés, consulter tm1637.py
        Arguments : LIST string a afficher
        Retourne : NULL"""
        self.tmg.write(self.tmg.encode_string(string))

    def display_tmb(self, string):
        """Affiche une chaîne de charactère sur l'écran bleu. Pour une complète des charactères tolérés, consulter tm1637.py
        Arguments : LIST string a afficher
        Retourne : NULL"""
        self.tmb.write(self.tmb.encode_string(string))

    def clear_screens(self):
        """Retire tout charactère des deux écrans
        Arguments : NULL
        Retourne : NULL"""
        self.tmb.write([0,0,0,0,0,0])
        self.tmg.write([0,0,0,0,0,0])

    def millis_to_hhmmss(self, t_initial, t_fin):
        """Fonction transformant la différence entre deux temps donnés en millisecondes
        en un string au format "hh:mm:ss"\n
        Arguments : INT Temps 1, INT Temps 2
        Retourne : STRING au format hh:mm:ss """

        x = str(timedelta(milliseconds = t_fin - t_initial))
        x = x.split('.')[0]
        if len(x) < 8:
            x = '0' + x
        return x

    def millis_to_mmssms(self, t_initial, t_fin):
        """Fonction transformant la différence entre deux temps donnés en millisecondes
        en un string au format "mm:ss:msms"\n
        Arguments : INT Temps 1, INT Temps 2
        Retourne : STRING au format mm:ss:msms"""

        x = str(timedelta(milliseconds = t_fin - t_initial))
        x = x.split(':')
        x = x[1] + ':' + x[2]
        x = x.replace('.',':')[:8]
        if len(x) < 8:
            x = x + ':00'
        return x

class rgb():
    """ Classe régissant les paramètres des LEDs RGB
    Arguments : INT GPIO num rouge, INT GPIO num green, INT GPIO num bleu"""
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

        GPIO.setup(self.r, GPIO.OUT)
        GPIO.setup(self.g, GPIO.OUT)
        GPIO.setup(self.b, GPIO.OUT)

        GPIO.output(self.r, GPIO.LOW)
        GPIO.output(self.g, GPIO.LOW)
        GPIO.output(self.b, GPIO.LOW)

    def light_red(self):
        GPIO.output(self.r, GPIO.HIGH)
        GPIO.output(self.g, GPIO.LOW)
        GPIO.output(self.b, GPIO.LOW)

    def light_green(self):
        GPIO.output(self.r, GPIO.LOW)
        GPIO.output(self.g, GPIO.HIGH)
        GPIO.output(self.b, GPIO.LOW)

    def light_blue(self):
        GPIO.output(self.r, GPIO.LOW)
        GPIO.output(self.g, GPIO.LOW)
        GPIO.output(self.b, GPIO.HIGH)

class config():
    """ Classe régissant le fichier de configuration
    Peut simplement être déclarée comme "config('config.ini')" pour initialiser les paramètres
    Arguments : STRING nom du fichier de configuration (config.ini)"""
    def __init__(self, configname):
        self.name = configname
        self.config = configparser.ConfigParser()

        self.config_setup()

    def config_setup(self):
        """ Fonction principale de la classe. Vérifie, corrige et met à jour le fichier de configuration\n
        Arguments : soit-même
        Retourne : NULL
        """
        if not self.config_exists():
           self.config_reset()
        
        self.config_ini_var()
        self.config_write_module()
        self.config_ini_var()

    def config_ini_var(self):
        """ Fonction lisant le fichier de configuration et initialisant les variables globales\n
        Arguments : soit-même
        Retourne : NULL"""
        self.config.read(self.name)

        if 'Module' in self.config and 'DB_con' in self.config:
            for key in self.config['Module']:
                TS_var.module.append(self.config['Module'][key])

            # Mode par défaut = Pause
            if TS_var.module[3] != 'Pause' or TS_var.module[3] != 'Continu':
                TS_var.module[3] = 'Pause'

            for key in self.config['DB_con']:
                TS_var.DB_connect.append(self.config['DB_con'][key])

        else:
            self.config_reset()
            self.config_ini_var()
    
    def config_exists(self):
        """Fonction vérifiant si le fichier de configuration existe\n
        Arguments : soit-même
        Retourne : BOOL : Vrai si trouvé, sinon Faux"""
        return True if os.path.exists(self.name) else False

    def config_reset(self):
        """Fonction remettant à zéro les valeurs du fichier de configuration. Se calque sur le fichier reset_config.ini\n
        Arguments : soit-même
        Retourne : NULL"""
        shutil.copy("reset_config.ini", "config.ini")

    def config_write_module(self):
        """Fonction se connectant, récupérant et modifiant les paramètres [Module] du fichier de configuration\n
        Arguments : soit-même
        Retourne : False si aucune connexion n'est réalisée, Vrai si l'écriture s'est passée correctement"""
        sql = DB_connect(TS_var.DB_connect)
        if not sql:
            return False

        with sql:
            with sql.cursor() as cursor:
                cursor.execute("SELECT Mode, ID_piscine FROM module WHERE ID_module=%s", TS_var.module[0])
                r = cursor.fetchone()
                
                self.config.set('Module', 'mode', r[0])
                self.config.set('Module', 'id_piscine', str(r[1]))

                cursor.execute("SELECT Longueur FROM piscine WHERE ID_piscine=%s", r[1])
                r = cursor.fetchone()
                self.config.set('Module', 'l_piscine', str(r[0]))
    
        with open(self.name, 'w') as configfile:
            self.config.write(configfile)

        return True

def DB_connect(id_con):
    """Fonction se connectant à la base de donnée MySQL selon les paramètres de connexion donnés\n
    Arguments : LISTE information de connexion, au format :
    [STR 'hôte', INT 'port', STR 'utilisateur', STR 'mots de passe', STR 'base de données']
    Retourne : PYMYSQL objet de connexion si connexion OK, sinon BOOL Faux"""
    try:
        sql = pymysql.connect(host=id_con[0],
                port=int(id_con[1]),
                user=id_con[2],
                password=id_con[3],
                database=id_con[4])

        if sql:
            TS_var.led_wifi.light_green()
            return sql
    except:
        TS_var.led_wifi.light_red()
        return False