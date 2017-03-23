# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import sys

#TODO append path.
#sys.path.append('/usr/local/lib/python2.7/site-packages')
import re
import numpy as np
import matplotlib.pyplot as plt
import serial

#TODO set serial port, baud rate. e.g. mac:'/dev/tty.usbserial-DJ00M1QE' win:'COM3'
ser = serial.Serial('/dev/tty.usbserial-DJ00M1QE', 115200)

class GraphManager:
    """Graph Manager class"""
    
    #dx:delta Time.
    dx = 0.5

    def __init__(self, n):
        self.n = n
        self.gain = 1.0
        self.axis = ""
        self.lines = [""]*n
        self.x = np.arange(0, 10, GraphManager.dx)
        self.ys = np.zeros([n, len(self.x)])

    def setup(self, title, labels, ymin, ymax, gain):
        for num in range(len(self.lines)):
            self.lines[num], = self.axis.plot(self.x, self.ys[0],label=labels[num])
        self.axis.legend(loc=2, fontsize=9)
        self.axis.set_ylim((ymin, ymax))
        self.axis.set_title(title)
        self.gain = gain

    def update(self, ys):
        if len(ys) != self.n:
            return
        self.x += GraphManager.dx
        ya = np.array(ys)
        ya = ya.astype(np.int)

        self.ys = np.hstack((self.ys, np.transpose([self.gain*ya])))
        self.ys = np.hsplit(self.ys,[1])
        self.ys = self.ys[1]

        self.axis.set_xlim((self.x.min(), self.x.max()))
        for num in range(len(self.lines)):
            self.lines[num].set_data(self.x, self.ys[num])

def pause_plot():
    #init garaph
    ge_acc = GraphManager(3)
    ge_gyr = GraphManager(3)
    ge_mag = GraphManager(3)
    ge_temp = GraphManager(1)

    fig, ([ge_acc.axis, ge_gyr.axis], [ge_mag.axis, ge_temp.axis])= plt.subplots(nrows=2,ncols=2, figsize=(12,8))
    
    ge_acc.setup("加速度 (g)", ["x", "y", "z"], -2, 2, 0.001)
    ge_gyr.setup("ジャイロ (°/sec)", ["x", "y", "z"], -250, 250, 0.001*250)
    ge_mag.setup("磁気 (uT)", ["x", "y", "z"], -100, 100, 1.0)
    ge_temp.setup("温度 (℃)", ["t"], 0, 50, 0.1)

    while True:
        #read serial
        line = ser.readline()
        
        if re.search(r"ACC:", line):
            accs = re.findall(r"\d{1,}", line)
            ge_acc.update(accs)
#            print ("ACC:%s" % accs)
            continue
        if re.search(r"GYR:", line):
            grys = re.findall(r"\d{1,}", line)
            ge_gyr.update(grys)
#            print ("GYR:%s" % grys)
            continue
        if re.search(r"MAG:", line):
            mags = re.findall(r"\d{1,}", line)
            ge_mag.update(mags)
#            print ("MAG:%s" % mags)
            continue
        if re.search(r"T:", line):
            temps = re.findall(r"\d{1,}", line)
            ge_temp.update(temps)
#            print ("T:%s" % temps)

            #replot
            plt.ion()
            plt.pause(0.0001)

if __name__ == "__main__":
    print ("----START MPU9250----")
    pause_plot()
    ser.close()
    print ("----END MPU9250----")
