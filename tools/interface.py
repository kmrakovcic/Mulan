import serial
import numpy as np
import serial.tools.list_ports
import os


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
    timestamps = np.char.array(["A", "b"])
    while not (np.char.array(timestamps).isdigit().all() and timestamps.shape[0] == 16):
        signal = ser.read(1)
        signal += ser.read(ser.inWaiting())
        timestamps = np.array(signal.decode("ascii").split("\r")[:-1])
    timestamps = timestamps.astype(int)
    return (timestamps[1::2]-timestamps[0::2])*12.5/1000

def write_port_data_to_csv(data, filename):
    """
    Write the data from the serial port to a csv file. The data is written in a column format.
    :param ser: serial port object to read from
    :param filename: filename of the csv file
    :return: None
    """
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass
    with open(filename, 'a') as f:
        for i in data:
            f.write(str(i) + '\n')


if __name__ == '__main__':
    import sys
    serial = open_serial_port()
    while True:
        data = read_serial_port(serial)