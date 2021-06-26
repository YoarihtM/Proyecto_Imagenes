from tkinter import *
import tkinter.filedialog
from PIL import Image,ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from tkinter import messagebox
import cv2 as cv

class GUI():
    def abrirArchivo(self):
        self.ruta_archivo = tkinter.filedialog.askopenfilename()
        # print('Ruta del archivo ', self.ruta_archivo)
        self.imagen = cv.imread(self.ruta_archivo)
        cv.imshow('Imagen seleccionada', self.imagen)
        cv.waitKey(0)
        
    
        
    def __init__(self):
        self.color_base = '#24264F'
        self.color_fuente = '#FFFFFF'
        self.root = Tk()
        # self.root.iconbitmap('/Users/yoarihtmacedo/Desktop/Senales/Practica2TCS/img_interfaz/señales.ico')
        self.root.title('Practica 2 - Teoría de Comunicaciones y Señales')
        self.root.geometry('500x400')
        self.root.resizable(0,0)
        self.root.config()
        
        ########### FRAME ###########
        
        self.frame1 = Frame(bd=10, width='500', height='400', bg=self.color_base)
        self.frame1.pack()
        self.lblTitulo = Label(self.frame1, text='Proyecto Final', font=('Open Sans', 20), fg=self.color_fuente, bg=self.color_base)
        self.lblTitulo.place(x=150, y=0)
        
        self.img_file = Image.open('./file_n_folder/png/007-folder-8.png')
        self.img_file = self.img_file.resize((50,50), Image.ANTIALIAS)
        self.img_file = ImageTk.PhotoImage(self.img_file)
        self.btnFile = Button(self.frame1, image=self.img_file, text='Abrir', bg=self.color_base, command=self.abrirArchivo)
        self.btnFile.place(x=35,y=55)
        self.lblAbrir = Label(self.frame1, text='Abrir archivo', font=('Open Sans', 10), fg=self.color_fuente, bg=self.color_base)
        self.lblAbrir.place(x=20,y=115)
        
        #############################
        
        self.root.mainloop()

gui = GUI()