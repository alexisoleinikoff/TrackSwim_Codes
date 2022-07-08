from TS_function import SECONDE, millis_to_hhmmss, millis, DB_connect, config
from datetime import datetime
from datetime import datetime
import TS_var
import pymysql
import time

config('config.ini')

SECONDE = 1000 #ms
MINUTE = 60000 #ms

def decode_list(list):
    """Fonction permettant de décoder une lite de bytes en liste de string selon le code utf-8.
    Fonction non utilisée\n
    Arguments : LIST list à décoder
    Retourne : NULL"""
    i = 0
    for b in list:
        list[i] = b.decode("utf-8")
        i += 1

class tag():
    def __init__(self, EPC, t):
        self.epc = EPC
        self.timestamp = t

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
        l = 0

        for tag in TagReadData:
            for session in self.sessions_list: # Peut être en resverse ? gain de temps ?
                if session.is_EPC_and_active(tag.epc): #tag + session_end == none
                    if len(session.depart) <= len(session.arrivee):
                        session.add_depart(tag.timestamp)
                    elif tag.timestamp - session.depart[len(session.depart)-1] >= THRESHOLD:
                        session.add_arrivee(tag.timestamp) # ajoute la valeur d'arrivée
                        session.add_depart(tag.timestamp) # ajoute la valeur de départ
                    else:
                        session.depart[len(session.depart)-1] = tag.timestamp

                    break
                l += 1
    
            if l == len(self.sessions_list): # Testé tout les tags sans aucune session valide -> nouvelle session
                self.add_session(data.session(tag.epc, tag.timestamp))

            l = 0
        
    def close_sessions(self):
        """Fonction de clôture des sessions qui n'ont pas reçus de mise à jour depuis un certains temps.
        À appeler périodiquement dans le programme, juste avant la sauvegarde des données\n
        Arguments : soit-même
        Retourne : NULL"""
        for session in self.sessions_list:
            # Si la dernière valeur de départ a été pris il y a plus de 2 minutes et que la session est encore ouverte -> fermer session
            if session.session_end == None:
                if (millis() - session.depart[len(session.depart) - 1] >= 2):
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
        Retourne : False si la connexion ne s'est pas établie correctement"""
        sql = DB_connect(TS_var.DB_connect)
        if not sql:
            return False

        with sql:
            with sql.cursor() as cursor:
                for session in self.sessions_to_upload:
                    # Etape 1 : Trouver l'ID_tag correspondant à EPC
                    cursor.execute("SELECT ID_tag FROM tag WHERE EPC=%s", str(session.EPC))
                    r = cursor.fetchone()[0] #normalement pas de doublon, prend le premier unqiuement index 0

                    # Etape 2 : Trouver l'ID_utilisateur correspondant à ID_tag
                    cursor.execute("SELECT ID_user FROM association_utilisateur_tag WHERE ID_tag=%s", r)
                    r = cursor.fetchone()[0] #normalement pas de doublon, prend le premier unqiuement index 0

                    # Etape 3 : Insérer une nouvelle session pour cet ID_utilisateur et récupérer l'ID_session
                    command = "INSERT INTO session (Debut, Fin, ID_piscine, ID_user) VALUES (%s, %s, %s, %s)"
                    cursor.execute(command, (datetime.fromtimestamp(session.session_start),
                                            datetime.fromtimestamp(session.session_end),
                                            TS_var.module[1], r))
                    cursor.execute("SELECT @@IDENTITY") # Récupération de l'ID propre de la nouvelle session qui vient d'être créée
                    ID_session = cursor.fetchone()[0] 

                    # Etape 4 : Insérer toutes les performances [depart, arrivee] avec l'ID_session de la nouvelle session
                    for i in range(len(session.depart)):
                        command = "INSERT INTO perf (Depart, Arrivee, ID_session) VALUES (%s, %s, %s)"
                        cursor.execute(command, (session.depart[i], session.arrivee[i], ID_session))


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

a = data()

tag_list = []
epc = [b'E28011606000020A66893DC6', b'E28011606000020A4B109998',
        b'E2806890000000032AFD81E0', b'E200001974080202128097E1',
        b'E2806890000000032AFDC8D3', b'E200001B731102172540E2FC',
        b'E200341201321800048817DD', b'E280681000000039969F1C7A']
timestamp = [15, 13, 15, 15, 16, 17, 18, 19]

for i in range(len(epc)):
    tag_list.append(tag(epc[i], timestamp[i]))


# remplacer t par tag.timestamp dans le prog
a.data_treatment(tag_list, 2)

epc = [b'E28011606000020A66893DC6', b'E28011606000020A4B109998',
        b'E200001974080202128097E1', b'E2806890000000032AFDC8D3',
        b'E200341201321800048817DD', b'E280681000000039969F1C7A']
timestamp = [x+5 for x in timestamp]

tag_list.clear()

for i in range (len(epc)):
    tag_list.append(tag(epc[i], timestamp[i]))

a.data_treatment(tag_list, 2)

a.close_sessions()
a.upload_closed_sessions()

a.sessions_to_upload.clear() # supprimer les sessions une fois sauvegardées

