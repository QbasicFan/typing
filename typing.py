#Typing game

import pygame 
import random
from urllib import request
import json

r = request.urlopen("https://www.mcatmom.com/api/?")
pygame.font.init() 
pygame.init()

myfont = pygame.font.SysFont('Comic Sans MS', 40)

screen_width  = 500
screen_height  = 270

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Typing game")

clock = pygame.time.Clock()
FPS = 60


words = []
data = r.read()
d = json.loads(data)
v = d[0]
for j in d:
    a = j["title"]
    if not("paused" in a):
        words.append(a.strip())

text = words[random.randrange(0,len(words))]

score = 0

#image 
bg = pygame.image.load('Background_2.png').convert_alpha()

textsurface = myfont.render('You Win. (q) = Quit , (r) restart', False, (0, 0, 0))
textmask = myfont.render(text, False, (200,20, 50))
pts = myfont.render(str(score), False, (200,220, 150))


RED = (255,150,50)


class parts:
    def __init__(self,x,y):
        self.x = (x+35) - random.randrange(10,30)
        self.y = (y+20) - random.randrange(10,30)
        self.size = random.randrange(20,40)
        self.dx = random.randrange(1,10) - 5
        self.dy = random.randrange(1,10) - 5
        self.pop = False

    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        self.size -=1 
        if self.size < 2:
            self.pop = True    

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.size, 0)


parti = []

def make_parts(x,y):
    for i in range(10):        
        parti.append(parts(x,y))



PARTICLE_EVENT = pygame.USEREVENT + 1

run = True

while run:

    clock.tick(FPS)
    screen.blit(bg, (0,0))

    #screen.blit(textsurface,(200,200))
    screen.blit(myfont.render(text, False, (200,20, 50)),(200,200))
    screen.blit(myfont.render(str(score), False, (200,220, 150)),(100,100))


    random_color = (random.randrange(0, 254), random.randrange(0, 254), random.randrange(0, 254))
    random_pos = (random.randrange(0, screen_width), random.randrange(0, screen_height))
    random_radius = random.randrange(2,20)
    
    idx = 0
    for i in parti:
        i.move()
        if i.pop:
            parti.pop(idx)
        else:        
            i.draw()
        idx +=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if len(text) ==0 and  pygame.key.get_pressed()[pygame.K_q] == 1:
            run = False
        if len(text) == 0 and pygame.key.get_pressed()[pygame.K_r] == 1:
            text = words[random.randrange(1,len(words))]
        if event.type == pygame.KEYDOWN:
            
            k = pygame.key.name(event.key)

            if k in text[0]:
                text = text.replace(k,'',1)
                score +=1
                make_parts(200,200)
            else:
                score -=1
            print(k ,"", text,"*",len(text))

    if len(text) == 0:
        screen.blit(textsurface,(20,200))
        
    #update
    pygame.display.update()

pygame.quit()
