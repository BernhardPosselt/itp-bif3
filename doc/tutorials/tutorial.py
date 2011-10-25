#!/usr/bin/python

# imports
from os import path_exists
import os
from os.path import abspath as apath

# variablen
a = 5
b = "hi"
c = r"[a-z]*"

# listen
liste = ["hi", "du"]
print liste[0]

# tupel
tupel = ("hi",)
print tupel[0]

# dicts
dictionary = { "schluessel": "hi", "nummer": 5 }
print dictionary["nummer"]



# if
if a == 5:
    pass
elif a == 6:
    pass

if a:
    pass


# for schleifen
for i in xrange(5):
    print i

for item in liste:
    print liste

for key, value in dictionary.iteritems():
    print key
    print value


# try catch
try:
    liste[2]
except IndexError:
    print "error"
finally:
    print "exiting"



# functionen
def my_func(argument1, argument2=3):
    pass

my_func("hi")
my_func("hi", 4)


# klassen
class MyObject(object):
    
    def __init__(self, param1):
        self.param = param1
        
    
    def sayHi(self):
        print "hi"
    
    
obj = MyObject("param")
obj.sayHi()

