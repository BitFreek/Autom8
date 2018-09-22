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
import traceback, os, errno, random, time, datetime, argparse, pygame, xml.etree.ElementTree as ET

argparser = argparse.ArgumentParser(description='autom8 Anything')
argparser.add_argument('--interactive', 
                        dest='interactive', 
                        action='store_const', 
                        const=True, 
                        default=False, 
                        help='Use interactive I/O instead of GPIO and I2C (default: GPIO and I2C)')

args = argparser.parse_args()
if args.interactive:
    print "Running in interactive mode..."
    import interactiveSMBus as smbus, interactiveRPi.GPIO as GPIO
else:
    print "Running in normal mode..."
    import smbus, RPi.GPIO as GPIO

################################################################################
#                                                                              #
# Initial set up                                                               #
#                                                                              #
################################################################################
i2cBus = smbus.SMBus(1)
i2cRecieverAddress = 0

now = datetime.datetime.now()
logFile = "/home/pi/autom8/logs/" + now.strftime("%Y%m%d") + "/" + now.strftime("%H%M%S") + ".log"
if not os.path.exists(os.path.dirname(logFile)):
    try:
        os.makedirs(os.path.dirname(logFile))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

numScenes = 14
ambientTrack = "Ambient.mp3"
sceneAudioChannels = [
    {'scene': 'A', 'channel': 1,  'track': "01.mp3"},
    {'scene': 'B', 'channel': 2,  'track': "02.mp3"},
    {'scene': 'C', 'channel': 3,  'track': "03.mp3"},
    {'scene': 'D', 'channel': 4,  'track': "04.mp3"},
    {'scene': 'E', 'channel': 5,  'track': "05.mp3"},
    {'scene': 'F', 'channel': 6,  'track': "06.mp3"},
    {'scene': 'G', 'channel': 7,  'track': "07.mp3"},
    {'scene': 'H', 'channel': 8,  'track': "08.mp3"},
    {'scene': 'I', 'channel': 9,  'track': "09.mp3"},
    {'scene': 'J', 'channel': 10, 'track': "10.mp3"},
    {'scene': 'K', 'channel': 11, 'track': "11.mp3"},
    {'scene': 'L', 'channel': 12, 'track': "12.mp3"},
    {'scene': 'M', 'channel': 13, 'track': "13.mp3"},
    {'scene': 'N', 'channel': 14, 'track': "14.mp3"}
]

alreadyPlayed = []

################################################################################
#                                                                              #
# Main run loop                                                                #
#                                                                              #
################################################################################
def run():
    print "Starting Main Loop"
    global numScenes, ambientTrack, sceneAudioChannels, alreadyPlayed

    tree = ET.parse('/home/pi/autom8/cfg/app.xml')
    app = tree.getroot()
    app.find('stop').text = '0'
    tree.write('/home/pi/autom8/cfg/app.xml')

    while(1):
        tree = ET.parse('/home/pi/autom8/cfg/app.xml')
        app = tree.getroot()
        if app.find('stop').text == '1':
            log('App Stop!')
            break

        sceneID = readSceneID()

        # Check for reset
        if len(alreadyPlayed) > 0 and sceneID == 0:
            log('RESET')
            pygame.mixer.music.fadeout(1000)
            alreadyPlayed = []
            GPIO.output(20, True)
        
        # Check for scene trigger
        for index, member in enumerate(sceneAudioChannels):
            if sceneID == member['channel'] and not member['scene'] in alreadyPlayed:
                log(member['scene'])
                alreadyPlayed.append(member['scene'])
                playTrack(member['track'])
                GPIO.output(24, False)
                GPIO.output(25, False)
                GPIO.output(20, False)
                time.sleep(1)
                break
        
        # If not doing anything else play ambient
        if not pygame.mixer.music.get_busy():
            playTrack(ambientTrack)

        # check for comunication error
        if sceneID == -1:
            GPIO.output(24, False)
            for x in range(5):
                GPIO.output(25, True)
                time.sleep(0.25)
                GPIO.output(25, False)
                time.sleep(0.25)
            
        # Update status LED
        if len(alreadyPlayed) == numScenes:
            GPIO.output(24, True)
            GPIO.output(25, False)
        elif len(alreadyPlayed) == 0:
            GPIO.output(24, False)
            GPIO.output(25, True)
        else:
            GPIO.output(24, True)
            GPIO.output(25, True)

################################################################################
#                                                                              #
# play an audio track                                                          #
#                                                                              #
################################################################################
def playTrack(trackName):
    log(trackName)

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(1000)

    path = os.path.join("/home/pi/autom8/media/audio", trackName)
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

################################################################################
#                                                                              #
# Read scene ID from i2c                                                       #
#                                                                              #
################################################################################        
def readSceneID():
    retry = 0
    while retry < 5:
        try:
    	    sceneID = i2cBus.read_byte(i2cRecieverAddress)
            return sceneID
        except:
            retry+=1
    return -1

################################################################################
#                                                                              #
# Logging Helper function                                                      #
#                                                                              #
################################################################################    
def log(message):
    with open(logFile, 'a') as f:
        f.write(datetime.datetime.now().strftime("%H:%M:%S - "))
        f.write(str(message))
        f.write("\n")

################################################################################
#                                                                              #
# Script Body                                                                  #
#                                                                              #
################################################################################
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)  # Relay 0
    GPIO.setup(24, GPIO.OUT)  # Status LED Green
    GPIO.setup(25, GPIO.OUT)  # Status LED Red

    GPIO.output(24, False)
    GPIO.output(25, True)

    GPIO.output(20, True)

    pygame.mixer.pre_init(44100, -16, 2, 64000)
    pygame.mixer.init()
    pygame.init()
    
    run()
    GPIO.cleanup()
    pygame.mixer.music.stop()
except:
    traceback.print_exc()
    GPIO.cleanup()
    pygame.mixer.music.stop()
