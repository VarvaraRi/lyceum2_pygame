import pygame
import random

pygame.init()
fps = 50
size = (width, height) = (600, 400)
clock = pygame.time.Clock()
black = (0,0,0)
white = (255,255,255)
blue = (0, 0, 225)
screen = pygame.display.set_mode(size)

def start_screen():
    intro_text = ["PingPong", "",
                  "Правила игры",
                  "1)Вы должны отбивать мячик",
                  "2)Забивайте мячик своему апоненту",
                  "3)Заработайте как можно больше очков"]
    image =  pygame.image.load("fon.png")
    fon = pygame.transform.scale(image, (width, height))
    screen.blit(fon, (0, 0))
    text_coord = 300
    text_coordy = 50
    for line in intro_text:
        textdisp(line, 25, text_coord, text_coordy, black)
        text_coordy += 30

def textdisp(text,fontsize,x,y,color):
    font = pygame.font.SysFont('-', fontsize, True, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)

def iipmove(iip,ball):
    if ball.move[0] > 0:
        if ball.rect.bottom > iip.rect.bottom + iip.rect.height / 5:
           iip.move[1] = 7
        elif ball.rect.top < iip.rect.top - iip.rect.height / 5:
            iip.move[1] = -7
        else:
            iip.move[1] = 0
    else:
        iip.move[1] = 0

class Paddle(pygame.sprite.Sprite):
    def __init__(self,x,y,sizex,sizey,color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey
        self.color = color
        self.image = pygame.Surface((sizex,sizey),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        pygame.draw.rect(self.image,self.color,(0,0,sizex,sizey))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.points = 0
        self.move = [0,0]

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    def update(self):
        self.rect = self.rect.move(self.move)
        self.checkbounds()

    def draw(self):
        screen.blit(self.image,self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,size,color,move=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.move = move
        self.image = pygame.Surface((size,size),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image,self.color,(int(self.rect.width/2),int(self.rect.height/2)),int(size/2))
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10
        self.score = 0

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    def update(self):
        if self.rect.top == 0 or self.rect.bottom == height:
            self.move[1] = -1*self.move[1]
        if self.rect.left == 0:
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.move = [random.randrange(-1,2,2)*4,random.randrange(-1,2,2)*4]
            self.score = 1
        if self.rect.right == width:
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.move = [random.randrange(-1,2,2)*4,random.randrange(-1,2,2)*4]
            self.score = -1
        self.rect = self.rect.move(self.move)
        self.checkbounds()

    def draw(self):
        pygame.draw.circle(self.image, self.color, (int(self.rect.width / 2), int(self.rect.height / 2)), int(self.size / 2))
        screen.blit(self.image, self.rect)
start = True
running = True
paddle = Paddle(width/10,height/2,width/60,height/8,white)
iip = Paddle(width - width/10,height/2,width/60,height/8,white)
ball = Ball(width/2,height/2,20,blue,[4,4])
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle.move[1] = -7
            elif event.key == pygame.K_DOWN:
                paddle.move[1] = 7
        if event.type == pygame.KEYUP:
            paddle.move[1] = 0
        if event.type == pygame.MOUSEBUTTONUP:
            start = False
    if start is True:
        start_screen()
    else:
        screen.fill(black)
        iipmove(iip, ball)
        paddle.draw()
        iip.draw()
        ball.draw()
        textdisp(str(paddle.points), 30, width / 8, 25, (255, 0, 0))
        textdisp(str(iip.points), 30, width - width / 8, 25, (255, 0, 0))

        if pygame.sprite.collide_mask(paddle, ball):
            ball.move[0] = -1 * ball.move[0]
            ball.move[1] = ball.move[1] - int(0.1 * random.randrange(5, 10) * paddle.move[1])
            if ball.move[1] > ball.speed:
                ball.move[1] = ball.speed
            if ball.move[1] < -1 * ball.speed:
                ball.move[1] = -1 * ball.speed
        if pygame.sprite.collide_mask(iip, ball):
            ball.move[0] = -1 * ball.move[0]
            ball.move[1] = ball.move[1] - int(0.1 * random.randrange(5, 10) * iip.move[1])
            if ball.move[1] > ball.speed:
                ball.move[1] = ball.speed
            if ball.move[1] < -1 * ball.speed:
                ball.move[1] = -1 * ball.speed

        if ball.score == 1:
            iip.points += 1
            ball.score = 0
        elif ball.score == -1:
            paddle.points += 1
            ball.score = 0

        paddle.update()
        ball.update()
        iip.update()

    pygame.display.update()
    clock.tick(fps)
pygame.quit()
quit()
