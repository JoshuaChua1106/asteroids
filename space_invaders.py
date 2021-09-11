import constants
import pygame
import random
from pygame.locals import *

class GameEntity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Player(GameEntity):

    playerSizeHeight = 15
    playerSizeWidth = 35
    frames = 0
    shooting = False

    def __init__(self, x, y, gameDisplay):
        self.rect = Rect(x-(self.playerSizeWidth/2), y, self.playerSizeWidth, self.playerSizeHeight)
        self.gameDisplay = gameDisplay    

    def update(self, pressed_keys):
        self.printPlayer()
        self.boundaries()

        if pressed_keys[K_RIGHT]:
            if self.frames == 0:
                self.frames = 2
                self.rect.move_ip(1,0)
        if pressed_keys[K_LEFT]:
            if self.frames == 0:
                self.frames = 2
                self.rect.move_ip(-1,0)
        if pressed_keys[K_UP]:
            if self.frames == 0:
                self.frames = 2
                self.rect.move_ip(0,-1)
        if pressed_keys[K_DOWN]:
            if self.frames == 0:
                self.frames = 2
                self.rect.move_ip(0,1)

        if self.frames > 0:
            self.frames -= 1


    def printPlayer(self):
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), self.rect)


    def boundaries(self):
        if self.rect.right < 0:
            self.rect.right = constants.WINDOW_LENGTH
        if self.rect.left > constants.WINDOW_LENGTH:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > constants.WINDOW_HEIGHT:
            self.rect.bottom = constants.WINDOW_HEIGHT

    def getXCentre(self):
        return (self.rect.left + self.rect.right)/2
    
    def getYCentre(self):
        return (self.rect.top + self.rect.bottom)/2

    def shoot(self, bullet_list):
        bullet = Bullet(self.getXCentre(), self.getYCentre(), self.gameDisplay)
        bullet_list.append(bullet)
        

class Asteroid(GameEntity):

    asteroidWidth = 40
    asteroidHeight = 40

    x = 0
    y = 0

    frames = 0

    def __init__(self, x, y, gameDisplay):
        self.rect = Rect(x, y, self.asteroidWidth, self.asteroidHeight)
        self.x = x
        self.y = y
        self.gameDisplay = gameDisplay  

    def printAsteroid(self):
        pygame.draw.rect(self.gameDisplay, (255, 255, 0), self.rect)

    def update(self, asteroid_list):
        self.printAsteroid()
        if self.frames == 0:
            self.frames = 20
            self.rect.move_ip(0,1)
            self.y += 1

        if self.frames > 0:
            self.frames -= 1

        if self.y > 500:
            asteroid_list.remove(self)
        

    def spawnAsteroid(self, time, asteroid_list):
        if time % 5 == 0:
            new_asteroid = Asteroid(random.randrange(10, 450), -40, self.gameDisplay)
            asteroid_list.append(new_asteroid)
        

class Bullet(GameEntity):

    radius = 5

    # x,y for centre of circle
    x = 0
    y = 0
    frames = 0

    def __init__(self, x, y, gameDisplay):
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2) #left, top, width, height
        self.gameDisplay = gameDisplay
        self.x = x
        self.y = y   
    
    def printBullet(self):
        pygame.draw.circle(self.gameDisplay, (255, 0, 0), (self.x, self.y), self.radius)

    def update(self, bullet_list):
        self.printBullet()
        if self.frames == 0:
            self.frames = 2
            self.rect.move_ip(0,-1)
            self.y -= 1

        if self.frames > 0:
            self.frames -= 1

        if self.y < 0:
            bullet_list.remove(self)

            
    
    


def main():
    pygame.init()

    

    gameDisplay = pygame.display.set_mode([constants.WINDOW_LENGTH, constants.WINDOW_HEIGHT])
     
    player = Player(constants.WINDOW_LENGTH/2, (constants.WINDOW_HEIGHT*4)/5, gameDisplay)
    running = True

    bullet_list = []
    asteroid_list = []

    time = 0

    while running:

        events = pygame.event.get()
        gameDisplay.fill((0, 0, 0))

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False
                if e.key == K_SPACE:
                    # isShooting = True
                    player.shoot(bullet_list)

            elif e.type == QUIT:
                running = False
            

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        if time % 4000 == 0:
            new_asteroid = Asteroid(random.randrange(10, 450), -40, gameDisplay)
            asteroid_list.append(new_asteroid)
        
        for bullet in bullet_list:
            bullet.update(bullet_list)

        for asteroid in asteroid_list:
            asteroid.update(asteroid_list)

    

        time += 1
        pygame.display.flip()


    pygame.quit()   

if __name__ == "__main__":
    main()



