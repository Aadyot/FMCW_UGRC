import serial
from praser import *
ser = serial.Serial('COM11', 9600)  # Replace 'COM3' with your Arduino's port


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import queue
import threading
import time

def byte4_to_float(bytes_data):
    return struct.unpack('<f', bytes_data)[0]


data_queue = queue.Queue(maxsize=100)
def data_producer():
    while(True):
        line = ser.readline()
        print(line)
        parser = FrameParser(line)
        if(parser.function_code == 4 and parser.address_1 == 3 and parser.address_2 == 6):
            if data_queue.full():
                data_queue.get()  # Remove old data to keep queue size constant
            data_queue.put(byte4_to_float(parser.data))
            print(byte4_to_float(parser.data))
        

# Set up the plot
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-')

def init():
    """Initialize the background of the plot."""
    ln.set_data([], [])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    return ln,

def update(frame):
    """Update the plot with new data."""
    while not data_queue.empty():
        ydata.append(data_queue.get())
        xdata.append(len(ydata))
        
        # Update the plot with new data
        ln.set_data(xdata, ydata) 
        
        ax.set_xlim(0, max(len(ydata), 10))
        ax.set_ylim(min(ydata) - 1, max(ydata) + 1)
        
          
    return ln,

# Start data producer thread
producer_thread = threading.Thread(target=data_producer, daemon=True)
producer_thread.start()

# Create animation
ani = animation.FuncAnimation(fig, update, init_func=init,  interval=100)

plt.show()



