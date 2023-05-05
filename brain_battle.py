from tkinter import Tk, Label, PhotoImage, font, Frame
import tkinter as tk
import time
import threading
import random
import RPi.GPIO as gpio


GREEN_GPIO = 21
RED_GPIO   = 20


#seta a GPIO
gpio.setmode(gpio.BCM)
gpio.setup(GREEN_GPIO, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(RED_GPIO, gpio.IN, pull_up_down = gpio.PUD_DOWN)

janela = Tk()
janela.geometry("1024x810") 

#TITULO
janela.title("Brain battle")

top = Frame(janela)
top.pack(side=tk.TOP)

buttons = Frame(janela)
buttons.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

#logo IFRN
bg = PhotoImage(file="ifrn-logo.png") 
logo = Label( janela, image=bg, bg='white')
logo.pack(in_=top)

#cores
red         = '#c81f25'
red_light   = '#ff0009'
green       = '#2e9946'
green_light = '#0ed13a'



janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

myFont = font.Font(size=180)

botaoVerde     = Label(janela, 
                    font=myFont, 
                    fg='white', 
                    background=green, 
                    text='0')
botaoVermelho = Label(janela, 
                    font=myFont, 
                    fg='white', 
                    background=red, 
                    text='0')


botaoVerde.pack(in_=buttons,side=tk.LEFT, expand=True, fill='both')
botaoVermelho.pack(in_=buttons,side=tk.RIGHT, expand=True, fill='both')

# ACOES
stopBlinking = True

def addPontoAzul(evt):
    global stopBlinking
    stopBlinking = True
    botaoVerde['text'] = int(botaoVerde['text']) + 1

def decPontoAzul(evt):
    botaoVerde['text'] = int(botaoVerde['text']) - 1

def addPontoVermelho(evt):
    global stopBlinking
    stopBlinking = True
    botaoVermelho['text'] = int(botaoVermelho['text']) + 1

def decPontoVermelho(evt):
    botaoVermelho['text'] = int(botaoVermelho['text']) - 1

botaoVerde.bind("<Button-1>", addPontoAzul)
botaoVerde.bind("<Button-3>", decPontoAzul)

botaoVermelho.bind("<Button-1>", addPontoVermelho)
botaoVermelho.bind("<Button-3>", decPontoVermelho)


def lightEffect(button):
    global stopBlinking
    stopBlinking = False
    bkColor = button['bg']
    newColor = green_light
    if (button['bg'] == red):
        newColor = red_light
    while stopBlinking == False:
        button['bg'] = newColor
        time.sleep(.5)
        button['bg'] = bkColor
        time.sleep(.5)
    button['bg'] = bkColor

def thread_function(name):
    while True:
        if (gpio.input(GREEN_GPIO) == 1):
            lightEffect(botaoVerde)
        elif(gpio.input(RED_GPIO) == 1):
            lightEffect(botaoVermelho)
        
        
        #codigo para simular o apertar dos botoes aleatoriamente
        #time.sleep(5)
        #if (random.randint(0,1)):
        #    lightEffect(botaoVerde)
        #else:
        #    lightEffect(botaoVermelho)

x = threading.Thread(target=thread_function, args=(1,))
x.start()

janela.configure(bg='white')
janela.mainloop()

gpio.cleanup()
exit()