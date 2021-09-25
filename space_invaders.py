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
    shooting_level2 = False
    shooting_level3 = False
    shootingCooldown = False

    current_shooting_level = 1

    time = 0

    def __init__(self, x, y, gameDisplay):
        self.rect = Rect(x-(self.playerSizeWidth/2), y, self.playerSizeWidth, self.playerSizeHeight)
        self.gameDisplay = gameDisplay    

    def update(self, pressed_keys, bullet_list):
        self.printPlayer()
        self.boundaries()

        # Moving
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


        # Shooting
        if pressed_keys[K_SPACE] and self.shootingCooldown == False:
            self.shootingCooldown = True
            self.shoot(bullet_list)

            # If upgrades are activated
            if self.shooting_level2:
                self.shootlvl2(bullet_list)
        
            if self.shooting_level3:
                self.shootlvl3(bullet_list)

        if self.shootingCooldown:
            self.time += 1
        
        if self.time == 300:
            self.time = 0
            self.shootingCooldown = False

        

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
    
    def shootlvl2(self, bullet_list):
        bullet = Bullet(self.getXCentre()-(self.playerSizeWidth/3), self.getYCentre(), self.gameDisplay)
        bullet_list.append(bullet)
    
    def shootlvl3(self, bullet_list):
        bullet = Bullet(self.getXCentre()+(self.playerSizeWidth/3), self.getYCentre(), self.gameDisplay)
        bullet_list.append(bullet)

    def setshootlevel(self, level):
        if level == 2:
            self.shooting_level2 = True
            self.current_shooting_level = 2
        if level == 3:
            self.shooting_level3 = True
            self.current_shooting_level = 3

    def getShootingLevel(self):
        return self.current_shooting_level
    

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

    def update(self, asteroid_list, rect_list):
        self.printAsteroid()
        if self.frames == 0:
            self.frames = 20
            self.rect.move_ip(0,1)
            self.y += 1

        if self.frames > 0:
            self.frames -= 1

        if self.y > 500:
            asteroid_list.remove(self)
            rect_list.remove(self)

    def spawnAsteroid(self, time, asteroid_list):
        if time % 5 == 0:
            new_asteroid = Asteroid(random.randrange(10, 450), -40, self.gameDisplay)
            asteroid_list.append(new_asteroid)
    
    def getRect(self):
        return self.rect
        

class Bullet(GameEntity):

    radius = 5

    # x,y for centre of circle
    x = 0
    y = 0
    frames = 0

    def __init__(self, x, y, gameDisplay):
        self.x = x
        self.y = y  
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2) #left, top, width, height
        self.gameDisplay = gameDisplay
         
    
    def printBullet(self):
        pygame.draw.circle(self.gameDisplay, (255, 0, 0), (self.x, self.y), self.radius)

    def update(self, bullet_list, rect_list, asteroid_list):
        self.printBullet()
        if self.frames == 0:
            self.frames = 2
            self.rect.move_ip(0,-1)
            self.y -= 1

        if self.frames > 0:
            self.frames -= 1

        if self.y < 0:
            bullet_list.remove(self)


    def getRect(self):
        return self.rect

    def collision(self, rect_list):
        return self.rect.collidelist(rect_list)
           


class Collisions():

    @staticmethod
    def collide(bullet, bullet_list, rect_list, asteroid_list, score):
        collision_index = bullet.collision(rect_list)
        if collision_index != -1:
            bullet_list.remove(bullet)
            rect_list.pop(collision_index)
            asteroid_list.pop(collision_index)

            score.updateTotal()
        

class Score():

    total = 0
    increment = 1

    def __init__(self, total, font):
        self.total = total
        self.font = font

    def getTotal(self):
        return self.total

    def setTotal(self, total):
        self.total = total

    def updateTotal(self):
        self.total += self.increment
    
    def printScore(self, gameDisplay):
        text = self.font.render(str(self.total), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (200, 200) 
        gameDisplay.blit(text, textRect)

    def updateIncrement(self, new_inc):
        self.increment += new_inc


class Shop():
    
    @staticmethod
    def upgradeShooting(self, player):
        pass


    
    


def main():
    pygame.init()

    font = pygame.font.Font('freesansbold.ttf', 13) 


    gameDisplay = pygame.display.set_mode([constants.WINDOW_LENGTH, constants.WINDOW_HEIGHT])
     
    player = Player(constants.WINDOW_LENGTH/2, (constants.WINDOW_HEIGHT*4)/5, gameDisplay)
    running = True

    score = Score(0, font)

    bullet_list = []
    asteroid_list = []
    rect_list = []

    time = 0

    while running:

        events = pygame.event.get()
        gameDisplay.fill((0, 0, 0))

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False
                # if e.key == K_SPACE:
                #     # isShooting = True
                #     player.shoot(bullet_list)
                if e.key == K_1 and score.getTotal() >= 2:
                    score.setTotal(score.getTotal()-2)
                    score.updateIncrement(1)

                if e.key == K_2 and player.getShootingLevel() != 3 and score.getTotal() >= 20:
                    score.setTotal(score.getTotal()-20)
                    if player.getShootingLevel() == 2:
                        player.setshootlevel(3)

                    if player.getShootingLevel() == 1:
                        player.setshootlevel(2)
                    
                        
                if e.key == K_3:
                    print(player.shooting_level3)


            elif e.type == QUIT:
                running = False
            

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys, bullet_list)

        if time % 4000 == 0:
            new_asteroid = Asteroid(random.randrange(10, 450), -40, gameDisplay)
            asteroid_list.append(new_asteroid)
            rect_list.append(new_asteroid.getRect())
        
        

        for bullet in bullet_list:
            bullet.update(bullet_list, rect_list, asteroid_list)
            Collisions.collide(bullet, bullet_list, rect_list, asteroid_list, score)
            
        for asteroid in asteroid_list:
            asteroid.update(asteroid_list, rect_list)
            
        
        score.printScore(gameDisplay)

        time += 1
        pygame.display.flip()


    pygame.quit()   

if __name__ == "__main__":
    main()



