# convolution-tool-python
 The software comes an educational tool written in python to demonstrate a convolution operation in an image.
 
   Ps. Description in PT-BR
```
 ____  _____    _    ____  __  __ _____ 
|  _ \| ____|  / \  |  _ \|  \/  | ____|
| |_) |  _|   / _ \ | | | | |\/| |  _|  
|  _ <| |___ / ___ \| |_| | |  | | |___ 
|_| \_\_____/_/   \_\____/|_|  |_|_____|
```

Atividade - Visão Computacional

Implementar software para convolução 2D

Aluno: Gabriel Kirsten Menezes

Universidade Católica Dom Bosco

### Imagem do software
![alt tag](https://cloud.githubusercontent.com/assets/15522193/18115621/c9e96b1c-6f0e-11e6-8186-2a416f0d897d.png)
![alt tag](https://cloud.githubusercontent.com/assets/15522193/18115621/c9e96b1c-6f0e-11e6-8186-2a416f0d897d.png)
### Descrição

Desenvolvido em Python v2.7.12 utilizando como base a biblioteca OpenCV v3.0.0 
Sistema Operacional: Ubuntu 16.04 LTS 

BIBLIOTECAS ADICIONAIS:
  - numpy
  - argparse
  - sys
  - math
  - skimage

Software desenvolvido para disciplina de Visão Computacional, foram dedicadas em um intervalo de três semanas, cerca de 35 horas de desenvolvimento.
O sofware contou com a ajuda dos acadêmicos: Adair Oliveira (nas partes relacionadas a matriz de convolução e operação de convolução) e Pedro Lucas (na parte relacionada a biblioteca openCV e como ela se comporta com seus tipos de dados).
O material utilizado para estudo da convolução foi:
- http://www.pyimagesearch.com/2016/07/25/convolutions-with-opencv-and-python/
- http://docs.gimp.org/2.9/pt_BR/plug-in-convmatrix.html
	
A implementação deste software foi a mais complexa até o momento, foram encontrados muitos problemas em sua implementação. 

A interface foi gerada dinamicamente, de acordo com os valores de tamanho da matriz informados no inicio do programa, o que possibilitou trabalhar com matrizes de diferentes tamanhos.

A parte relacionada com a apresentação dos dados passo a passo foi inicialmente implementada com um interface no terminal utilizando a biblioteca curses do python, ela se mostrou uma solução fácil, pois já era conhecida, e boa para apresentação dos dados, pois conta com uma ótima estrutura de textos e cores, posteriormente foi implementada uma outra utilizando o tkinter.

Para a parte de apresentação dos dados no passo a passo, foi utilizada uma biblioteca para normalização da imagem (skimagem) e sua documentação foi obtida através do link http://nullege.com/codes/search/skimage.exposure.rescale_intensity.

Na convolução, o maior problema encontrado, foi na normalização, mesmo após a utilização do skimage, os dados que a matriz recebia, só eram recebidos na faixa de 0 a 255, todos os valores fora desta faixa eram salvos com outros valores, e sua normalização se mostrou sem sucesso. a solução foi transformar a imagem que estava no formato da biblioteca openCV para uma matriz de float com a operação:

	img_conv = 1.0 * img_conv

Após aplicar esta operação, a convolução é realizada e os valores são normalizados e transformados para o tipo unsigned int de 8 bits (0 a 255):

img_conv = rescale_intensity(img_conv, in_range=(0,255))
img_conv = (img_conv * 255).astype("uint8")	

Na implementação da convolução também optou-se por aplicar um fator de divisão nas matrizes de convolução que soma os valores da matriz e divide o valor do acumulador por esta soma, exemplo:

	MATRIZ DE CONVOLUÇÃO:
		|1	1	1|
		|1	1	1|
		|1	1	1|
		
	Soma dos valores = 9
	
	NOVA MATRIZ DE CONVOLUÇÃO:
				|1	1	1|
	(1/9) *		|1	1	1|
				|1	1	1|
			
	(para somatórias = 0, a operação acima não é aplicada)
	
A convolução implementada encara a matriz de imagem como uma matriz espelhada, exemplo: no final da matriz de pixels, o pixel ultimaposicaolinha+1 é o mesmo pixel de inicio da mesma linha.

** Etapas de desenvolvimento:

	- Estudo sobre o funcionamento da convolução;
	- Estudo da manipulação de arquivos em python;
	- Implementação das função abrir/salvar matrizes;
	- Implementação da interface;
	- Implementação da convolução;
	- Implementação da parte de apresentação passo-a-passo dos dados;
	- Aperfeiçoamento do código.


### Utilização

- Instale (se não estiver instalado) a biblioteca "ImageTk" com o comando: "sudo apt-get install python-imaging-tk";
- Instale (se não estiver instalado) a biblioteca "Skimage" com o comando: "sudo apt-get install python-skimage";
- Altere o diretório no terminal linux com o comando 'cd' até a pasta onde se encontra o arquivo atividadeConvolucao.py;
- Execute o código atividadeFolha.py com o comando "python atividadeConvolucao.py";
- Selecione o tamanho da matriz de convolução, o tamanho é referente a uma das dimensões de uma matriz quadrada no campo "Size" e pressione o botão "OK";

##### PARA ABRIR UMA IMAGEM COM OS VALORES DOS PIXELS (MAIS DIDÁTICO): 

(a imagem sofrerá uma redução de 10 vezes a quantidade de pixel)

(OPÇÃO FUNCIONA COM IMAGENS PEQUENAS, COMO A DO EXEMPLO "TESTE.JPG")

	- Selecione a opção "Enable resize image" no campo "Options"
	- No menu superior, selecione "Image Options" -> "Open Image" e selecione um arquivo de imagem que será aplicada a convolução;
--------------------------------------------------------------------------------
##### PARA ABRIR UMA IMAGEM:(OPÇÃO PARA IMAGENS MAIORES, PORÉM, MENOS DIDÁTICO
	- Selecione a opção "Enable resize image" no campo "Options"
	- No menu superior, selecione "Image Options" -> "Open Image" e selecione um arquivo de imagem que será aplicada a convolução;
--------------------------------------------------------------------------------
##### PARA DIGITAR UMA MATRIZ:
	- Informe os valores de cada campo da matriz de convolução no campo identificado por "Convolution Matrix";
--------------------------------------------------------------------------------
##### PARA CARREGAR UMA MATRIZ SALVA:
	- No menu superior, selecione "Matrix Options" -> "Open Matrix" e selecione um arquivo de matriz;
--------------------------------------------------------------------------------
##### PARA SALVAR UMA MATRIZ:
	- Digite os valores da matriz no campo "Convolution Matrix"
	- No menu superior, selecione "Matrix Options" -> "Save Matrix" e digite um nome e selecione um diretorio para salvar a matriz;
	(obs: por definição, salve os nomes da matriz seguidos do seu tamanho, exemplo: "canny3x3.mtx")
--------------------------------------------------------------------------------
##### PARA APLICAR A CONVOLUÇÃO PASSO A PASSO:
	- Verifique se a matriz de convolução esta completamente preenchida e há uma imagem selecionada;
	- Pressione o botão "Convolution Step";
	- Uma nova janela irá se abrir, sobrepondo as outras, pressione "STEP" para visualizar a convolução passo a passo;
	(os valores intermediários da convolução irão ser apresentados no terminal)
	(se desejar terminar a convolução, pressione o botão "RESUME", que a convolução irá ser aplicada até o final)
--------------------------------------------------------------------------------
##### PARA APLICAR A CONVOLUÇÃO SEM PASSO A PASSO:
	- Verifique se a matrix de convolução esta completamente preenchida e há uma imagem selecionada;
	- Pressione o botão "Convolution";
--------------------------------------------------------------------------------
### Estrutura de diretórios
        .
        |-- atividadeConvolucao
        |	|-- atividadeConvolucao.py (código em python)
        |	|-- teste.png (imagem de teste)
        |	|-- soja2.jpg (imagem da folha)
        |	|-- README.txt (arquivo contendo informações do software)
        |	|-- mtx (diretorio com matrizes de exemplo)
        |	|	|-- agucar3x3.mtx
        |	|	|-- cannyH3x3.mtx
        |	|	|-- desfoque3x3.mtx
        |	|	|-- desfoque7x7.mtx
        |	|	|-- destacarrelevo3x3.mtx
        |	|	|-- detectarbordas3x3.mtx
        |	|	|-- realcarbordas3x3.mtx
        |	|	|-- sharpen3x3.mtx
        |	|	|-- sobely3x3.mtx

--------------------------------------------------------------------------------
### Comandos 
```
--------------------------------------------------------------------------------
# Comando #                     |       # Descrição #
--------------------------------------------------------------------------------
Menu "Image Options"            |       Opções relacionadas com a imagem;
Opção "Open Image"              |       Abrir o seletor de imagem;
--------------------------------------------------------------------------------
Menu "Matrix Options"           |       Opções relacionadas com a matrizes;
Opção "Open Matrix"             |       Abrir uma matriz;
Opção "Save Matrix as..."       |       Salvar uma matriz digitada;
--------------------------------------------------------------------------------	
Botão "Convolution Step"        |       Aplica a convolução mostrando o passo a 
                                |       passo;
--------------------------------------------------------------------------------
Botão "Convolution"             |       Aplica a convolução;
--------------------------------------------------------------------------------
Opção "Enable resize image"     |       Faz a imagem ser carregada com 10x menos 
                                |       pixels e cada pixel aparecerá maior, 
                                |       dentro dele é exibido o valor 
                                |       correspondente.		
--------------------------------------------------------------------------------
```
