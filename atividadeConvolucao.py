#! /usr/bin/env python
# coding: utf-8

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
__     _____ ____  /\/|  ___  	  ____ ___  __  __ ____  _   _ _____  _    ____ ___ ___  _   _    _    _   
\ \   / /_ _/ ___||/\/  / _ \ 	 / ___/ _ \|  \/  |  _ \| | | |_   _|/ \  / ___|_ _/ _ \| \ | |  / \  | | 
 \ \ / / | |\___ \ /_\ | | | |	| |  | | | | |\/| | |_) | | | | | | / _ \| |    | | | | |  \| | / _ \ | |  
  \ V /  | | ___) / _ \| |_| |	| |__| |_| | |  | |  __/| |_| | | |/ ___ \ |___ | | |_| | |\  |/ ___ \| |___ 
   \_/  |___|____/_/ \_\\___/ 	 \____\___/|_|  |_|_|    \___/  |_/_/   \_\____|___\___/|_| \_/_/   \_\_____|
                              
 ### VISAO COMPUTACIONAL - 03/10/2016 - Convolução ###
 Acadêmico: Gabriel Kirsten Menezes RA: 148298

 - Descrição:
	Produzir um software que implemente as seguintes funcionalidades:
		- Abrir um arquivo de imagem escolhida pelo usuário;
		- Converte para tons de cinza;
		- Ler uma matriz 7x7 contendo os valores de uma matriz de convolução (como um recurso extra, o software poderá também deixar que o usuário escolha  o tamanho da matriz);
		- Realizar a convolução da matriz com a imagem, mostrando passo a passo as matrizes intermediárias resultantes, destacando o valor central (a meta aqui é possibilitar ao usuário a visualização do que acontece internamente durante uma convolução, para cada pixel da imagem);
		- Permitir que a matriz seja salva e lida de um arquivo (o usuário deve ter a flexibilidade de usar e entrar com diferentes matrizes e portanto, para não ter que ficar digitando todos os elementos toda vez que precisar usar uma mesma matriz, o software precisa oferecer a opção de salvar e ler do disco rídigo);
		- Mostrar a imagem resultante da convolução ao lado da imagem original;
 
 - Requisitos e informações adicionais: 
	- Como bibliotecas de apoio para processamento de imagens poderão ser utilizadas a ImageJ ou a OpenCV, no entanto,  a convolução deve ser implementada completamente (não é válido apenas utilizar a operação de convolução disponível nas bibliotecas);
	- Releia as instruções sobre procedimentos e critérios de avaliação disponíveis no Planejamento Educacional da Disciplina (principalmente as que se referem à geração de código).
	
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import cv2                                          # importacao da biblioteca do OpenCV
from Tkinter import *                               # biblioteca para selecao do arquivo
from tkFileDialog import *                          # biblioteca para selecao do arquivo
from PIL import Image                               # interface para imagem
from PIL import ImageTk                             # interface para imagem
from skimage.exposure import rescale_intensity      # biblioteca para normalização

# Variaveis globais #
imgOrig = img = img_greyScale = filename = img_conv = root = gui = None
tamx = cancel = x1 = y1 = acumulador = acumuladorM = 0
oldx = oldy = 0

