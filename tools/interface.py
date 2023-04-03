import serial
import numpy as np
import serial.tools.list_ports
import os
import multiprocessing
import time


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
    timestamps = np.empty(21)
    run = True
    while run:
        signal = ser.read(1)
        signal += ser.read(ser.inWaiting())
        timestamps_old = timestamps.copy()
        timestamps = np.array(signal.decode("ascii").replace(" ", "").strip("\n").strip("'").split("\r"))
        numbers = np.char.array(timestamps).isdigit()
        timestamps = timestamps[numbers].astype(int)
        if (timestamps.shape[0] + timestamps_old.shape[0]) == 16:
            timestamps = np.concatenate((timestamps_old, timestamps))
            run = False
        elif timestamps.shape[0] % 2 == 0:
            run = False
    return (timestamps[1::2]-timestamps[0::2])*12.5/1000


def data_to_csv(data, filename):
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


def port_to_csv(filename):
    """
    Write the data from the serial port to a csv file. The data is written in a column format.
    :param ser: serial port object to read from
    :param filename: filename of the csv file
    :param samples: number of samples to read from the serial port
    :return: None
    """

    def count(ser, shared_list):
        while True:
            data = read_serial_port(ser)
            shared_list += data.tolist()

    def write(shared_list):
        event_counter = 0
        mion_counter = 0
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                pass

        with open(filename, 'a') as f:
            while True:
                time.sleep(1)
                for i in shared_list:
                    event_counter += 1
                    if (i < 10) and (i > 0):
                        mion_counter += 1
                    f.write(str(i) + '\n')
                print("\r counts:"+str(event_counter*2)+" mion:"+str(mion_counter), end="")
                shared_list[:] = []

    manager = multiprocessing.Manager()
    shared_list = manager.list()
    serial = open_serial_port()
    print("Serial port opened")
    p1 = multiprocessing.Process(name="Read serial", target=count, args=[serial, shared_list])
    p2 = multiprocessing.Process(name="Write to csv", target=write, args=[shared_list])
    print("Processes started")
    print()
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == '__main__':
    port_to_csv("../test_data.csv")