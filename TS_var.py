### FICHIER DE VARIABLES GLOBALES ###
from queue import Queue

# Variables du fichier de configuration
module = []
DB_connect = []

# LED RGB pour indicateur wifi
led_wifi = None

# Variables d'interuption
flagButton1 = False

etat_module = True # Vrai : Le module est en mode de fonctionnement normal (lecture, etc.), Faux : le module est en mode "configuration"
old_etat_module = False

button2timer = 0
etat_ajout_tag = 0 # 0 : Ne rien faire, 1 : Scanner un tag et enregistrer, 2 : Envoyer la liste des tags

quit_var = False # Variable permettant de quitter le programme, a modifier dans l'interrupt du bouton 4

q = Queue() # variable permettant de récupérer les données du thread parallèle (lecture des tags en continu)

