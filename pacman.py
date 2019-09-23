import pygame
import random

# definicao das cores
preto = (0,0,0)
branco = (255,255,255)
azul = (0,0,255)
vermelho = (255,0,0)

# imagem favicon

logo = pygame.image.load('persons/unifap.ico')
pygame.display.set_icon(logo)

# fundo musical
pygame.mixer.init()
pygame.mixer.music.load('pacman.mp3')
pygame.mixer.music.play(-1, 0.0)

class Parede(pygame.sprite.Sprite):
    def __init__(self,x,y,largura,altura, cor):
        pygame.sprite.Sprite.__init__(self)
  
        self.image = pygame.Surface([largura, altura])
        self.image.fill(cor)

        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

#cria as paredes do mapa
def iniciarFaseUm(lista_sprites):
    lista_parede=pygame.sprite.RenderPlain()
     
    # [x, y, largura, altura]
    paredes = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],            
            ]

    for item in paredes:
        parede=Parede(item[0],item[1],item[2],item[3],azul)
        lista_parede.add(parede)
        lista_sprites.add(parede)

    return lista_parede

def iniciarPortao(lista_sprites):
      portao = pygame.sprite.RenderPlain()
      lista_sprites.add(portao)
      return portao

class Bola(pygame.sprite.Sprite):
    def __init__(self, cor, largura, altura):
        # chama o construtor da classe pai (Sprite)
        pygame.sprite.Sprite.__init__(self) 
 
        self.image = pygame.Surface([largura, altura])
        self.image.fill(branco)
        self.image.set_colorkey(branco)
        pygame.draw.ellipse(self.image,cor,[0,0,largura,altura])
 
        self.rect = self.image.get_rect() 

class Jogador(pygame.sprite.Sprite):
    mudar_x=0
    mudar_y=0

    def __init__(self,x,y, filename):
        pygame.sprite.Sprite.__init__(self)
   
        self.image = pygame.image.load(filename).convert()

        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.anterior_x = x
        self.anterior_y = y

    def mudarvelocidade(self,x,y):
        self.mudar_x+=x
        self.mudar_y+=y

    def rotate(self, angulo):
      self.image = pygame.transform.rotate(self.image, 90)

    def atualizar(self,paredes,portao):
        antigo_x=self.rect.left
        novo_x=antigo_x+self.mudar_x
        anterior_x=antigo_x+self.anterior_x
        self.rect.left = novo_x
        
        antigo_y=self.rect.top
        novo_y=antigo_y+self.mudar_y
        anterior_y=antigo_y+self.anterior_y

        x_colisao = pygame.sprite.spritecollide(self, paredes, False)
        if x_colisao:
            self.rect.left=antigo_x
        else:
            self.rect.top = novo_y

            y_colisao = pygame.sprite.spritecollide(self, paredes, False)
            if y_colisao:
                self.rect.top=antigo_y

        if portao != False:
          gate_hit = pygame.sprite.spritecollide(self, portao, False)
          if gate_hit:
            self.rect.left=antigo_x
            self.rect.top=antigo_y

class Fantasma(Jogador):
    def mudarvelocidade(self,list,fantasma,virar,passos,l):
      try:
        z=list[virar][2]
        if passos < z:
          self.mudar_x=list[virar][0]
          self.mudar_y=list[virar][1]
          passos+=1
        else:
          if virar < l:
            virar+=1
          elif fantasma == "fantasminha":
            virar = 2
          else:
            virar = 0
          self.mudar_x=list[virar][0]
          self.mudar_y=list[virar][1]
          passos = 0
        return [virar,passos]
      except IndexError:
         return [0,0]

#definir movimentos dos fantasmas
direcoes = [
  [-30,0,2],
  [0,-15,4],
  [15,0,5],
  [0,15,7],
  [-15,0,11],
  [0,-15,7],
  [-15,0,3],
  [0,15,7],
  [-15,0,7],
  [0,15,15],
  [15,0,15],
  [0,-15,3],
  [-15,0,11],
  [0,-15,7],
  [15,0,3],
  [0,-15,11],
  [15,0,9],
]

