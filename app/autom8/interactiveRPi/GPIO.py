import xml.etree.ElementTree as ET

class GPIO:
    BCM = 0
    OUT = 0
    IN = 1
    
    mode = BCM
    pins = {}
    
    @classmethod
    def setmode(cls, mode):
        cls.mode = mode
        return 1
        
    @classmethod
    def setup(cls, pin, type):
        root = ET.Element("value")
        root.text = "0"
        tree = ET.ElementTree(root)
        try:
        	tree.write("/home/pi/autom8/cfg/interactiveIO/GPIO/pin" + str(pin) + ".xml")
        	cls.pins[pin] = type
        	return 1
        except ET.ParseError:
        	print("GPIO Error: setup failed for " + str(pin))
        	return 0
        
    @classmethod
    def output(cls, pin, value):
        if pin in cls.pins and cls.pins[pin] == cls.OUT:
            root = ET.Element("value")
            root.text = "1" if value else "0"
            tree = ET.ElementTree(root)
            try:
            	tree.write("/home/pi/autom8/cfg/interactiveIO/GPIO/pin" + str(pin) + ".xml")
            	return 1
            except ET.ParseError:
            	print("GPIO Error: output failed for " + str(pin))
            	return 0
        else:
            raise Exception("Pin isn't setup for output!")
            return 0
    
    @classmethod
    def cleanup(cls):
        # TODO: remove xml pin files
        cls.pins = {}
        return 1
