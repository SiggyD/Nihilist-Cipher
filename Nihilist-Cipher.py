#########################
#                       #
#   NIHLIST-CIPHER.PY   #
#                       #
#########################
'''
A python implementation of the nihilist ciper.
Learn about it here! -> https://en.wikipedia.org/wiki/Nihilist_cipher

This program provides functionality of creating a polybius square for a given key.
It also has the ability to encrypt and decrypt nihilist ciphers. The cipher is fairly simple to encrypt, even by hand.
As with most ciphers, (key)size matters, don't expect

TODO:
[] Decrypt branch
[] Add logic branch for -e/-d flags
[] Add flag to toggle verbosity
'''
###############
#             #
#   IMPORTS   #
#             #
###############

import os
import sys
import string

####################
#                  #
#   DECLERATIONS   #
#                  #
####################

# the null matrix /  polybius 
poly = [[0,1,2,3,4,5],
[1,'','','','',''],
[2,'','','','',''],
[3,'','','','',''],
[4,'','','','',''],
[5,'','','','','']]
polybiusCT = ""
polybiusKey = ""
#Display the help text
def sendHalp():
	print "*HELP TEXT*\nNihilist-Cipher.py is a simple python implementation of the classical cipher."
	print "Usage:\n> python Nihilist-Cipher.py <PolybiusKey> <-e|-d> <pathToPlainText/Ciphetext> <AdditiveKey>"
	print "Example: \n> python Nihilist-Cipher.py spookyscary -e ~Nihilist-Cipher/pt.txt \"Cryptographers have trust issues\""
	print "Optionally, this program can also operate in polybius mode, which will create a square for you to admire. This will happen by default of you only provide the first key argument."
	
#Ugly method for displaying the polybius square.
def prettyPrint():
	print "  1 2 3 4 5"
	for i in xrange(1,6):
		lineBuild = str(i)+" "
		for j in xrange(1,6):
			lineBuild = lineBuild + str(poly[i][j])+" " 
		print lineBuild
	print ""

#returns the polybius row-column vector for a specified letter
def decodePoly(queryChar):
	for i in xrange(1,6):
		for j in xrange(1,6):
			if (poly[i][j] == queryChar):
				return str(i)+str(j)

#Turns a given keyword into a key friendly version. It strips repititious characters from a string.
def ToSingleLetterInstance(inStr):
	key = ""
	usedChars = ""
	for i in xrange(len(inStr)):		
		if (inStr[i] not in usedChars): 
			usedChars += inStr[i]
			key += inStr[i]
	return key

#This takes a keyphrase and uses it to fill the previously null polybius square.
def polybiusFill(key):
	#Build the keyAlphabet, a permutation of 25 letters unique to the a subset of polybius keys.
	keyAlphabet = key
	alph = "ABCDEFGHIKLMNOPQRSTUVWXYZ" #The letter 'J' is commonly removed from the square. It is replaced in the ciphertext with 'I'
	for i in xrange(len(alph)):
		if (alph[i] not in keyAlphabet):
			keyAlphabet += alph[i]
	#fillSquare
	count = 0
	for j in xrange(1,6):
		for k in xrange(1,6):
			poly[j][k] = keyAlphabet[((j-1)*5)+(k-1)]

##################
#                #
#   VALIDATION   #
#                #
##################

if ( len(sys.argv) !=  2 and len(sys.argv) !=  5):
	print "Error_0 - Wrong # of args"
	sendHalp()
	exit()
	
if (len(sys.argv) ==  2):
	print "Starting in Polybius mode..."
	
if len(sys.argv) == 5:
	if (sys.argv[2] != "-e") and (sys.argv[2] != "-e" ):
		print "Error_1 - Expected"
		sendHalp()
		exit()
	else:
		print "Starting Nihilist mode..."

############
#          #
#   MAIN   #
#          #
############

#Get the key string
rawkey = sys.argv[1].upper()
print "Using Polybius Key : "+ rawkey 
key = ToSingleLetterInstance(rawkey)
polybiusFill(key)

#Test if argument is a valid file
path = sys.argv[3]
if not (os.path.exists(path)):
	print "ERROR_2 File was not found at "+ path
	exit()

#Grab the additive key and parse for usable chars
RawAdditiveKey = sys.argv[4]
RawAdditiveKey = RawAdditiveKey.upper()
additiveKey = ""
for i in range(len(RawAdditiveKey)):
	if ((ord(RawAdditiveKey[i]) > 64 ) and (ord(RawAdditiveKey[i])  < 91 )):
		additiveKey = additiveKey + RawAdditiveKey[i]
print "Using additive key: " + additiveKey+"\n"
#show the square!
prettyPrint()
# Encrypt 
with open( path, 'r') as myfile:
	fileText = myfile.read().upper()
	processed = ""
	for i in xrange(len(fileText)):
		if ((ord(fileText[i]) > 64 ) and (ord(fileText[i]) < 91 )):
			processed = processed + fileText[i]
			
	#print the proccessed key
	print "PT: " + processed
	#print the additive key
	temp = ""
	for j in xrange(len(processed)):
		temp = temp + additiveKey[j%len(additiveKey)]
	#print "KT: " + temp
	#Print & store the polybius lookup of the plaintext & expandedkey
	for i in xrange(len(processed)):
		polybiusCT = polybiusCT + decodePoly(processed[i])
		polybiusKey = polybiusKey + decodePoly(additiveKey[i%len(additiveKey)])
	#print "PC: " + polybiusCT 
	#print "PK: " + polybiusKey
	#do the thing
	ct = ""
	for i in range(0,(len(polybiusCT)/2)):
		j = i*2
		tempNum =  int(polybiusCT[j:(j+2)]) + int(polybiusKey[j:(j+2)])
		if (tempNum > 100):
			tempNum = tempNum - 100
		if tempNum < 10:
			ct = ct +"0"+ str(tempNum)
		else:	
			ct = ct + str(tempNum)
	print "CT: " + ct
# [] use round addition to add key to pt
# [] show pt & ct
