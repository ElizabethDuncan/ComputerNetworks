"""

Computer Networks Fall 2013
Elizabeth Duncan

routerRefactor.py is based on router.py except that the code has been restructured to include
python with statement and other structures

This script flashes a LED with a Morse message (if message is provided). Afterwards, it waits to
receive a message through the photodiode. Any message received will be translated into Morse code.

If at any time the program exits, the LED will be turned off and GPIO will be cleaned up.

"""


import RPi.GPIO as GPIO, time, os
import time
import sys

class Run(object):
	def __init__ (self, LED_pin = None, DIODE_pin = None, message = "1 HI ="):

		with MorseMessage(LED_pin = 25, DIODE_pin = 18) as fd:
			
			#If router starts with a message, send that
			#if message:
			#	fd.write(message)
			#Read any incomming message
			fd.read()
			
"""
			if self.message: 
				fd.write(message)
			for message in fd.read: fd.write(message)
"""
			
class MorseMessage(object):
	
	def __init__ (self, LED_pin = None, DIODE_pin = None):
		

		#Pin values
		self.LED_pin = 25
		self.DIODE_pin = 18
		
		#Miscellaneous variables
		self.value = 0
		self.oncounter = 0
		self.offcounter = 0
		self.currentLetter = []
		self.phrase = ""
		self.message = []
		self.begin = 0
		self.timeunit = 1
		
		#Dictionary from letters to Morse Code 
		self.MorseCodeLetters = {' ': 'X',
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
		
		#Dictionary of Morse Code 
		self.MorseCode = {'-----' : '0',
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
		
	def __enter__(self):
        #initialize GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.LED_pin, GPIO.OUT)
		return self
	
	def __exit__(self, xclass, xclasstr, xstacktrace):
		#reset GPIO
		print("Router script terminated.")
		GPIO.output(25, False)
		GPIO.cleanup()
		#GPIO.output(self.LED_pin, False)


	#Get value from photodiode
	def RCtime(self, RCpin):
	    reading = 0
	    GPIO.setup(RCpin, GPIO.OUT)
	    GPIO.output(RCpin, GPIO.LOW)
	    time.sleep(0.1)

	    GPIO.setup(RCpin, GPIO.IN)
	    while(GPIO.input(RCpin) == GPIO.LOW):
	        reading +=1

	    return reading

	#Function that flashes the LED in convention with Morse Code's dot
	def dot(self, LED_PIN):
		print("dot");
                GPIO.output(LED_PIN, True)
                time.sleep(1*self.timeunit)
		GPIO.output(LED_PIN, False)
		time.sleep(1*self.timeunit)

	#Function that flashes the LED in convention with Morse Code's dash
	def dash(self, LED_PIN):
                print("dash");
		GPIO.output(LED_PIN, True)
		time.sleep(3*self.timeunit)
		GPIO.output(LED_PIN, False)
		time.sleep(1*self.timeunit)
	
	#read the Morse message with the photodiode	
	def read(self):
                #make sure that LED is off for reading mode
                GPIO.output(25, False)
                print("READING MODE")
                while True:
                    value = self.RCtime(self.DIODE_pin)
                    #print(value)

                    #If value returned from RCtime is greater than 200, LED is OFF
                    if value > 100:
                        #If oncounter is greater than zero, the LED was JUST turned off
                        if self.oncounter > 0:
	            
                            if 7 <= self.oncounter <= 11:
                                print("Dot");
                                self.currentLetter.append('.')
	                
                            if  21 <= self.oncounter <= 33:
                                print("Dash");
                                self.currentLetter.append('-')
	                
                        self.oncounter = 0
                        self.offcounter = self.offcounter + 1

                        #If there is a long pause, then the message has ended

                        if self.offcounter > 100 and self.begin != 0:
                            self.key = ''.join(self.currentLetter)
                            if self.MorseCode[self.key] == 'SK' :
                                if self.phrase[0] == '1':
                                    self.phrase = self.phrase + "SK"
                                    print("message received!")
                                    print(self.phrase)
                                    exit()
                                else:
                                    self.phrase = self.phrase + "="
                                    print("repeating the message...")
                                    #repeat()
                                    write(self, self.phrase)                                   
                                    exit()
	            #If value returned from RCtime is less than 100, LED is ON
                    else:  
                        #Begin keeps track of how many times this has been called
	                self.begin = self.begin + 1
	        
                        #If oncounter is greater than zero, the LED was JUST turned ON
	                if self.offcounter > 0:
	                    #print(self.offcounter)
	                    if 1 <= self.offcounter <= 15:
                                #The space between parts of the same letter (1 unit)
	                        pass
	            
	                    if  16 <= self.offcounter <= 40 and self.begin != 1:
	                        #The space between letter (3 units)

                                self.key = ''.join(self.currentLetter)
                                #Print the letter that corresponds to the Morse Code signal
	                        print(self.MorseCode[self.key])
	                        self.phrase = self.phrase + self.MorseCode[self.key]
	                        self.currentLetter[:] = []
	                
	                    if 40 <= self.offcounter <= 120 and self.begin != 1:
                                #The space between words (7 units)
	                        self.key = ''.join(self.currentLetter)
	                        #print(self.key)
	                        print(self.MorseCode[self.key])
	                        #print("printed letter")
	                        self.phrase = self.phrase + self.MorseCode[self.key]
	                        print(" ")
	                        self.phrase = self.phrase + " "
	                        self.currentLetter[:] = []
	            
	                self.offcounter = 0
	                self.oncounter = self.oncounter + 1
	
	#write the Morse message with the LED	
	def write(self, message):
	    #input = phrase
	    print(message);

	    #iterate through ever letter of the input
            for letter in message:
                print(letter)
	
	        #look up each letter in the MorseCode dictionary
                for symbol in self.MorseCodeLetters[letter]:
		    if symbol == '-':
			self.dash(self.LED_pin)
		    elif symbol == '.':
			self.dot(self.LED_pin)
		    #if the symbol is an X (which corresponds to a space between words), wait for 7 units
		    elif symbol == 'X':
                        #sleep for 4 addtional time units (since it will also sleep 3 at the end of the letter)
                        #Total sleep (7 units) for new word
			time.sleep(4*self.timeunit)
                    else:
			print("Error with MorseCode dictionary!")

                    #sleep at the end of a letter          
            time.sleep(3*self.timeunit)
            return 0


if __name__ == "__main__":
	r = Run()

		
