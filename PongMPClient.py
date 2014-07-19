import pygame 
import sys
from random import Random
import socket
import select
import errno

bgfile = 'tennis.bmp'
ppballfile = 'ppball.gif'
HOSTSERVER = '127.0.0.1'
HOSTCLIENT = 'localhost' 
PORTSERVER = 8765
PORTCLIENT = 8766

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
                
                if(self.qtde_rebatidas%5==0): self.speed+=0.25
                
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
        
    def setPostition(self,dx,dy):
        self.rect.x = dx
        self.rect.y = dy
        
        
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
        global conn
             
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
            data = str(dy)
            conn.sendall(data.encode('ascii'))
        
running = True
WHITE = (255,255,255)
RED = (255,0,0)
FPS = 60
players = []
read_sockets = []

try:
    in_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    in_socket.setblocking(1)
    in_socket.connect((HOSTSERVER,PORTSERVER))
    
    out_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    out_socket.setblocking(1)
    out_socket.bind((HOSTCLIENT,PORTCLIENT))
    out_socket.listen(1)
    
    conn,addr=out_socket.accept()
    conn.setblocking(1)
except socket.error as e:
    print("Deu erro criando out socket "+str(e))

pygame.init()
window = pygame.display.set_mode((640, 480))

player1 = Player(1)
player2 = Player(2)
ball = Ball()
random = Random()

clock = pygame.time.Clock()

background = pygame.image.load_basic(bgfile).convert()

last = pygame.time.get_ticks()    

read_sockets.append(in_socket)
read_sockets.append(out_socket)
                        
while(running):
            
    clock.tick(FPS)
    
    readable,writable,erroned = select.select(read_sockets, [],[],0.001)
    for s in readable:
        if s is in_socket:
            try:
                data = in_socket.recv(64)
                (objeto,dx,dy) = data.decode('ascii').split(':')
                dx=int(dx)
                dy=int(dy)
                if(objeto=='player'):
                    player1.move(dy,'net')
                elif(objeto=='ball'):
                    ball.setPostition(dx, dy)
                else:
                    pass
                
            except socket.error as e:
                if(e.args[0] == errno.EWOULDBLOCK):
                    pass
            except ValueError as ve:
                print(ve)
                print(data)
        else:
            pass
    
    now = pygame.time.get_ticks()
    
    if(now-last>50 and ball.ballmove):
        ball.roll()
        last=now
    
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        if(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    
    key = pygame.key.get_pressed()
   
    if(key[pygame.K_w]):
        player2.move(-10,'self')
    if(key[pygame.K_s]):
        player2.move(10,'self')
   
    pygame.display.flip()
    window.blit(background,(0,0))
    window.blit(ball.imagembola,ball.rect)
    pygame.draw.rect(window, WHITE, player1.rect)
    pygame.draw.rect(window, WHITE, player2.rect)    
    pygame.display.set_caption("Pyng Pong Player 2 - Sofia, We love You! FPS:%i"%(clock.get_fps()))
    pygame.display.update(None)
    
pygame.quit()
out_socket.close()
in_socket.close()
conn.close()
sys.exit()