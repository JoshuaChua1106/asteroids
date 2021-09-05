import pygame
from pygame.locals import *

class GameEntity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Player(GameEntity):

    playerSizeHeight = 15
    playerSizeWidth = 35

    def __init__(self, x, y):
        self.rect = Rect(x-(self.playerSizeWidth/2), y, Player.playerSizeWidth, Player.playerSizeHeight)    

    def update(self, pressed_keys):
        self.printPlayer()
        self.boundaries()
        if pressed_keys[K_RIGHT]:
                self.rect.move_ip(1,0)
        elif pressed_keys[K_LEFT]:
                self.rect.move_ip(-1,0)
        elif pressed_keys[K_UP]:
                self.rect.move_ip(0,-1)
        elif pressed_keys[K_DOWN]:
                self.rect.move_ip(0,1)


    def printPlayer(self):
        pygame.draw.rect(gameDisplay, (255, 0, 0), self.rect)

    def boundaries(self):
        if self.rect.left < 0:
            self.rect.right = windowLength
        if self.rect.right > windowLength:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > windowHeight:
            self.rect.bottom = windowHeight


class Asteroid(GameEntity):
    def __init__(self, x, y):
        super().__init__(x, y)

class Bullet(GameEntity):
    def __init__(self, x, y):
        super().__init__(x, y)


pygame.init()

windowHeight = 500
windowLength = 500

gameDisplay = pygame.display.set_mode([windowLength,windowHeight])

player = Player(windowLength/2, (windowHeight*4)/5)


running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            

        elif event.type == QUIT:
            running = False

        
    pressed_keys = pygame.key.get_pressed()

    gameDisplay.fill((0, 0, 0))
    player.update(pressed_keys)

    pygame.display.flip()


pygame.quit()   




