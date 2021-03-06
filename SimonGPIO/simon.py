#! /usr/bin/env python

import RPi.GPIO as GPIO
import random
import time
import sys
import os
import thread

########################## Preferences ##########################

muted = False
output = "local"   #headphone jack = "local", HDMI audio = "hdmi"

buttons = [22, 24, 23, 21]                      #button GPIO pins
lights = [16, 18, 13, 11]                          #LED GPIO pins
colors = [                            	           #button colors
	"red", "green",
	"yellow", "blue"
	 ]
sounds = [			                #audio file names
	"toneRed.m4a", "toneGreen.m4a",
	"toneYellow.m4a", "toneBlue.m4a"
	 ]
debug = True                                          #Debug mode
beeps = []

########################## GPIO Setup ##########################

GPIO.setmode(GPIO.BOARD)

for button in buttons:
	GPIO.setup(button, GPIO.IN)

for light in lights:
	GPIO.setup(light, GPIO.OUT)

########################### Functions ###########################

def clearAll():
	for light in lights:
		GPIO.output(light, GPIO.LOW)
		
def debugLog(text):
	if debug:
		print text
	
def blink(color, duration):
	GPIO.output(lights[color], GPIO.HIGH)
	time.sleep(duration)
	GPIO.output(lights[color], GPIO.LOW)
	
def blinkLight(color, duration):
	try:
		thread.start_new_thread(blink, (color,duration)) #time will get faster over time in future
	except:
		print "Error, unable to create thread"
		
def tone(sound):
	if(muted == False):
		path, file = os.path.split(os.path.realpath(__file__))
		os.system("omxplayer -w -o" + output + " " + path +"/audio/" + sounds[sound] + ">/dev/null 2>/dev/null &")

def showPattern(beeps):
	for i in beeps:
	
		blinkLight(i, 0.5) #duration will get faster over time in future
		tone(i)
		debugLog(colors[i])

		time.sleep(0.5)	
		
def levelgen():
	beeps.append(random.randrange(4))		

def level():
	global output

	levelgen()
	clearAll()	

	showPattern(beeps)
	
	for k, v in enumerate((beeps)): #for each light enabled
		clearAll()
		waiting = True
		while waiting: #waiting for button to be pressed
			for i in range(4): #for each button
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


main()	

