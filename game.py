import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)

## Initialisation des variables
# Input/Output
ledY = 4
ledB = 27
button = 17

# Temps
waiting = time.time()
blinkTime = time.time()
randUp = 3000 #ms
randDown = 200 #ms
rand = float(random.randint(randDown, randUp))/1000
constLedUp = [0.15, 0.35, 0.6] #s
buffer = 0.2 #s
waitOk = False

# Input utilisateur
userInput = 0
userInputOk = False

# Résultat
game = 0 # 0 = attente, 1 = round perdu, 2 = round gagné
wonAmm = 0
lossAmm = 0

# Input
stateTimer = time.time()
aRebond = 0.05
state = False
pressedAlready = False

# Initialisation des pins
GPIO.setup(ledY, GPIO.OUT)
GPIO.setup(ledB, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(ledY, GPIO.LOW)
GPIO.output(ledB, GPIO.LOW)

# Main
try:
	# Initialisation du jeu
	while not userInputOk:
		userInput = int(input("Veuillez sélectionner la difficulté (ordre décroissant : 0,1,2): "))
		if userInput == 0 or userInput == 1 or userInput == 2:
			userInputOk = True
		else:
			print("Erreur. Sélection de 0 à 2")

	print("3...")
	time.sleep(0.75)
	print("2...")
	time.sleep(0.75)
	print("1...")
	time.sleep(0.75)
	print("GO!")
	time.sleep(0.75)

	# Jeu en boucle
	while True:
		blinkTime = time.time() if not waitOk else blinkTime

		# Attente avant que la led s'allume
		if time.time() - waiting > rand:
			waitOk = True
			GPIO.output(ledY, GPIO.HIGH)

		# Condition de reset
		if time.time() - blinkTime > constLedUp[userInput] or game:
			GPIO.output(ledY, GPIO.LOW)
			if game == 2:				# Si gagné
				wonAmm += 1
				GPIO.output(ledB, GPIO.HIGH)
				time.sleep(1)
				GPIO.output(ledB, GPIO.LOW)
			else:					# Si en attente ou perdu
				lossAmm += 1

			waiting = time.time()
			rand = float(random.randint(randDown, randUp))/1000
			game = 0
			waitOk = False

		# Gestion de l'input
		if not GPIO.input(button):
			stateTimer = time.time()
			state = True
		elif time.time() - stateTimer > aRebond:
			state = False
		else:
			pass

		# Gestion de la réussite ou échec
		if not game:
			if waitOk and state:							# Appuyé au bon moment ? -> gagné
				game = 2
			elif not waitOk and state and time.time() - waiting > buffer:		# Appuyé trop tôt ? -> perdu
				game = 1							# Buffer si appuyé trop tard
			else:									# Autre cas, encore en attente
				pass

except KeyboardInterrupt:
	print("")
	print("Parties jouées : " +str(wonAmm+lossAmm))
	print("Taux de réussite: "+str(int((wonAmm/(wonAmm+lossAmm))*100))+"% "+"("+str(wonAmm)+")")
	GPIO.cleanup()
