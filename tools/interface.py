import serial
import numpy as np
import serial.tools.list_ports


def open_serial_port(port=None, baudrate=None):
    """
    Open serial port and return the serial port object. If no port is specified, the function will try to find the
    serial port of the microcontroller. If no baudrate is specified, the default baudrate of 115200 is used.
    :param port: serial port to open default is None
    :param baudrate: baudrate of the serial port default is None
    :return: serial port object
    """
    if port is None:
        for ports, descs, hwids in sorted(serial.tools.list_ports.comports()):
            if 'FT232R' in descs:
                port = ports
    if baudrate is None:
        baudrate = 115200
    ser = serial.Serial(port, baudrate, timeout=1)
    return ser


def read_serial_port(ser):
    """
    Read serial port and return the difference in timestamps of the two neigbouring signals in microseconds.
    The differences are returned as a numpy array of 16 integers in microseconds.
    :param ser: serial port object to read from
    :return: numpy array of 16 integers with the timestamps in microseconds of the rising edges of the signal
    """
    deltat = np.array([])
    read = False
    while not read:
        signal = ser.read(100)
        signal += ser.read(ser.inWaiting())
        timestamps = np.array(signal.decode("ascii").split("\r")[:-1])
        if timestamps.shape[0] <= 16:
            timestamps = timestamps.astype(int)
            deltat = timestamps[1::2]-timestamps[0::2]
            read = True
    return deltat

if __name__ == '__main__':
    pass