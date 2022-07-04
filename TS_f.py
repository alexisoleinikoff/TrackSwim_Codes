### FICHIER DES FONCTIONS ET CLASSES ###

from datetime import timedelta
import time
import os
import pymysql
import shutil
import configparser
import TS_var

### FONCTIONS DE TRAITEMENT DES MESURES ###

# Fonction renvoyant le temps écoulé, en milisecondes, depuis 1970
# Arguments : NULL
# Retourne : INTEGER, temps en millisecondes
def millis():
    return int(time.time()*1000)

# Fonction transformant la différence entre deux temps donnés en millisecondes
# en un string au format "hh:mm:ss"
# Arguments : INT Temps 1, INT Temps 2
# Retourne : STRING au format hh:mm:ss
def millis_to_hhmmss(t_initial, t_fin):
    x = str(timedelta(milliseconds = t_fin - t_initial))
    x = x.split('.')[0]
    if len(x) < 8:
        x = '0' + x
    return x

# Fonction transformant la différence entre deux temps donnés en millisecondes
# en un string au format "mm:ss:msms"
# Arguments : INT Temps 1, INT Temps 2
# Retourne : STRING au format mm:ss:msms
def millis_to_mmssms(t_initial, t_fin):
    x = str(timedelta(milliseconds = t_fin - t_initial))
    x = x.split(':')
    x = x[1] + ':' + x[2]
    x = x.replace('.',':')[:8]
    if len(x) < 8:
        x = x + ':00'
    return x

# Vérifie si un EPC existe déjà dans la liste lst de stockage
# Trie aussi parmis les sessions fermées et ouvertes et ne
# renvoie l'index que de la session ouverte
# Arguments : LISTE de SESSION lst, INT EPC
# Retourne : INT j, l'index
def EPC_exist(lst, EPC):
    i = None
    for j in range(len(lst)):
        if lst[j].EPC == EPC and lst[j].session_end != None:
            i = i
            break
    return i


class session():
    def __init__(self, EPC, session_start, session_end=None):
        self.EPC = EPC

        self.session_start = session_start
        self.session_end = session_end

        self.depart = []
        self.arrivee = []


### FONCTIONS DE CONTRÔLE DU MODULE ###
class rgb():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

# Interrupt bouton 1
def button1_callback(channel):
    TS_var.flagButton1 = True

# Interrupt bouton 2
def button2_callback(channel):
    TS_var.flagButton2 = True


# Gestion du fichier de configuration config.ini
class config():
    def __init__(self, configname):
        self.name = configname
        self.config = configparser.ConfigParser()

    # Initialise les paramètres du fichier de configuration
    # Corrige à la valeur de initiale si aucun fichier ou fichier erroné trouvé
    def config_setup(self):
        if not self.config_exists():
           self.config_reset()
        
        self.config_ini_var()
        self.config_write_module()
        self.config_ini_var()


    # Lis le fichier de configuration et initialise les variables globales
    def config_ini_var(self):
        self.config.read(self.name)

        if 'Module' in self.config and 'DB_con' in self.config:
            for key in self.config['Module']:
                TS_var.module.append(self.config['Module'][key])

            for key in self.config['DB_con']:
                TS_var.DB_connect.append(self.config['DB_con'][key])

        else:
            self.config_reset()
            self.config_ini_var()
    
    # Vérifie si le fichier de configuration existe
    def config_exists(self):
        return True if os.path.exists(self.name) else False

    # Remet à 0 du fichier de configuration
    def config_reset(self):
        shutil.copy("reset_config.ini", "config.ini")

    
    # Récupère et modifie les paramètres "MODULE"
    def config_write_module(self):
        sql = DB_con(TS_var.DB_connect)
        
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

# Se connecte à la base de donnée et renvoi son objet
def DB_con(id_con):
    try:
        return pymysql.connect(host=id_con[0],
                user=id_con[1],
                password=id_con[2],
                database=id_con[3])

    except:
        return False