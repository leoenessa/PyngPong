import sys
import pygame
import subprocess

def validador(ip):
    octetos=[]
    oct_tmp = ''
    for ch in ip:
        if(ch=='.'):
            try:
                octetos.append(int(oct_tmp))
                oct_tmp=''
            except Exception:
                print("PyngPong Erro - IP entrado nao e valido")
                pygame.quit()
                sys.exit()
        else:
            oct_tmp+=ch
    octetos.append(int(oct_tmp))
    
    if(len(octetos)!=4):
        return(False)
    for octeto in octetos:
        if(octeto>255 or octeto<1):
            return(False)
    return(True)                  
            
BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()

screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("PyngPong Player 2")

fontrender = pygame.font.SysFont("Sans Serif",34)
text = fontrender.render("Entre com o IP do Player 1",1,WHITE,None)
text_width,text_height = text.get_size()
borda_rect = pygame.Rect(640/4,480/2,text_width,text_height+10)
ip = ''

running= True

while(running):
    
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                subprocess.Popen("python Menu.Py")
                pygame.quit()
                sys.exit()
            elif(event.key >=pygame.K_0 and event.key<=pygame.K_9):
                ch = chr(event.key)
                ip+=ch
            elif(event.key == pygame.K_PERIOD):
                ip+='.'
            elif(event.key == pygame.K_BACKSPACE):
                ip = ip[:-1]
            elif(event.key == pygame.K_RETURN):
                if(validador(ip)):
                    subprocess.Popen("python PongMPClient.py %s"%(ip))
                    pygame.quit()
                    sys.exit()
                else:
                    pass
            elif(event.key == pygame.K_RIGHT):
                pass
            
    ip_text = fontrender.render(ip, 1, WHITE, None) 
    
    screen.fill(BLACK)
    screen.blit(text,((640/2-text_width/2),480/3))
    pygame.draw.rect(screen, WHITE, borda_rect, 1)
    screen.blit(ip_text,(640/4+10,480/2+10))
    pygame.display.update()