pygame.init()

#configuracoes da tela
tela = pygame.display.set_mode([606, 606])

pygame.display.set_caption('Pacman')

background = pygame.Surface(tela.get_size())

background = background.convert()
  
background.fill(preto)

relogio = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

def iniciarJogo():

  lista_sprites = pygame.sprite.RenderPlain()

  lista_bola = pygame.sprite.RenderPlain()

  lista_monstros = pygame.sprite.RenderPlain()

  colisao_pacman = pygame.sprite.RenderPlain()

  lista_parede = iniciarFaseUm(lista_sprites)

  portao = iniciarPortao(lista_sprites)

  #Localizacao inicial dos personagens
  altura_pacman = 301 
  largura_pacman = 242 

  largura_fantasma = 400 
  altura_fantasma = 100 

  # Adiciona os personagens
  Pacman = Jogador( altura_pacman, largura_pacman, "persons/espiral.png" )
  lista_sprites.add(Pacman)
  colisao_pacman.add(Pacman)
   
  Fantasma1 = Fantasma( altura_fantasma, largura_fantasma, "persons/lucas-close.png" )
  lista_monstros.add(Fantasma1)
  lista_sprites.add(Fantasma1)

  Fantasma2 = Fantasma( altura_fantasma, largura_fantasma, "persons/lorena-close.png" )
  lista_monstros.add(Fantasma2)
  lista_sprites.add(Fantasma2)

  Fantasma3 = Fantasma( altura_fantasma, largura_fantasma, "persons/edef.png" )
  lista_monstros.add(Fantasma3)
  lista_sprites.add(Fantasma3)

  Fantasma4 = Fantasma( altura_fantasma, largura_fantasma, "persons/luigi-open.png" )
  lista_monstros.add(Fantasma4)
  lista_sprites.add(Fantasma4)

  Fantasma5 = Fantasma( altura_fantasma, largura_fantasma, "persons/mat.png" )
  lista_monstros.add(Fantasma5)
  lista_sprites.add(Fantasma5)

  Fantasma6 = Fantasma( altura_fantasma, largura_fantasma, "persons/mateus-close.png" )
  lista_monstros.add(Fantasma6)
  lista_sprites.add(Fantasma6)

  # Desenha a grade
  for linha in range(19):
      for coluna in range(19):
          if (linha == 7 or linha == 8) and (coluna == 8 or coluna == 9 or coluna == 10):
              continue
          else:
            bola = Bola(vermelho, 29, 29)

            # Seta um local aleatorio para o bloco
            bola.rect.x = (30*coluna+6)+26
            bola.rect.y = (30*linha+6)+26

            b_collide = pygame.sprite.spritecollide(bola, lista_parede, False)
            p_collide = pygame.sprite.spritecollide(bola, colisao_pacman, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Adiciona o bloco pra lista de objetos
              lista_bola.add(bola)
              lista_sprites.add(bola)

  pontuacao_maxima = len(lista_bola)

  pontos = 0

  finalizar = False

  i = 0

  while finalizar == False:
      Pacman.rotate(90)
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              finalizar=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.mudarvelocidade(-20,0)
                ##  Pacman.rotate(90)
              if event.key == pygame.K_RIGHT:
                  Pacman.mudarvelocidade(20,0)
                ##  Pacman.rotate(90)
              if event.key == pygame.K_UP:
                  Pacman.mudarvelocidade(0,-20)
                ##  Pacman.rotate(90)
              if event.key == pygame.K_DOWN:
                  Pacman.mudarvelocidade(0,20)
                ##  Pacman.rotate(90)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.mudarvelocidade(20,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.mudarvelocidade(-20,0)
              if event.key == pygame.K_UP:
                  Pacman.mudarvelocidade(0,20)
              if event.key == pygame.K_DOWN:
                  Pacman.mudarvelocidade(0,-20)
      
      Pacman.atualizar(lista_parede,portao)

      fantasma_virar = int(1 + (random.random() * 40)) #1 cima 2 direita 3 baixo 4 esquerda
      fantasma_passos = 10
      Fantasma1.mudarvelocidade(direcoes,"fantasminha",fantasma_virar,fantasma_passos,0)
      Fantasma1.atualizar(lista_parede,False)

      fantasma_virar = int(1 + (random.random() * 40)) #1 cima 2 direita 3 baixo 4 esquerda
      fantasma_passos = 0
      Fantasma2.mudarvelocidade(direcoes,"fantasminha",fantasma_virar,fantasma_passos,0)
      Fantasma2.atualizar(lista_parede,False)

      fantasma_virar = int(1 + (random.random() * 40)) #1 cima 2 direita 3 baixo 4 esquerda
      fantasma_passos = 0
      Fantasma3.mudarvelocidade(direcoes,"fantasminha",fantasma_virar,fantasma_passos,0)
      Fantasma3.atualizar(lista_parede,False)

      fantasma_virar = int(1 + (random.random() * 40)) #1 cima 2 direita 3 baixo 4 esquerda
      fantasma_passos = 0
      Fantasma4.mudarvelocidade(direcoes,"fantasminha",fantasma_virar,fantasma_passos,0)
      Fantasma4.atualizar(lista_parede,False)

      fantasma_virar = int(1 + (random.random() * 40)) #1 cima 2 direita 3 baixo 4 esquerda
      fantasma_passos = 0
      Fantasma5.mudarvelocidade(direcoes,"fantasminha",fantasma_virar,fantasma_passos,0)
      Fantasma5.atualizar(lista_parede,False)

      fantasma_virar = int(1 + (random.random() * 40)) #1 cima 2 direita 3 baixo 4 esquerda
      fantasma_passos = 0
      Fantasma6.mudarvelocidade(direcoes,"fantasminha",fantasma_virar,fantasma_passos,0)
      Fantasma6.atualizar(lista_parede,False)

      blocks_hit_list = pygame.sprite.spritecollide(Pacman, lista_bola, True)

      if len(blocks_hit_list) > 0:
          pontos +=len(blocks_hit_list)
      
      tela.fill(preto)
        
      lista_parede.draw(tela)
      portao.draw(tela)
      lista_sprites.draw(tela)
      lista_monstros.draw(tela)

      texto=font.render("Pontos: "+str(pontos)+"/"+str(pontuacao_maxima), True, azul)
      tela.blit(texto, [10, 10])

      if pontos == pontuacao_maxima:
        resultado("Parabens, voce venceu!",145,lista_sprites,lista_bola,lista_monstros,colisao_pacman,lista_parede,portao)

      monsta_hit_list = pygame.sprite.spritecollide(Pacman, lista_monstros, False)

      if monsta_hit_list:
        resultado("Game Over",235,lista_sprites,lista_bola,lista_monstros,colisao_pacman,lista_parede,portao)

      pygame.display.flip()
    
      relogio.tick(10)

def resultado(mensagem,left,lista_sprites,lista_bola,lista_monstros,colisao_pacman,lista_parede,portao):
  while True:
      # Processamento de eventos
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
          if event.key == pygame.K_RETURN:
            del lista_sprites
            del lista_bola
            del lista_monstros
            del colisao_pacman
            del lista_parede
            del portao
            iniciarJogo()

      altura_pacman = pygame.Surface((400,200)) 
      altura_pacman.set_alpha(10)                
      altura_pacman.fill((128,128,128))          
      tela.blit(altura_pacman, (100,200))    

      text1=font.render(mensagem, True, branco)
      tela.blit(text1, [left, 233])

      text2=font.render("Jogar novamente: ENTER.", True, branco)
      tela.blit(text2, [135, 303])
      text3=font.render("Sair: ESC.", True, branco)
      tela.blit(text3, [135, 333])

      pygame.display.flip()

      relogio.tick(10)

iniciarJogo()

pygame.quit()