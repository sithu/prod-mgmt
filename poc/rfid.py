# `serial` refers to the pyserial library which can be found here: http://pyserial.sourceforge.net/
import serial


BAUD_RATE = 9600
RFID_BYTES = 12
START_CHAR = '\x02'
ser = serial.Serial('/dev/cu.Bluetooth-Incoming-Port', BAUD_RATE)

while True:
    print 'Wating for RFID Tag......'

    # Wait until a tag is read
    rfid = ser.read(RFID_BYTES)
    rfid = str(rfid.strip(START_CHAR))

    # Only act if we think we have a valid tag
    if len(rfid) == (RFID_BYTES - 1):
        print 'Tag Found', rfid

        # Logic to do things with the RFID tag .....

        # Flush the bus
        ser.flushInput()