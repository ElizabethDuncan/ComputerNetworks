import RPi.GPIO as GPIO, time, os
import time
import sys

#Variables used by photoresistor for receiving Morse Code
DEBUG = 1
GPIO.setmode(GPIO.BCM)
value = 0
oncounter = 0
offcounter = 0
currentLetter = []
phrase = ""
message = []
begin = 0

#Variables used by LED for flashing Morse Code
#Set Morse Code's time unit
timeunit = 1;

#Dictionary of Morse Code 
MorseCodeLetters = {' ': 'X',
		'=': '...-.-',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..'}

#Set up the Raspberry Pi's connection to the board
LED_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def RCtime(RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(RCpin, GPIO.IN)
    while(GPIO.input(RCpin) == GPIO.LOW):
        
        reading +=1
    return reading

#Function that flashes the LED in convention with Morse Code's dot
def dot():
        print("dot");
	GPIO.output(LED_PIN, True)
	time.sleep(1*timeunit)
	GPIO.output(LED_PIN, False)
	time.sleep(1*timeunit)

#Function that flashes the LED in convention with Morse Code's dash
def dash():
        print("dash");
	GPIO.output(LED_PIN, True)
	time.sleep(3*timeunit)
	GPIO.output(LED_PIN, False)
	time.sleep(1*timeunit)

def repeat():
    input = phrase
    print(phrase);

#iterate through ever letter of the input
    for letter in input:
        print(letter)
	
	#look up each letter in the MorseCode dictionary
	for symbol in MorseCodeLetters[letter]:
		if symbol == '-':
			dash()
		elif symbol == '.':
			dot()
		#if the symbol is an X (which corresponds to a space between words), wait for 7 units
		elif symbol == 'X':
                        #sleep for 4 addtional time units (since it will also sleep 3 at the end of the letter)
                        #Total sleep (7 units) for new word
			time.sleep(4*timeunit)
		else:
			print("Error with MorseCode dictionary!")

        #sleep at the end of a letter           
        time.sleep(3*timeunit)
    return 0
    


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
    if value > 200:
        #If oncounter is greater than zero, the LED was JUST turned off
        if oncounter > 0:
            
            if 7 <= oncounter <= 11:
                print("Dot");
                currentLetter.append('.')
                
            if  21 <= oncounter <= 33:
                print("Dash");
                currentLetter.append('-')
                
        oncounter = 0
        offcounter = offcounter + 1

        #If there is a long pause, then the message has ended

        if offcounter > 100 and begin != 0:
            key = ''.join(currentLetter)
            if MorseCode[key] == 'SK' :
                if phrase[0] == '1':
                    phrase = phrase + "SK"
                    print("message received!")
                    print(phrase)
                    exit()
                else:
                    phrase = phrase + "="
                    print("repeating the message...")
                    repeat()
                    exit()
    #If value returned from RCtime is less than 200, LED is ON
    else:
        #Begin keeps track of how many times this has been called
        begin = begin + 1
        
        #If oncounter is greater than zero, the LED was JUST turned ON
        if offcounter > 0:
            print(offcounter);
            if 1 <= offcounter <= 15:
                #The space between parts of the same letter (1 unit)
                pass
            
            if  16 <= offcounter <= 40 and begin != 1:
                #The space between letter (3 units)

                key = ''.join(currentLetter)
                #Print the letter that corresponds to the Morse Code signal
                print(MorseCode[key])
                phrase = phrase + MorseCode[key]
                currentLetter[:] = []
                
            if 40 <= offcounter <= 120 and begin != 1:
                #The space between words (7 units)
                key = ''.join(currentLetter)
                print(MorseCode[key])
                phrase = phrase + MorseCode[key]
                print(" ")
                phrase = phrase + " "
                currentLetter[:] = []
            
        offcounter = 0
        oncounter = oncounter + 1

GPIO.cleanup()