class Step:
    """

    # Classe Step #
    Classe utilizada para exibir uma interface que mostra o processo de convolução passo a passo

    """

    def __init__(self, parent):
    	#utilização de variaveis globais
        global x1, y1, oldx, oldy
        
        # cria uma nova janela
        self.top = Toplevel(parent.master)
        self.top.title("Step")

        # cria os componentes de interface
        
        # frame que armazena os componentes da matriz
        containerMatrizPrincipal = LabelFrame(self.top, relief=GROOVE, borderwidth=2, padx="10", pady="10", text="Convolution Matrix * Pixel")
        containerMatrizPrincipal["pady"] = 10
        containerMatrizPrincipal.pack(expand="yes", side="top")
        
        # matriz que armazena os valores da matriz
        containerMatriz = []
        
      	# valores da matriz
        m = [[[]]]

        # imprime os valores da matriz de convolução multiplicada pelos valores dos pixels
        for x in range(-int((tamx + 1) / 2), int((tamx) / 2)):  # Linhas
			# cria um novo elemento que posicionará todos elementos da linha
            containerMatriz.append(Frame(containerMatrizPrincipal, pady="10"))
            containerMatriz[x + int((tamx + 1) / 2)].pack(side="top", expand="no")
            
            # cria uma nova linha na matriz
            m.append([])

            for y in range(-int((tamx + 1) / 2), int((tamx) / 2)):  # Colunas
				
				#cria uma nova coluna na matriz
                m[x + int((tamx + 1) / 2)].append([])

                # tenta exibir o valor, se não for possivel, exibe zero
                try:
                    saida = str(int(parent.m[int((tamx + 1) / 2) + x + 1][int((tamx + 1) / 2) + y + 1][0].get()) * img_greyScale.item((x1 + x + 1), (y1 + y + 1)))
                    m[int((tamx + 1) / 2 + x)][int((tamx + 1) / 2) + y].append(Label(containerMatriz[int((tamx + 1) / 2) + x], text=saida))
                except:
                    m[int((tamx + 1) / 2 + x)][int((tamx + 1) / 2) + y].append(Label(containerMatriz[int((tamx + 1) / 2) + x], text="0"))
				
				# configura os parâmentros do elemento
                m[int((tamx + 1) / 2) + x][int((tamx + 1) / 2) + y][0]["width"] = 5
                m[int((tamx + 1) / 2) + x][int((tamx + 1) / 2) + y][0].pack(side="left", padx="10")

        # adiciona os botões
        frameBtn = Frame(self.top)
        frameBtn.pack(side="bottom")
        b = Button(frameBtn, text="NEXT STEP >", command=self.nextStep).pack(side="right", pady=5, padx=5)
        b2 = Button(frameBtn, text="RESUME", command=self.endR).pack(side="left", pady=5, padx=5)
        frameBottom = Frame(self.top)
        frameBottom.pack(side="bottom")
        
        # aciciona as labels com os valores de ACC e Auto Divisor
        containerAcc = LabelFrame(frameBottom, relief=GROOVE, borderwidth=2, padx="2", pady="2", text="ACC")
        containerAcc.pack(expand="yes", side="left")
        acc = Label(containerAcc, text=str(parent.acumulador))
        acc["width"] = 10
        acc.pack(side="left", padx="10")
        containerAccM = LabelFrame(frameBottom, relief=GROOVE, borderwidth=2, padx="2", pady="2", text="Auto Divisor")
        containerAccM.pack(expand="yes", side="left")

        # condição para realizar o fator de divisão quando a somatoria dos valores presentes na matriz de convolução for diferente de zero
        if parent.acumuladorM != 0:
            accM = Label(containerAccM, text=str(parent.acumuladorM))
            containerACCN = LabelFrame(frameBottom, relief=GROOVE, borderwidth=2, padx="2", pady="2", text="New ACC")
            containerACCN.pack(expand="yes", side="left")
            accN = Label(containerACCN, text=str(parent.acumulador / parent.acumuladorM))
            accN["width"] = 10
            accN.pack(side="left", padx="10")

        else:
            accM = Label(containerAccM, text="0")

        # posiciona o elemento Label
        accM["width"] = 10
        accM.pack(side="left", padx="10")

        # calcula as coordenadas para posicionamento da janela
        w = 300 + (48 * tamx)  # width da interface
        h = 110 + (48 * tamx)  # height da interface

        ws = self.top.winfo_screenwidth()  # width da tela
        hs = self.top.winfo_screenheight()  # height da tela

        # calcula as coordenadas da tela
        if oldx != 0:
            x = oldx
        else:
            x = (ws / 2) - (w / 2)
        if oldy != 0:
            y = oldy
        else:
            y = (hs / 2) - (h / 2)

        # exibe a janela com o tamanho definido e no centro da tela
        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.top.wm_attributes("-topmost", 1)
        self.top.focus_force()

    # Método para prosseguir a convolução
    def nextStep(self):
        global oldx, oldy
        # obtêm os valores de posicionamento da janela, para a mesma ser posicionada no mesmo lugar no proximo step
        oldx = self.top.winfo_x()
        oldy = self.top.winfo_y() - 28
        self.top.destroy()

    # Método para encerrar a convolução passo a passo
    def endR(self):
        global gui
        gui.cancel = 1
        self.top.destroy()


