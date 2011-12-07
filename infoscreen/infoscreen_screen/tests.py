"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
from lxml import etree
from infoscreen.infoscreen_screen.parser import *


    

class Testparser(unittest.TestCase):
    def test_tags(self):
        """
        Einlesen mit Parser
        """
       
        x = 2+2
        self.assertEqual(x,4)
        
        """ 
      
        for element in xml_element:
            print element.tag
       
        self.assertEqual(x,"B3")
        """
        """
        root = etree.parse("tests/xml/dummy.xml")
        context = etree.iterwalk(root)
        for elem in context:"""
