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
        cv.destroyAllWindows()
    
    def traslacion(self, ancho, alto):
        nueva_img = self.imagen
        ancho_img = nueva_img.shape[0] 
        alto_img = nueva_img.shape[1] 
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
        cv.destroyAllWindows()
        
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
        cv.destroyAllWindows()
    
    def escalado(self, escala):
        nueva_img = self.imagen
        img_escalada = imutils.resize(nueva_img, width=escala)
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_escalada.jpg'
        cv.imwrite(nombre, img_escalada)
        cv.imshow(nombre, img_escalada)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def recortar(self, col_i, col_f, fila_i, fila_f):
        nueva_img = self.imagen
        img_recortada = nueva_img[col_i:col_f, fila_i:fila_f]
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_recortada.jpg'
        cv.imwrite(nombre, img_recortada)
        cv.imshow(nombre, img_recortada)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def grises(self):
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_grises.jpg'
        print('Ruta del archivo ', self.ruta_archivo)
        cv.imwrite(nombre, img_grises)
        cv.imshow(nombre, img_grises)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    def canales(self):
        print('Ruta del archivo ', self.ruta_archivo)
        nueva_img = self.imagen
        alto = nueva_img.shape[0]
        ancho = nueva_img.shape[1]
        
        img_b = nueva_img[:, :, 0]
        img_g = nueva_img[:, :, 1]
        img_r = nueva_img[:, :, 2]

        nombre_l = self.nombre.split('.')
        
        nombre = nombre_l[0] + '_BGR'
        nombre_b = nombre_l[0] + '_B.jpg'
        nombre_g = nombre_l[0] + '_G.jpg'
        nombre_r = nombre_l[0] + '_R.jpg'
        
        nombre_b1 = nombre_l[0] + '_b.jpg'
        nombre_g1 = nombre_l[0] + '_g.jpg'
        nombre_r1 = nombre_l[0] + '_r.jpg'
        
        zeroImgMatrix = np.zeros((alto, ancho), dtype="uint8")
        
        (b,g,r) = cv.split(nueva_img)
        b = cv.merge([b, zeroImgMatrix, zeroImgMatrix])
        g = cv.merge([zeroImgMatrix, g, zeroImgMatrix])
        r = cv.merge([zeroImgMatrix, zeroImgMatrix, r])
        
        cv.imwrite(nombre_b, img_b)
        cv.imwrite(nombre_g, img_g)
        cv.imwrite(nombre_r, img_r)
        
        # cv.imshow(nombre_b, img_b) #Se obtiene la imagen en el canal B y su visualización es en escala a grises
        # cv.imshow(nombre_g, img_g) #Se obtiene la imagen en el canal G y su visualización es en escala a grises
        # cv.imshow(nombre_r, img_r) #Se obtiene la imagen en el canal R y su visualización es en escala a grises
        
        cv.imshow(nombre_b1, b)
        cv.imshow(nombre_g1, g)
        cv.imshow(nombre_r1, r)

        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def umbralizacion(self, umbral):
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        _, img_binaria = cv.threshold(img_grises, umbral, 255, cv.THRESH_BINARY)
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_Umbralizada.jpg'
        cv.imshow(nombre, img_binaria)
        cv.imwrite(nombre, img_binaria)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    def invertir(self, umbral):
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        _, img_binaria = cv.threshold(img_grises, umbral, 255, cv.THRESH_BINARY_INV)
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_Umbralizada_Inv.jpg'
        cv.imshow(nombre, img_binaria)
        cv.imwrite(nombre, img_binaria)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def contornos(self, umbral):
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        _, img_binaria = cv.threshold(img_grises, umbral, 255, cv.THRESH_BINARY_INV)
        
        contornos,_ = cv.findContours(img_binaria, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_Contornos.jpg'
        
        cv.drawContours(nueva_img, contornos, -1, (0,0,255), 2)
        cv.imshow(nombre, nueva_img)
        cv.imwrite(nombre, nueva_img)
        cv.waitKey(0)
        
        # for i in range(num_contornos):
        
        cv.destroyAllWindows()
    
    def erosion(self, umbral, iteraciones):
        kernel = np.array(
            [[0,1,0],
            [1,1,1],
            [0,1,0]]
            , np.uint8)
        # kernel = cv.imread('ee2.jpg')
        
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        _, img_binaria = cv.threshold(img_grises, umbral, 255, cv.THRESH_BINARY)
        
        img_erosion = cv.erode(img_binaria, kernel, iterations=iteraciones)
        
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_erosion.jpg'
        
        cv.imshow(nombre, img_erosion)
        cv.imwrite(nombre, img_erosion)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def dilatacion(self, umbral, iteraciones):
        kernel = np.ones((3,3), np.uint8)
        
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        _, img_binaria = cv.threshold(img_grises, umbral, 255, cv.THRESH_BINARY)
        
        img_dilatacion = cv.dilate(img_binaria, kernel, iterations=iteraciones)
        
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_dilatacion.jpg'
        
        cv.imshow(nombre, img_dilatacion)
        cv.imwrite(nombre, img_dilatacion)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    def apertura(self, umbral):
        kernel = np.ones((3,3), np.uint8)
        
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        _, img_binaria = cv.threshold(img_grises, umbral, 255, cv.THRESH_BINARY)
        
        img_apertura = cv.morphologyEx(img_binaria, cv.MORPH_OPEN, kernel)
        
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_apertura.jpg'
        
        cv.imshow(nombre, img_apertura)
        cv.imwrite(nombre, img_apertura)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    def cierre(self, umbral):
        kernel = np.ones((3,3), np.uint8)
        
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        _, img_binaria = cv.threshold(img_grises, umbral, 255, cv.THRESH_BINARY)
        
        img_cierre = cv.morphologyEx(img_binaria, cv.MORPH_CLOSE, kernel)
        
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_cierre.jpg'
        
        cv.imshow(nombre, img_cierre)
        cv.imwrite(nombre, img_cierre)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def gradiente(self, umbral):
        kernel = np.ones((3,3), np.uint8)
        
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        _, img_binaria = cv.threshold(img_grises, umbral, 255, cv.THRESH_BINARY)
        
        img_gradiente = cv.morphologyEx(img_binaria, cv.MORPH_GRADIENT, kernel)
        
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_gradienteMorfologico.jpg'
        
        cv.imshow(nombre, img_gradiente)
        cv.imwrite(nombre, img_gradiente)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def hitmiss(self, umbral):
        kernel = np.ones((3,3), np.uint8)
        
        nueva_img = self.imagen
        img_grises = cv.cvtColor(nueva_img, cv.COLOR_BGR2GRAY)
        _, img_binaria = cv.threshold(img_grises, umbral, 255, cv.THRESH_BINARY)
        
        img_hitmiss = cv.morphologyEx(img_binaria, cv.MORPH_HITMISS, kernel)
        
        contornos,_ = cv.findContours(img_binaria, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        
        nombre_l = self.nombre.split('.')
        nombre = nombre_l[0] + '_hit&miss.jpg'
        
        cv.imshow(nombre, img_hitmiss)
        cv.imwrite(nombre, img_hitmiss)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
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
        
        self.btnGris = Button(self.frame1, text='Grises', bg=self.color_base, fg=self.color_fuente, command=self.grises)
        self.btnGris.place(x=200,y=120)
        
        self.btnCanales = Button(self.frame1, text='BGR', bg=self.color_base, fg=self.color_fuente, command=self.canales)
        self.btnCanales.place(x=200,y=160)
        
        ############# Entrys ############
        
        self.columnas = Entry(self.frame1, width=5)
        self.columnas.place(x=390,y=120)
        self.lblcol = Label(self.frame1, text='valor 1', bg=self.color_base, fg=self.color_fuente) 
        self.lblcol.place(x=335,y=120)
        
        self.filas = Entry(self.frame1, width=5)
        self.filas.place(x=390,y=150)
        self.lblfila = Label(self.frame1, text='valor 2', bg=self.color_base, fg=self.color_fuente)
        self.lblfila.place(x=335,y=150)
        
        self.columnas1 = Entry(self.frame1, width=5)
        self.columnas1.place(x=390,y=180)
        self.lblcol1 = Label(self.frame1, text='valor 3', bg=self.color_base, fg=self.color_fuente)
        self.lblcol1.place(x=335,y=180)
        
        self.filas1 = Entry(self.frame1, width=5)
        self.filas1.place(x=390,y=210)
        self.lblfil1 = Label(self.frame1, text='valor 4', bg=self.color_base, fg=self.color_fuente)
        self.lblfil1.place(x=335,y=210)
        
        ############ Operaciones que necesitan de los entrys ##############
        
        self.btnFile = Button(self.frame1, text='Traslación', bg=self.color_base, fg=self.color_fuente, command= lambda: self.traslacion(float(self.columnas.get()), float(self.filas.get())))
        self.btnFile.place(x=35,y=120)
        
        self.btnFile = Button(self.frame1, text='Rotación', bg=self.color_base, fg=self.color_fuente, command= lambda: self.rotacion(float(self.columnas.get()), float(self.filas.get())))
        self.btnFile.place(x=35,y=160)
        
        self.btnFile = Button(self.frame1, text='Escalar', bg=self.color_base, fg=self.color_fuente, command= lambda: self.escalado(int(self.columnas.get())))
        self.btnFile.place(x=35,y=200)
        
        self.btnFile = Button(self.frame1, text='Recortar', bg=self.color_base, fg=self.color_fuente, command= lambda: self.recortar(int(self.columnas.get()), int(self.columnas1.get()), int(self.filas.get()), int(self.filas1.get())))
        self.btnFile.place(x=35,y=240)
        
        self.btnFile = Button(self.frame1, text='Umbralizar', bg=self.color_base, fg=self.color_fuente, command= lambda: self.umbralizacion(float(self.columnas.get())))
        self.btnFile.place(x=35,y=280)
        
        self.btnFile = Button(self.frame1, text='Umbralizar Inv', bg=self.color_base, fg=self.color_fuente, command= lambda: self.invertir(float(self.columnas.get())))
        self.btnFile.place(x=35,y=320)
        
        self.btnContornos = Button(self.frame1, text='Contornos', bg=self.color_base, fg=self.color_fuente, command= lambda: self.contornos(float(self.columnas.get())))
        self.btnContornos.place(x=200,y=200)
        
        self.btnContornos = Button(self.frame1, text='Erosión', bg=self.color_base, fg=self.color_fuente, command= lambda: self.erosion(float(self.columnas.get()), int(self.filas.get())))
        self.btnContornos.place(x=200,y=240)
        
        self.btnContornos = Button(self.frame1, text='Dilatación', bg=self.color_base, fg=self.color_fuente, command= lambda: self.dilatacion(float(self.columnas.get()), int(self.filas.get())))
        self.btnContornos.place(x=200,y=280)
        
        self.btnContornos = Button(self.frame1, text='Apertura', bg=self.color_base, fg=self.color_fuente, command= lambda: self.apertura(float(self.columnas.get())))
        self.btnContornos.place(x=200,y=320)
        
        self.btnContornos = Button(self.frame1, text='Cierre', bg=self.color_base, fg=self.color_fuente, command= lambda: self.cierre(float(self.columnas.get())))
        self.btnContornos.place(x=335,y=240)
        
        self.btnContornos = Button(self.frame1, text='Gradiente', bg=self.color_base, fg=self.color_fuente, command= lambda: self.gradiente(float(self.columnas.get())))
        self.btnContornos.place(x=335,y=280)

        self.btnContornos = Button(self.frame1, text='Hit-&-Miss', bg=self.color_base, fg=self.color_fuente, command= lambda: self.hitmiss(float(self.columnas.get())))
        self.btnContornos.place(x=335,y=320)
        
        #############################
        
        self.root.mainloop()

gui = GUI()