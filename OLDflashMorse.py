import RPi.GPIO as GPIO
import time

#Set Morse Code's time unit
timeunit = 1;

#Dictionary of Morse Code 
MorseCode = {' ': 'X',
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

input = '1 E ='

#iterate through ever letter of the input
for letter in input:
	
	print(letter)
	
	#look up each letter in the MorseCode dictionary
	for symbol in MorseCode[letter]:
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
 