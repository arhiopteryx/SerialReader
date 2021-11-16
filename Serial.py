import shelve
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import reduce
from typing import Match
import math
from tkinter.filedialog import askopenfilename
from tkinter import *
import serial
from pylab import *
from serial.tools import list_ports
from threading import Thread


class Main(tk.Frame):

    def __init__(self, root):

        self.arrPorts = []
        self.speeds = [300, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200, 230400, 250000, 500000, 1000000, 2000000]
        self.fileName = tk.StringVar()
        self.textFromPort = tk.StringVar()
        self.textFromPort.set("Serial: ")

        self.isOpenPort = False
        

        super().__init__(root)
        root.title("Serial")
        root.geometry("300x300")
        root.resizable(False, False)
        self.init_main()

    def changePort(self) :
        self.arrPorts = []
        for port in list_ports.comports():
            self.arrPorts.append(port.device)
        self.comboPort["values"] = self.arrPorts


    def ThreadSerial(self):
        if self.isOpenPort == False:
            self.isOpenPort = True
            self.btnReadPort.configure(text="Stop reading")
            Thread(target=self.readSerial, daemon=True).start()  
        else:
            self.btnReadPort.configure(text="Read from port to file")
            self.isOpenPort = False

   
    
    
    def readSerial(self):
        try:
            speed = self.comboSpeed.get()
            port = self.comboPort.get()
            fileName = self.entryFileName.get()

            if speed == "" or port == "" or fileName == "":
                messagebox.showerror('Error', 'Empty field')
                return
            
            ser = serial.Serial(port, timeout=None, baudrate=int(speed))
            file = open(fileName+".txt",'w')
            self.textFromPort.set("Serial: ...")

            while(True):
                if self.isOpenPort == False:
                    self.textFromPort.set("Serial: ")
                    break
                textFromSerial = str(ser.readline())
                textFromSerial = textFromSerial.replace("b'", "")
                textFromSerial = textFromSerial.replace("\\r\\n'", "")
                self.textFromPort.set("Serial: " + textFromSerial)
                file.write(textFromSerial + '\n')            
            file.close()         
            
        except :
            messagebox.showerror('Error', 'Do not open port') 
            file.close()
            

    def init_main(self):

        self.labelSpeed = tk.Label(root, text='Speed', fg='black', font="Verdana 12", width=10)
        self.labelSpeed.pack(padx=5, pady=5, side=TOP)
        
        self.comboSpeed = ttk.Combobox(root, values=self.speeds, font = ("Verdana" , 12), state="readonly")
        self.comboSpeed.pack(padx=5, pady=5, side=TOP)
        self.comboSpeed.current(4)

        self.labelPort = tk.Label(root, text='Port', fg='black', font="Verdana 12", width=10)
        self.labelPort.pack(padx=5, pady=5, side=TOP)
        
        self.comboPort = ttk.Combobox(root, values=self.arrPorts, font = ("Verdana" , 12), state="readonly", postcommand=self.changePort)
        self.comboPort.pack(padx=5, pady=5, side=TOP)

        
        self.labelFileName = tk.Label(root, text='File Name', fg='black', font="Verdana 12", width=10)
        self.labelFileName.pack(padx=5, pady=5, side=TOP)
        self.entryFileName = ttk.Entry(root, width=22, textvariable=self.fileName, font="Verdana 12")
        self.entryFileName.pack(padx=5, pady=5)        
        self.entryFileName.insert(0, "fileName")

        
        self.btnReadPort = tk.Button(root, text='Read from port to file', command=self.ThreadSerial, background="#555", foreground="#ccc", font="15")
        self.btnReadPort.pack(padx=10, pady=10)

        self.labelSerialData = tk.Label(root, textvariable=self.textFromPort, fg='black', width=30)
        self.labelSerialData.pack(padx=5, pady=5, side=TOP)

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.mainloop()



