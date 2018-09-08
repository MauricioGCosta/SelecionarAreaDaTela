# coding: utf-8

# Define imports
from django.shortcuts import render
from PIL import ImageDraw, Image, ImageTk
import sys
from tkinter import filedialog
import tkinter

# Define Variaveis locais e globais, estas utilizadas para guardar as coordenadas
x1 = x2 = y1 = y2 = clique = 0
linha = []

def home(request):
    # Funcao que desenha o retangulo
    def draw_rectangle(draw, coordinates, color, width=1):
        for i in range(width):
            rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
            rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)
            draw.rectangle((rect_start, rect_end), outline=color)

    # Captura evento de cada clique na tela
    def callback(event):
        global x1; global x2; global y1; global y2; global clique; global linha

        # Testa validacao se coordenadas sao maiores que zero
        if (event.x > 0 and event.y > 0):

            if (clique == 0):
                x1 = event.x
                y1 = event.y
            elif (clique == 1):
                x2 = event.x
                y2 = event.y
                # Desenha o retangulo na tela
                canvas.create_rectangle(x1, y1, x2, y2, width=3)

                # Guarda no vetor para resultado final
                linha.append(window.filename + ", " + str(x1) + ", " + str(y1) + ", " + str(x2) + ", " + str(y2))
                clique = -1

            clique += 1

    escolheu_arquivo = True

    # Loop para cada arquivo desejado
    while escolheu_arquivo:

        # Janela do retangulo
        window = tkinter.Tk(className=" Quadrado: Clique no canto superior esquerdo, depois clique no canto inferior direito")

        # Janela File Dialog
        window.filename = filedialog.askopenfilename(initialdir="/", title="Selecione um Arquivo, para SAIR clique Cancelar",
                                                     filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        arquivo = window.filename

        # Testa fim de programa
        if (window.filename == ""):
            escolheu_arquivo = False
            break

        # Apresenta tela
        image = Image.open(arquivo)
        image = image.resize((640, 640), Image.ANTIALIAS)
        canvas = tkinter.Canvas(window, width=image.size[0], height=image.size[1])
        canvas.pack()
        image_tk = ImageTk.PhotoImage(image)
        canvas.create_image(image.size[0] // 2, image.size[1] // 2, image=image_tk)
        canvas.bind("<Button-1>", callback)
        canvas.mainloop()

    # Grava resultado final
    arquivo = open('Resultado.csv', 'w')
    for cada_linha in linha:
        arquivo.write('%s\n' % cada_linha)
    arquivo.close()

    return render(request, 'selecoes.html')