## ------ FIM CLASSE STEP ------ ##

class DialogMatrix:
    """

    # Classe DialogMatrix #
    Classe utilizada para exibir uma interface para entrada do tamanho da matriz

    """

    def __init__(self, parent):
        # cria um novo objeto de interface
        top = self.top = Toplevel(parent)
        self.top.title("Matrix Size")
        Label(top, text="Set the matrix size...").pack(pady="10")
        self.entrada = Entry(top)
        Label(top, text="Size: ").pack(side="left", padx=5, pady=5)
        self.entrada.pack(side="left", padx=5, pady=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5, padx=5)

        w = 300  # width da interface
        h = 80  # height da interface
        ws = self.top.winfo_screenwidth()  # width da tela
        hs = self.top.winfo_screenheight()  # height da tela

        # calcula as coordenadas para posicionamento da interface
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.top.wm_attributes("-topmost", 1)
        self.top.focus_force()

    # metodo ok que valida e entrada e salva na variavel global
    def ok(self):
        try:
            int(self.entrada.get())
        except ValueError:
            print "ERROR - matrix size (input)"
        else:
            global tamx
            tamx = self.entrada.get()
            self.top.destroy()


## ------ FIM CLASSE DIALOGMATRIX ------ ##

class Gui:
    """

    # Classe Gui #
    Classe utilizada para exibir uma interface principal, que contém as opções e imagens.

    """

    def __init__(self, master):
        global tamx
        tamx = int(tamx)
        
        # posicionamento dos componentes de interfafce
        self.master = master
        self.mainContainerEsquerda = Frame(master=self.master, relief=RAISED, borderwidth=1, padx="10", pady="10")
        self.mainContainerEsquerda.pack(expand="no", fill="both", side="left")

        self.mainContainerDireita = Frame(master=self.master, relief=RAISED, borderwidth=1, padx="10", pady="10")
        self.mainContainerDireita.pack(expand="yes", fill="both", side="right")

        self.btnAplicarConvolucao = Button(master=self.mainContainerEsquerda, text="> Convolution",command=lambda: self.aplicaConvolucao(1))
        self.btnAplicarConvolucao.pack(fill="x", side="bottom")
        self.btnAplicarConvolucaoStep = Button(master=self.mainContainerEsquerda, text="> Convolution Step",command=lambda: self.aplicaConvolucao(0))
        self.btnAplicarConvolucaoStep.pack(fill="x", side="bottom")

        self.imgOrigC = LabelFrame(master=self.mainContainerDireita, text="Original Image")
        self.imgConvC = LabelFrame(master=self.mainContainerDireita, text="Convolution Image")

        self.mainImg = Label(self.imgOrigC, img=None)
        self.mainImg.pack(padx=10, pady=10, fill="both", expand="yes")

        self.mainImgC = Label(self.imgConvC, img=None)
        self.mainImgC.pack(padx=10, pady=10, fill="both", expand="yes")

        self.imgOrigC.pack(expand="yes", side="left", fill="both", padx="10", pady="10")
        self.imgConvC.pack(expand="yes", side="right", fill="both", padx="10", pady="10")

        self.containerMatriz = []
        self.m = [[[]]]

        self.containerMatrizPrincipal = LabelFrame(master=self.mainContainerEsquerda, relief=GROOVE, borderwidth=2, padx="10",pady="10", text="Convolution Matrix")
        self.containerMatrizPrincipal["pady"] = 10
        self.containerMatrizPrincipal.pack(expand="no", side="top")

        self.containerOpc = LabelFrame(master=self.mainContainerEsquerda, relief=GROOVE, borderwidth=2, padx="10", pady="10",text="Resize image")
        self.containerOpc.pack(fill="x", side="bottom")

        # opção para redimensionar, default = selecionada
        self.resize = IntVar()
        c = Checkbutton(master=self.containerOpc, text="Enable resize image", variable=self.resize)
        c.pack()
        c.select()

        # opção para exibir valores dos pixels, default = selecionada
        self.pValue = IntVar()
        p = Checkbutton(master=self.containerOpc, text="Display pixel value", variable=self.pValue)
        p.pack()
        p.select()

        # Menu de opções superior
        menubar = Menu(master)
        imagemenu = Menu(menubar, tearoff=0)
        imagemenu.add_command(label="Open Image", command=lambda: self.abrir_imagem())
        imagemenu.add_command(label="Save Image as...", command=self.salvar_imagem)
        menubar.add_cascade(label="Image Options", menu=imagemenu)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Matrix", command=self.abrir_matriz)
        filemenu.add_command(label="Save matrix as...", command=self.salvar_matriz)
        menubar.add_cascade(label="Matrix Options", menu=filemenu)
        self.master.config(menu=menubar)

        # imprime os indices da matriz
        for x in range(0, 1):  # linhas
            self.containerMatriz.append(Frame(self.containerMatrizPrincipal, pady="10"))
            self.containerMatriz[x].pack(side="top", expand="no")
            self.m.append([])
            for y in range(0, tamx + 1):  # colunas
                self.m[x].append([])
                if y == 0:
                    self.m[x][y].append(Label(self.containerMatriz[x], text=""))
                else:
                    self.m[x][y].append(Label(self.containerMatriz[x], text=y))
                self.m[x][y][0].pack(side="left", padx="15")

        # cria os campos de entrada de valores para matriz
        for x in range(1, tamx + 1):  # linhas
            self.containerMatriz.append(Frame(self.containerMatrizPrincipal, pady="10"))
            self.containerMatriz[x].pack(side="top", expand="no")
            self.m.append([])
            self.m[x].append([])
            self.m[x][0].append(Label(self.containerMatriz[x], text=x))
            self.m[x][0][0].pack(side="left", padx=10, pady=5, fill="both", expand="yes")
            for y in range(1, tamx + 1):  # colunas
                self.m[x].append([])
                self.m[x][y].append(Entry(self.containerMatriz[x]))
                self.m[x][y][0]["width"] = 2
                self.m[x][y][0].pack(side="left", padx="10")

        w = 800 + (48 * tamx)  # width da interface
        h = 300 + (48 * tamx)  # height da interface
        ws = self.master.winfo_screenwidth()  # width da tela
        hs = self.master.winfo_screenheight()  # height da tela

        # calcula as coordenadas da tela
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # posiciona janela no centro da tela
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # metodo para abrir a imagem
    def abrir_imagem(self):
        global filename, img_greyScale
        filename = askopenfilename(filetypes=[("Image Files", '*')])
        if len(filename) > 0:
            try:
                # abrir imagem selecionada em tons de cinza
                img_greyScale = cv2.imread(filename.encode('utf-8'), cv2.IMREAD_GRAYSCALE)
                if self.resize.get():
                    # se a condição de redimensionamento da imagem estiver selecionada, a imagem é redimensionada
                    height, width = img_greyScale.shape[:2]
                    img_greyScale = cv2.resize(img_greyScale, (width / 10, height / 10), interpolation=cv2.INTER_AREA)
                    img = cv2.resize(img_greyScale, (width * 3, height * 3), interpolation=cv2.INTER_AREA)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    height, width = img.shape[:2]
                    if (self.pValue.get()):
                        # se a condição de exibição dos valores dos pixels estiver selecionada, os valores são exibidos
                        for x in range(0, (width / 30)):
                            for y in range(0, (height / 30)):
                                try:
                                    # condição para imprimir o texto na cor oposta ao valor do pixel
                                    if int(img_greyScale.item(y, x)) >= 127:
                                        cv2.putText(img, str(img_greyScale.item(y, x)), ((x * width / (width / 30)), (
                                        y * height / (height / 30)) + height / (height / 20)), font, 0.4, (0, 0, 0), 1,
                                                    cv2.LINE_AA)  # escreve o valor na imagem
                                    else:
                                        cv2.putText(img, str(img_greyScale.item(y, x)), ((x * width / (width / 30)), (
                                        y * height / (height / 30)) + height / (height / 20)), font, 0.4,
                                                    (255, 255, 255), 1, cv2.LINE_AA)  # escreve o valor na imagem
                                except:
                                    pass
                else:
                    img = img_greyScale

                # exibe a imagem na interface
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(img)
                self.mainImg.image = img
                self.mainImg.configure(image=img)
            except:
                print "ERROR - Image can't be open"

    # metodo que salva a imagem apos a convolução
    def salvar_imagem(self):
        global img_conv
        if img_conv != None:
            filenameImagem = asksaveasfilename(filetypes=[("Image Files", '*')])
            if len(filenameImagem) > 0:
                cv2.imwrite(filenameImagem, img_conv)

    # metodo para salvar uma matriz
    def salvar_matriz(self):
        filenameMatriz = asksaveasfilename(filetypes=[("Matrix Files", '*.mtx')])
        if len(filenameMatriz) > 0:
            arquivoMatriz = open(filenameMatriz.encode('utf-8'), 'wb')
            conteudoMatriz = ""
            for x in range(1, tamx + 1):
                for y in range(1, tamx + 1):
                    conteudoMatriz += self.m[x][y][0].get()
                    if y != tamx:
                        conteudoMatriz += ","
                conteudoMatriz += "\n"
            arquivoMatriz.write(conteudoMatriz)
            arquivoMatriz.close()

    # metodo para abrir uma matriz
    def abrir_matriz(self):
        filenameMatriz = askopenfilename(filetypes=[("Matrix Files", '*.mtx')])
        if len(filenameMatriz) > 0:
            arquivoMatriz = open(filenameMatriz.encode('utf-8'), 'r')
            conteudoMatriz = arquivoMatriz.read().split('\n')
            try:
                for x in range(0, len(conteudoMatriz) - 1):
                    conteudoMatrizColuna = conteudoMatriz[x].split(',')
                    for y in range(0, len(conteudoMatrizColuna)):
                        self.m[x + 1][y + 1][0].delete(0, END)
                        self.m[x + 1][y + 1][0].insert(0, conteudoMatrizColuna[y])
                arquivoMatriz.close()
            except:
                print "ERROR - matrix size (on load)"

    # metodo que aplica a convolução na imagem
    def aplicaConvolucao(self, c):
        global x1, y1
        self.cancel = c
        if filename == None:
            print "ERROR - Image not selected"
        else:
            self.acumulador = self.acumuladorM = 0
            img_conv = img_greyScale.copy()
            alt = len(img_greyScale)
            lag = len(img_greyScale[0])
            img_conv = 1.0 * img_conv

            # calcula o valor de divisão para normalização da matriz de convolução
            for x2 in range(1, tamx + 1):
                for y2 in range(1, tamx + 1):
                    try:
                        self.acumuladorM += int(self.m[x2][y2][0].get())
                    except:
                        pass

            # aplica a convolução na imagem
            for x1 in xrange(alt):
                for y1 in xrange(lag):
                    self.acumulador = 0
                    for x2 in range(-int((tamx) / 2), int((tamx + 1) / 2)):
                        for y2 in range(-int((tamx) / 2), int((tamx + 1) / 2)):
                            try:
                                self.acumulador += int(self.m[int((tamx + 1) / 2) + x2][int((tamx + 1) / 2) + y2][
                                                           0].get()) * img_greyScale.item((x1 + x2), (y1 + y2))
                                if (self.cancel == 0):
                                    # se o programa ainda se encontrar no modo de execução passo a passo
                                    if self.resize.get():
                                        # se a opçao de redimensionamento ainda estiver selecionada
                                        if self.acumuladorM != 0:
                                            img_conv.itemset((x1, y1), int(float(self.acumulador / (self.acumuladorM))))
                                        else:
                                            img_conv.itemset((x1, y1), int(float(self.acumulador)))

                                        font = cv2.FONT_HERSHEY_SIMPLEX

                                        temp_conv = rescale_intensity(img_conv, in_range=(0, 255))
                                        temp_conv = (temp_conv * 255).astype("uint8")
                                        height, width = temp_conv.shape[:2]
                                        temp_conv = cv2.resize(temp_conv, (width * 30, height * 30), interpolation=cv2.INTER_AREA)
                                        height, width = temp_conv.shape[:2]

                                        if (self.pValue.get()):
                                            # se a opçao de exibição do valor do pixel ainda estiver selecionada
                                            if int(img_conv.item(x1, y1)) >= 127:
                                                cv2.putText(temp_conv, str(int(img_conv.item(x1, y1))),
                                                            ((y1 * height / 10), (x1 * width / 10) + width / 15), font,
                                                            0.4, (0, 0, 0), 1, cv2.LINE_AA)  # escreve o valor na imagem
                                            else:
                                                cv2.putText(temp_conv, str(int(img_conv.item(x1, y1))),
                                                            ((y1 * height / 10), (x1 * width / 10) + width / 15), font,
                                                            0.4, (255, 255, 255), 1,
                                                            cv2.LINE_AA)  # escreve o valor na imagem

                                        # converte a imagem para o formato do imageTk
                                        img = Image.fromarray(temp_conv)
                                        img = ImageTk.PhotoImage(img)
                                        
                                        # atualiza a imagem
                                        self.mainImgC.image = img
                                        self.mainImgC.configure(image=img)
                            except:
                                pass

                    if self.acumuladorM != 0:
                        # se houver fator de divisão para normalização da  matriz de convolução
                        img_conv.itemset((x1, y1), int(float(self.acumulador / (self.acumuladorM))))
                    else:
                        img_conv.itemset((x1, y1), int(float(self.acumulador)))

                    if (self.cancel == 0):
                        # se o metodo de passo a passo ainda estiver ativo
                        d = Step(self)
                        self.master.wait_window(d.top)

            # normaliza a imagem final
            img_conv = rescale_intensity(img_conv, in_range=(0, 255))
            img_conv = (img_conv * 255).astype("uint8")

            # exibe a imagem final
            if self.resize.get():
                # se a opção de redimensionamento estiver ativada
                height, width = img_conv.shape[:2]
                img_conv = cv2.resize(img_conv, (width * 30, height * 30), interpolation=cv2.INTER_AREA)

			# converte a imagem para o formato do imageTk
            img = Image.fromarray(img_conv)
            img = ImageTk.PhotoImage(img)
            
            # atualiza a imagem
            self.mainImgC.image = img
            self.mainImgC.configure(image=img)


## ------ FIM CLASSE GUI ------ ##

# MAIN			
def main():
    global gui
    root = Tk()
    w = 600  # width do Tk root
    h = 200  # height do Tk root
    ws = root.winfo_screenwidth()	# width da tela
    hs = root.winfo_screenheight()  # height da tela

    # calcula as coordenadas da tela
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title("Convolution - VC")
    root.cabecalho = Label(root, text="  Waiting matrix size..  ")
    root.cabecalho.pack(expand="yes", padx="10", pady="10")

    d = DialogMatrix(root)
    root.wait_window(d.top)
    root.cabecalho.pack_forget()
    gui = Gui(root)
    root.mainloop()


if __name__ == "__main__": main()

## ------ FIM MAIN ------ ##
