import pygame 
import sys
from random import Random

bgfile = 'tennis.bmp'
ppballfile = 'ppball.gif'

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
        
        if(self.rect.y>=455 or self.rect.y<=25):
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
                 
                print("rebatidas:%i | speed:%i"%(self.qtde_rebatidas,self.speed))
        
        resultx = self.directionx * 20 * self.speed
        resulty = self.directiony * 5 * self.speed
        self.rect.x +=resultx
        self.rect.y +=resulty
        
class Player(object):
    
    def __init__(self,tipo):

        if(tipo==1):
            self.rect = pygame.Rect(0,200,24,80)
                                
        if(tipo==2):
            self.rect = pygame.Rect(616,200,24,80)
        else:
            pass
        players.append(self)
    
    def move(self,dy):
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
    
running = True
WHITE = (255,255,255)
RED = (255,0,0)
FPS = 60
players = []

pygame.init()
window = pygame.display.set_mode((640, 480))

player1 = Player(1)
player2 = Player(2)
ball = Ball()
random = Random()
clock = pygame.time.Clock()
my_font = pygame.font.SysFont("arial", 16)
Texto = my_font.render("Press SPACE to start", True, (0,0,0), None)

background = pygame.image.load_basic(bgfile).convert()
last = pygame.time.get_ticks()    
                        
while(running):
    
    clock.tick(FPS)
    
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
    
    if(key[pygame.K_UP]):
        player1.move(-10)
    if(key[pygame.K_DOWN]):
        player1.move(10)
    if(key[pygame.K_w]):
        player2.move(-10)
    if(key[pygame.K_s]):
        player2.move(10)
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
    pygame.display.set_caption("Pyng Pong - Sofia, We love You! FPS:%i"%(clock.get_fps()))
    
pygame.quit()
sys.exit()