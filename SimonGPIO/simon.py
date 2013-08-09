#! /usr/bin/env python
import RPi.GPIO as GPIO
import random
import time
import sys
import os
#global levelNum

#340 hz : blue
#554 hz : yellow
#440 hz : red
#660 hz : green

GPIO.setmode(GPIO.BOARD)

GPIO.setup(21, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
#####preferences##########################################################
muted = False 
output = "local" #"local" is for headphone jack, "hdmi" is for hdmi audio
##########################################################################

buttons = [22, 24, 23, 21]
lights = [16, 18, 13, 11]
colors = ["red", "green", "yellow", "blue"]
sounds = ["toneRed.m4a", "toneGreen.m4a", "toneYellow.m4a", "toneBlue.m4a"]
beeps = []
pushes = []

def clearAll():
	for i in lights:
		GPIO.output(i, GPIO.LOW)
def levelgen():
	beeps.append(random.randrange(4))		

def level():
	global output
	levelgen()
	prev = 0
	for i in range(0, 4):
		GPIO.output(lights[i], GPIO.LOW)	
	for i in beeps:
		GPIO.output(lights[i], GPIO.HIGH)
		print colors[i]

		full_path = os.path.realpath(__file__)
		path, file = os.path.split(full_path)	

		os.system("omxplayer -w -o" + output + " " + path +"/audio/" + sounds[i] + ">/dev/null 2>/dev/null &")
		time.sleep(0.5)
		GPIO.output(lights[i], GPIO.LOW)
		time.sleep(0.1)	
	for k, v in enumerate((beeps)): #for each light enabled
		clearAll()
		waiting = True
		while waiting: #waiting for button to be pressed
			GPIO.output(lights[i], not  buttons[i]) 
			for i in range(0, 4): #for each button
				if (GPIO.input(buttons[i]) == 0): #if the button is enabled
				
					full_path = os.path.realpath(__file__)
					path, file = os.path.split(full_path)
					
					GPIO.output(lights[i], GPIO.HIGH)	

					os.system("omxplayer -w -o" + output + " " + path +"/audio/" + sounds[i] + ">/dev/null 2>/dev/null &")
					
					print colors[i] +  " pressed"
					
					if i != v: #if the button is incorrect
						print colors[i] + " is not " + colors[v]
						gameover()
					time.sleep(0.5)
					waiting = False
					GPIO.output(lights[i], GPIO.LOW)
					os.system("killall omxplayer")

					while (GPIO.input(buttons[i]) == 0):
						time.sleep(0.01)
						#os.system("killall omxplayer")
			time.sleep(0.01)
def gameover():
	running = False
	clearAll()
	sys.exit()			

def main():
	while True:
		level()	
		time.sleep(2)

def playsound(color):
	if(muted == False):
		print True
main()	

