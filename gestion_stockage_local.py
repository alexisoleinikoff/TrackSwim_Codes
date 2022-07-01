from datetime import timedelta
import time
from TS_f import millis, millis_to_hhmmss, EPC_exist, session

#initialisation
firstDetec = True
stockage = [None]


#detection
EPC = ['E123344D6F', 'E1233123D6F', 'E1212433123D6F', 'E1212433123D6F']
t1 = [104182124, 102282124, 124182124, 104182909]

for u in range(len(EPC)):

    # !!
    if(firstDetec):
        stockage[0] = session(EPC[u], t1[u])
        firstDetec = False
    else:
        i = EPC_exist(stockage, EPC[u])
        if i == None:
            stockage.append(session(EPC[u], t1[u]))
        elif len(stockage[i].depart) > len(stockage[i].arrivee) :
            stockage[i].arrivee.append(t1[u])
        else:
            stockage[i].depart.append(t1[u])



