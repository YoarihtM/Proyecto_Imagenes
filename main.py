from tkinter import *
import tkinter.filedialog
from PIL import Image,ImageTk
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from tkinter import messagebox
import cv2 as cv
import threading
import imutils
import matplotlib as plt

class GUI():
    def abrirArchivo(self):
        self.ruta_archivo = tkinter.filedialog.askopenfilename()
        print('Ruta del archivo ', self.ruta_archivo)
        self.imagen = cv.imread(self.ruta_archivo)
        datos = 'Columnas = ' + str(self.imagen.shape[1]) + ' Filas = ' + str(self.imagen.shape[0])
        self.lblImgInfo.config(text=datos)
        self.frame1.update()
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
    
    def escalado(self, escala):
        nueva_img = self.imagen
        img_escalada = imutils.resize(nueva_img, width=escala)
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_escalada.jpg'
        cv.imwrite(nombre, img_escalada)
        cv.imshow(nombre, img_escalada)
        cv.waitKey(0)
    
    def recortar(self, col_i, col_f, fila_i, fila_f):
        nueva_img = self.imagen
        img_recortada = nueva_img[col_i:col_f, fila_i:fila_f]
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_recortada.jpg'
        cv.imwrite(nombre, img_recortada)
        cv.imshow(nombre, img_recortada)
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
        
    def canales(self):
        nueva_img = self.imagen
        # img_b, img_g, img_r = cv.
        
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
        self.btnFile.place(x=40,y=55)
        
        self.lblImgInfo = Label(self.frame1, text='', bg=self.color_base, fg=self.color_fuente)
        self.lblImgInfo.place(x=120,y=65)
        
        ############# Operaciones que no usan entrys #############
        
        self.btnFile = Button(self.frame1, text='Grises', bg=self.color_base, fg=self.color_fuente, command=self.grises)
        self.btnFile.place(x=200,y=120)
        
        
        
        ############# Entrys ############
        
        self.columnas = Entry(self.frame1, width=5)
        self.columnas.place(x=390,y=120)
        
        self.filas = Entry(self.frame1, width=5)
        self.filas.place(x=390,y=150)
        
        self.columnas1 = Entry(self.frame1, width=5)
        self.columnas1.place(x=390,y=180)
        
        self.filas1 = Entry(self.frame1, width=5)
        self.filas1.place(x=390,y=210)
        
        ############ Operaciones que necesitan de los entrys ##############
        
        self.btnFile = Button(self.frame1, text='Traslación', bg=self.color_base, fg=self.color_fuente, command= lambda: self.traslacion(int(self.columnas.get()), int(self.filas.get())))
        self.btnFile.place(x=35,y=120)
        
        self.btnFile = Button(self.frame1, text='Rotación', bg=self.color_base, fg=self.color_fuente, command= lambda: self.rotacion(int(self.columnas.get()), int(self.filas.get())))
        self.btnFile.place(x=35,y=160)
        
        self.btnFile = Button(self.frame1, text='Escalar', bg=self.color_base, fg=self.color_fuente, command= lambda: self.escalado(int(self.columnas.get())))
        self.btnFile.place(x=35,y=200)
        
        self.btnFile = Button(self.frame1, text='Recortar', bg=self.color_base, fg=self.color_fuente, command= lambda: self.recortar(int(self.columnas.get()), int(self.columnas1.get()), int(self.filas.get()), int(self.filas1.get())))
        self.btnFile.place(x=35,y=240)
        
        #############################
        
        self.root.mainloop()

gui = GUI()