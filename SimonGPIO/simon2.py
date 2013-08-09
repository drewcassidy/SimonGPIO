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
while True:
	for i in range(0, 4):
		GPIO.output(lights[i], not GPIO.input( buttons[i]))
		print GPIO.input(buttons[i])		
