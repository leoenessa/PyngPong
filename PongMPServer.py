import pygame 
import sys
from random import Random
import socket
import select

bgfile = 'tennis.bmp'
ppballfile = 'ppball.gif'
HOSTSERVER = '' #No codigo, HOSTSERVER e incializado com endereco do player2
HOSTCLIENT = socket.gethostbyname(socket.gethostname())
PORTSERVER = 8766
PORTCLIENT = 8765

class Ball(object):
    
    ballmove = False
    qtde_rebatidas = 0
    speed = 1
    
    directionx = -1
    directiony = 1 
    
    def __init__(self):
                
        self.imagembola = pygame.image.load(ppballfile).convert_alpha()
        self.rect = self.imagembola.get_rect()
        self.rect = pygame.Rect(307,227,25,25)
        
        
    def start(self,directionx,directiony):
        self.ballmove = True
        self.directionx = directionx
        self.directiony = directiony
            
    def roll(self):
        
        if(self.rect.x<=5 or self.rect.x>=620):
            global running
            running = False
        
        if(self.rect.y>=455 or self.rect.y<=10):
            self.directiony *=-1    
        
        for player in players:
            if(self.rect.colliderect(player.rect)):
                self.directionx *= -1
                self.qtde_rebatidas+=1
                
                if(self.qtde_rebatidas%5==0): pass#self.speed+=0.25
                
                if(self.rect.y>=player.rect.y and self.rect.y<player.rect.y+40):
                    if(self.directiony>0):
                        self.directiony*=-1
                    else:
                        pass
                elif(self.rect.y>player.rect.y+41 and self.rect.y<=player.rect.y+80):
                    if(self.directiony>0):
                        pass
                    else:
                        self.directiony*=-1
                else:
                    pass
                 
                print("rebatidas:%i | speed:%i\nbola x:%i | bola y:%i"%(self.qtde_rebatidas,self.speed,self.rect.x,self.rect.y))
        
        resultx = self.directionx * 20 * self.speed
        resulty = self.directiony * 5 * self.speed
        self.rect.x +=resultx
        self.rect.y +=resulty
        data = str("ball:%s:%s:"%(str(self.rect.x),str(self.rect.y)))
        out_socket.sendall(data.encode('ascii'))
        
class Player(object):
    
    def __init__(self,tipo):

        if(tipo==1):
            self.rect = pygame.Rect(0,200,24,80)
                                
        if(tipo==2):
            self.rect = pygame.Rect(616,200,24,80)
        else:
            pass
        players.append(self)
    
    def move(self,dy,caller):
        global out_socket
        
        if(dy>0):
            if(self.rect.y>=400):
                pass
            else:
                self.rect.y +=dy
                
        if(dy<0):
            if(self.rect.y<=0):
                pass
            else:
                self.rect.y +=dy
        if(caller=='self'):
            data = str("player:0:%s"%(str(dy)))
            out_socket.sendall(data.encode('ascii'))
          
running = True
WHITE = (255,255,255)
RED = (255,0,0)
FPS = 60
players = []
read_sockets = []

pygame.init()
window = pygame.display.set_mode((640, 480))

try:
        
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOSTCLIENT,PORTCLIENT))
    s.listen(1)
    print("Esperando Player 2 em %s:%i"%(HOSTCLIENT,PORTCLIENT))
    s.settimeout(10)
    out_socket,addr = s.accept()
    print("Oponente Conectado: %s:%i"%(addr[0],addr[1]))
    
    HOSTSERVER = addr[0]
    in_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    in_socket.setblocking(1)
    in_socket.connect((HOSTSERVER,PORTSERVER))
        
except socket.error as e:
    print("PyngPong Erro:"+str(e))

player1 = Player(1)
player2 = Player(2)
ball = Ball()
random = Random()

clock = pygame.time.Clock()

background = pygame.image.load_basic(bgfile).convert()

last = pygame.time.get_ticks()    

read_sockets.append(in_socket)
                        
while(running):
       
    clock.tick(FPS)
    
    now = pygame.time.get_ticks()
    
    readable,writable,erroned = select.select(read_sockets, [], [],0.001)
    
    for s in readable:
        if s is in_socket:
            data = in_socket.recv(64)
            data = int(data.decode('ascii'))
            player2.move(data,'net')
        else:
            pass
           
    if(now-last>50 and ball.ballmove):
        ball.roll()
        last=now
    
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        if(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    
    key = pygame.key.get_pressed()
    
    if(key[pygame.K_UP]):
        player1.move(-10,'self')
    if(key[pygame.K_DOWN]):
        player1.move(10,'self')
    if(key[pygame.K_SPACE]):
        if(not ball.ballmove):
            ball.start(random.choice([-1,1]),random.choice([-1,1]))
        else:
            pass
        
    pygame.display.flip()
    window.blit(background,(0,0))
    window.blit(ball.imagembola,ball.rect)
    pygame.draw.rect(window, WHITE, player1.rect)
    pygame.draw.rect(window, WHITE, player2.rect)    
    pygame.display.set_caption("Pyng Pong Player 1 - Sofia, We love You! FPS:%i"%(clock.get_fps()))
    pygame.display.update(None)
    
pygame.quit()
in_socket.close()
out_socket.close()
s.close()
sys.exit()