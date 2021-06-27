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
import threading

class GUI():
    def abrirArchivo(self):
        self.ruta_archivo = tkinter.filedialog.askopenfilename()
        print('Ruta del archivo ', self.ruta_archivo)
        self.imagen = cv.imread(self.ruta_archivo)
        self.ruta_l = self.ruta_archivo.split('/')
        self.tam_l = len(self.ruta_l)
        self.nombre = self.ruta_l[self.tam_l-1]
        cv.imshow(self.nombre, self.imagen)
        cv.waitKey(0)
    
    def traslacion(self, ancho, alto):
        nueva_img = self.imagen
        ancho_img = nueva_img.shape[0] #numero de columnas
        alto_img = nueva_img.shape[1] #numero de filas
        M = np.float32([
            [1,0,ancho],
            [0,1,alto]
        ])
        img_trasladada = cv.warpAffine(nueva_img, M, (alto_img, ancho_img))
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_trasladada.jpg'
        cv.imwrite(nombre, img_trasladada)
        cv.imshow(nombre, img_trasladada)
        cv.waitKey(0)
        
    def rotacion(self, grados, tam):
        nueva_img = self.imagen
        ancho = nueva_img.shape[0]
        alto = nueva_img.shape[1]
        M = cv.getRotationMatrix2D((ancho//2, alto//2), tam, grados)
        img_rotada = cv.warpAffine(nueva_img, M, (alto, ancho))
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_rotada.jpg'
        cv.imwrite(nombre, img_rotada)
        cv.imshow(nombre, img_rotada)
        cv.waitKey(0)
    
    def grises(self):
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_grises.jpg'
        print('Ruta del archivo ', self.ruta_archivo)
        cv.imwrite(nombre, img_grises)
        cv.imshow(nombre, img_grises)
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
        self.img_file = self.img_file.resize((40,40), Image.ANTIALIAS)
        self.img_file = ImageTk.PhotoImage(self.img_file)
        self.btnFile = Button(self.frame1, image=self.img_file, text='Abrir', bg=self.color_base, command=self.abrirArchivo)
        self.btnFile.place(x=35,y=55)
        self.lblAbrir = Label(self.frame1, text='Abrir archivo', font=('Open Sans', 10), fg=self.color_fuente, bg=self.color_base)
        self.lblAbrir.place(x=20,y=115)
        
        self.btnFile = Button(self.frame1, text='Grises', bg=self.color_base, fg=self.color_fuente, command=self.grises)
        self.btnFile.place(x=85,y=55)
        
        ############# Entrys ############
        self.columnas = Entry(self.frame1, width=5)
        self.columnas.place(x=35,y=100)
        
        self.filas = Entry(self.frame1, width=5)
        self.filas.place(x=35,y=70)
        
        ############ Operaciones que necesitan de los entrys ##############
        
        self.btnFile = Button(self.frame1, text='Traslación', bg=self.color_base, fg=self.color_fuente, command= lambda: self.traslacion(int(self.columnas.get()), int(self.filas.get())))
        self.btnFile.place(x=35,y=150)
        
        self.btnFile = Button(self.frame1, text='Rotación', bg=self.color_base, fg=self.color_fuente, command= lambda: self.rotacion(int(self.columnas.get()), int(self.filas.get())))
        self.btnFile.place(x=35,y=180)
        
        
        #############################
        
        self.root.mainloop()

gui = GUI()