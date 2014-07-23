import pygame
import sys
import subprocess

class BreakIt(Exception): pass
class Menu(object):
        altura = 0
        posicao_opcao_1 = 0
        
        def drawOptions(self,lista,screen): #retorna um surface com o menu inserido
            myfont = pygame.font.SysFont("Sans Serif", 34)
            opcoes_lista = []
            qtde = 0
            posicao_y_atual = 0
    
            for item in lista:
                print(item)
                opcoes_lista.append(myfont.render(item,1,(255,255,255)))
                qtde+=1
    
            for opcao in opcoes_lista:
                x,y = opcao.get_size()
                self.altura += 10+y
                posicao_y_atual = (480-self.altura)/2
                self.posicao_opcao_1 = posicao_y_atual
                
            for opcao in opcoes_lista:
                x,y = opcao.get_size()
                screen.blit(opcao,(640/2-x/2,posicao_y_atual))
                posicao_y_atual+=y+10
            
            altura_por_item = (self.altura-10*qtde)/qtde  
                 
            #print("quantidade:%i\naltura total:%i\naltura opcao:%i"%(qtde,self.altura,altura_por_item))
                        
            return(screen,self.posicao_opcao_1,altura_por_item)

class ChRect(object):
    posicaoAtual=1
    numOpcoes = 0
    posProxItem = 0
    
    def __init__(self,dy,altura,numOpcoes):
        self.rect = pygame.Rect(640/4,dy,300,altura)
        self.posProxItem = altura+10
        self.numOpcoes = numOpcoes
    def moveDown(self):
        if(self.posicaoAtual>=self.numOpcoes):
            pass
        else:
            self.rect.y+= self.posProxItem
            self.posicaoAtual+=1
            print(self.rect.y)
        
    def moveUp(self):
        if(self.posicaoAtual<=1):
            pass
        else:
            self.rect.y-=self.posProxItem-1
            self.posicaoAtual-=1
            print(self.rect.y)
    
    def getPosicao(self):
        return(self.posicaoAtual)
    
running = True
menu_choice = 0

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pyng Pong MENU - Sofia we Love you!")

menu = Menu()
opcoes_menu = ["Um Jogador","Multi Jogador vs PC","Multi Jogador Criar","Multi Jogador Entrar","SAIR"]

menu_surface = pygame.Surface((640,480))
menu_surface.fill((0,0,0))
menu_surface.set_colorkey((0,0,0))
menu_surface.set_alpha(100)

menu_surface,posicao1,alturadoitem = menu.drawOptions(opcoes_menu,menu_surface)

chRec = ChRect(posicao1, alturadoitem, len(opcoes_menu))

try:
    while(running):
        for e in pygame.event.get():
            if(e.type == pygame.QUIT):
                running = False
                break
            if(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
                break

            key = pygame.key.get_pressed()
        
            if(key[pygame.K_UP]):
                chRec.moveUp()
            if(key[pygame.K_DOWN]):
                chRec.moveDown()
            if(key[pygame.K_RETURN]):
                print(chRec.posicaoAtual)
                menu_choice = chRec.getPosicao()
                raise BreakIt
            
        screen.fill((0,0,0))
        pygame.draw.rect(screen,(125,33,44), chRec)
        screen.blit(menu_surface,(0,0))
        pygame.display.flip()     
except BreakIt as bi:pass

if(menu_choice):
    if(menu_choice==1):
        subprocess.Popen("python PongSP.py")
    elif(menu_choice==2):
        pass
    elif(menu_choice==3):
        subprocess.Popen("python PongMPServer.py")
    elif(menu_choice==4):
        subprocess.Popen("python PongMPClient.py")
    else:
        pass
    
pygame.quit()
sys.exit()