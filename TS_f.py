from datetime import timedelta
import time

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
        

