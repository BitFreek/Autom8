################################################################################
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
################################################################################

import sys

################################################################################
#                                                                              #
# Check python version for proper support                                      #
#                                                                              #
################################################################################
# if sys.version_info < (3,2):
#     sys.exit('Sorry, Python < 3.2 is not supported')

################################################################################
#                                                                              #
# Import packages and parse arguments                                          #
#                                                                              #
################################################################################
import traceback, time, xml.etree.ElementTree as ET

try:
    print "\nctrl+c to exit\n"
    
    while True:
        print "\r",
        
        try:
            pin20 = ET.parse('/home/pi/autom8/cfg/interactiveIO/GPIO/pin20.xml').getroot().text.strip()
        except ET.ParseError:
            pin20 = 0
        
        try:
            pin24 = ET.parse('/home/pi/autom8/cfg/interactiveIO/GPIO/pin24.xml').getroot().text.strip()
        except ET.ParseError:
            pin24 = 0
        
        try:
            pin25 = ET.parse('/home/pi/autom8/cfg/interactiveIO/GPIO/pin25.xml').getroot().text.strip()
        except ET.ParseError:
            pin25 = 0
        
        print "          Pin 20: " + str(pin20) + " Pin 24: " + str(pin24) + " Pin 25: " + str(pin25),
        time.sleep(0.1)
except:
    print "\n\n"
    traceback.print_exc()