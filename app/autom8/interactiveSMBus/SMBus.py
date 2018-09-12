import xml.etree.ElementTree as ET

class SMBus:
    def __init__(self, port):
        self.port = port

    def read_byte(self, address):
        try:
            e = ET.parse('/home/admin/autom8/cfg/interactiveIO/i2c.xml').getroot()
            return int(e.find('port' + str(self.port)).find('address' + str(address)).text.strip())
        except ET.ParseError:
            return -1