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

################################################################################
#                                                                              #
# Import packages                                                              #
#                                                                              #
################################################################################    
import sys, traceback, os, errno, random, time, datetime, argparse, pygame, xml.etree.ElementTree as ET

################################################################################
#                                                                              #
# Logging Helper function                                                      #
#                                                                              #
################################################################################    
def log(message):
    print message
    
    with open(logFile, 'a') as f:
        f.write(datetime.datetime.now().strftime("%H:%M:%S - "))
        f.write(str(message))
        f.write("\n")
    
################################################################################
#                                                                              #
# Initial set up                                                               #
#                                                                              #
################################################################################
now = datetime.datetime.now()
logFile = "/home/pi/autom8/logs/" + now.strftime("%Y%m%d") + "/" + now.strftime("%H%M%S") + ".log"
if not os.path.exists(os.path.dirname(logFile)):
    try:
        os.makedirs(os.path.dirname(logFile))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
            
argparser = argparse.ArgumentParser(description='autom8 Anything')
argparser.add_argument('--interactive', 
                        dest='interactive', 
                        action='store_const', 
                        const=True, 
                        default=False, 
                        help='Use interactive I/O instead of GPIO and I2C (default: GPIO and I2C)')

args = argparser.parse_args()
if args.interactive:
    log("Running in interactive mode...")
    import interactiveSMBus as smbus, interactiveRPi.GPIO as GPIO
else:
    log("Running in normal mode...")
    import smbus, RPi.GPIO as GPIO
    
i2cBus = smbus.SMBus(1)
i2cRecieverAddress = 0
    
################################################################################
#                                                                              #
# play an audio track                                                          #
#                                                                              #
################################################################################
def playTrack(trackName):
    log(trackName)

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(100)

    path = os.path.join("/home/pi/autom8/media/audio", trackName)
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    
################################################################################
#                                                                              #
# Read RF signal from i2c                                                      #
#                                                                              #
################################################################################        
def readRFSignal():
    retry = 0
    while retry < 5:
        try:
            RFSignal = i2cBus.read_byte(i2cRecieverAddress)
            return RFSignal
        except:
            retry+=1
    return -1

################################################################################
#                                                                              #
# Main run loop                                                                #
#                                                                              #
################################################################################
def run():
    log("Starting Main Loop")
    
    while(1):
        tree = ET.parse('/home/pi/autom8/cfg/app.xml')
        app = tree.getroot()
        if app.find('stop').text == '1':
            log('App Stop!')
            break

################################################################################
#                                                                              #
# Script Body                                                                  #
#                                                                              #
################################################################################
try:
    tree = ET.parse('/home/pi/autom8/cfg/app.xml')
    app = tree.getroot()
    app.find('stop').text = '0'
    tree.write('/home/pi/autom8/cfg/app.xml')
    
    GPIO.setmode(GPIO.BCM)
    
    # pygame.mixer.pre_init(44100, -16, 2, 64000)
    pygame.mixer.init()
    pygame.init()
    
    run()
    
    GPIO.cleanup()
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
except:
    traceback.print_exc()
    GPIO.cleanup()
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()