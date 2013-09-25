import RPi.GPIO as GPIO, time, os
import time
import sys

DEBUG = 1
GPIO.setmode(GPIO.BCM)
value = 0
oncounter = 0
offcounter = 0
currentLetter = []
message = []

def RCtime(RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(RCpin, GPIO.IN)
    while(GPIO.input(RCpin) == GPIO.LOW):
        
        reading +=1
    return reading


#Dictionary of Morse Code 
MorseCode = {'-----' : '0',
        '.----' : '1',
        '..---' : '2',
        '...--' : '3',
        '....-' : '4',
        '.....' : '5',
        '-....' : '6',
        '--...' : '7',
        '---..': '8',
        '----.' : '9',
        '.-' : 'A',
        '-...' : 'B',
        '-.-.' : 'C',
        '-..' : 'D',
        '.' : 'E',
        '..-.' : 'F',
        '--.' : 'G',
        '....' : 'H',
        '..' : 'I',
        '.---' : 'J',
        '-.-' : 'K',
        '.-..' : 'L',
        '--' : 'M',
        '-.' : 'N',
        '---' : 'O',
        '.--.' : 'P',
        '--.-' : 'Q',
        '.-.' : 'R',
        '...' : 'S',
        '-' : 'T',
        '..-' : 'U',
        '...-' : 'V',
        '.--' : 'W',
        '-..-' : 'X',
        '-.--' : 'Y',
        '--..': 'Z',
		'...-.-': 'SK'}

while True:
    value = RCtime(18)
    #print(value)

    #If value returned from RCtime is greater than 200, LED is OFF
    if value > 200 :
        #If oncounter is greater than zero, the LED was JUST turned off
        if oncounter > 0:
            
            if 7 <= oncounter <= 11:
                #A dot (1 unit)
				currentLetter.append('.')
                
            if  21 <= oncounter <= 33:
                #A dash (3 units)
				currentLetter.append('-')
                
        oncounter = 0
        offcounter = offcounter + 1

        #If there is a long pause, then the message has ended

        if offcounter > 200:
            key = ''.join(currentLetter)
            print(MorseCode[key])
            
            exit()
    #If value returned from RCtime is less than 200, LED is ON
    else:
        
        #If oncounter is greater than zero, the LED was JUST turned ON
        if offcounter > 0:
            print(offcounter)
            pass
        
            if 7 <= offcounter <= 11:
                #The space between parts of the same letter (1 unit)
                pass
            if  21 <= offcounter <= 40:
                #The space between letter (3 units)
				
				key = ''.join(currentLetter)
				if MorseCode[key] == 'SK' :
					exit()
				
                #Print the letter that corresponds to the Morse Code signal
				print(MorseCode[key])
                
				currentLetter[:] = []
                
            if 49 <= offcounter <= 120:
                #The space between words (7 units)
                key = ''.join(currentLetter)
                print(MorseCode[key])
                print(" ")
                currentLetter[:] = []
            
        offcounter = 0
        oncounter = oncounter + 1
