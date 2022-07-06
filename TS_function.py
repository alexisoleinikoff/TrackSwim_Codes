### FICHIER DES FONCTIONS ET CLASSES ###

from datetime import timedelta
import time
import os
import pymysql
import shutil
import configparser
import RPi.GPIO as GPIO
import mercury
import TS_var

### Constantes (dupliquées de TS_main.py)
LED_YELLOW = 4
LED_BLUE = 27
BUTTON1 = 17
BUTTON2 = 22
BUTTON3 = 25

### FONCTIONS DE TRAITEMENT DES MESURES ###
def millis():
    """Fonction renvoyant le temps écoulé, en milisecondes, depuis le 01.01.1970\n
    Arguments : NULL
    Retourne : INTEGER, temps en millisecondes """

    return int(time.time()*1000)


def millis_to_hhmmss(t_initial, t_fin):
    """Fonction transformant la différence entre deux temps donnés en millisecondes
    en un string au format "hh:mm:ss"\n
    Arguments : INT Temps 1, INT Temps 2
    Retourne : STRING au format hh:mm:ss """

    x = str(timedelta(milliseconds = t_fin - t_initial))
    x = x.split('.')[0]
    if len(x) < 8:
        x = '0' + x
    return x


def millis_to_mmssms(t_initial, t_fin):
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

def ini_reader(read_pow):
    """ Initialise le lecteur RFID avec la puissance de lecture passée en argument\n
    Arguments : INT puissance de lecture
    Retourne : MERCURY reader"""

    if read_pow < 0:
        read_pow = 1
    if read_pow > 2700:
        read_pow = 2700

    reader = mercury.Reader("tmr:///dev/ttyS0", baudrate=115200)
    reader.set_region("EU3")
    reader.set_read_plan([1], "GEN2", read_power=read_pow)

    return reader

# Ajouter un tag à la base de données
def add_tag(reader, list):
    if not TS_var.etat_ajout_tag: # cas 0 : ne rien faire
        pass

    elif TS_var.etat_ajout_tag == 1: # cas 1 : scanner une fois et enregister les tags dans une liste temporaire
        GPIO.output(LED_BLUE, GPIO.HIGH)
        for tag in reader.read():
            if list:
                if not tag.epc in list:
                    list.append(tag.epc)
            else:
                list.append(tag.epc)

        GPIO.output(LED_BLUE, GPIO.LOW)

    else: # cas 2 : Mettre à jour la base de données
        print(list)
    
    TS_var.etat_ajout_tag = 0
    

class session():
    """ Classe régissant les paramètres d'une session de natation
    Le paramètre "session_end" est auto-initialisé à None\n
    Arguments: INT EPC, INT Début de session"""

    def __init__(self, EPC, session_start, session_end=None):
        self.EPC = EPC

        self.session_start = session_start
        self.session_end = session_end

        self.depart = []
        self.arrivee = []
    
    def EPC_exists(self, EPC):
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

class rgb():
    """ Classe régissant les paramètres des LEDs RGB
    Arguments : INT GPIO num rouge, INT GPIO num green, INT GPIO num bleu"""

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

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
        Retourne : NULL"""

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


def DB_connect(id_con):
    """Fonction se connectant à la base de donnée MySQL selon les paramètres de connexion donnés\n
    Arguments : LISTE information de connexion, au format : ['hôte', 'utilisateur', 'mots de passe', 'base de données']
    Retourne : PYMYSQL objet de connexion si connexion OK, sinon BOOL Faux"""

    try:
        return pymysql.connect(host=id_con[0],
                user=id_con[1],
                password=id_con[2],
                database=id_con[3])
    except:
        return False
