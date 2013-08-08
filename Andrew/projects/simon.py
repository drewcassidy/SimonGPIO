import RPi.GPIO as GPIO
import random
import time
import sys

#global levelNum

GPIO.setmode(GPIO.BOARD)

GPIO.setup(21, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

buttons = [22, 24, 23, 21]
lights = [16, 18, 13, 11]
colors = ["red", "green", "yellow", "blue"]

beeps = []
pushes = []

def levelgen():
	beeps.append(random.randrange(4))		

def level(levelNum):
	levelgen()
	prev = 0
	for i in range(0, 4):
		GPIO.output(lights[i], GPIO.LOW)	
	for i in beeps:
		GPIO.output(lights[i], GPIO.HIGH)
		print colors[i]
		time.sleep(0.5)
		GPIO.output(lights[i], GPIO.LOW)
		time.sleep(0.1)	
	for k, v in enumerate((beeps)): #for each light enabled
		waiting = True
		while waiting: #waiting for button to be pressed
			for i in range(0, 4): #for each button
				GPIO.output(lights[i], not  buttons[i]) 
				if (GPIO.input(buttons[i]) == 0): #if the button is enabled
					print colors[i] +  " pressed"
					if i != v: #if the button is incorrect
						print colors[i] + " is not " + colors[v]
						gameover()
					waiting = False
					pushes.append(i)
					while (GPIO.input(buttons[i]) == 0):
						time.sleep(0.01)
			time.sleep(0.01)
def gameover():
	running = False
	sys.exit()			
def main():
	levelNum = 1
	while True:
		#print GPIO.input(22)
		#print random.randrange(1, 5, 1)	
		#for i in range(1,5):
			#GPIO.output(lights[i], not  GPIO.input(buttons[i]))	
		level(levelNum)	
		levelNum += 1
		time.sleep(2)
main()	

