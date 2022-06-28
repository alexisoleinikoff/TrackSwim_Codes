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
# Retourne : STRING 
def millis_to_hhmmss(t_initial, t_fin):
    x = str(timedelta(milliseconds = t_initial - t_fin))
    x = x.split('.')[0]
    if len(x) < 8:
        x = '0' + x
    return x