from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, picture, x, y, width, hight):
        super().__init__()
        self.image=transform.scale(image.load(picture), (width, hight))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def __init__(self, picture, x, y, width, hight, xSpeed, ySpeed):
        super().__init__(picture, x, y, width, hight)
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
    def update(self):
        if (self.rect.x <= 620 and self.xSpeed > 0) or (self.rect.x >= 0 and self.xSpeed < 0):
            self.rect.x += self.xSpeed
        platformsTouched = sprite.spritecollide(self, bariers, False)
        if self.xSpeed > 0:
            for p in platformsTouched:
                self.rect.right = min(self.rect.right, p.rect.left)
        if self.xSpeed < 0:
            for p in platformsTouched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if (self.rect.y <= 410 and self.ySpeed > 0) or (self.rect.y >= 0 and self.ySpeed < 0):
            self.rect.y += self.ySpeed
        platformsTouched = sprite.spritecollide(self, bariers, False)
        if self.ySpeed > 0:
            for p in platformsTouched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        if self.ySpeed < 0:
            for p in platformsTouched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 50, 20)
        bullets.add(bullet)


class Enemy(GameSprite):
    def __init__(self, picture, x, y, width, hight, speed=5):
        super().__init__(picture, x, y, width, hight)
        self.speed = speed
        self.direction = 'left'
    def update(self):
        if self.rect.x <= 430:
            self.direction = 'left'
        if self.rect.x >= 600:
            self.direction = 'right'
        if self.direction == 'left':
            self.rect.x += self.speed
        if self.direction == 'right':
            self.rect.x -= self.speed

class Bullet(GameSprite):
    def __init__(self, picture, x, y, width, hight, speed=7):
        super().__init__(picture, x, y, width, hight)
        self.speed = speed
    def update(self):
        if self.rect.x >= 700:
            self.kill()
        self.rect.x += self.speed

color = (85, 67, 112)
window = display.set_mode((700, 500))
display.set_caption("Игра")
background = (119, 210, 223)

wall1 = GameSprite('wall.png', 340, 250, 80, 180)
wall2 = GameSprite('wall.png', 50, 200, 370, 100)
player = Player('hero.png', 10, 10, 50, 50, 0, 0)
monster = Enemy("monster.png", 620, 180, 80, 80)
final = GameSprite("final.png", 620, 420, 80, 80)

monsters = sprite.Group()
monsters.add(monster)

bullets = sprite.Group()

bariers = sprite.Group()
bariers.add(wall1)
bariers.add(wall2)

play = True
finish = False



while play:
    for e in event.get():
        if e.type == QUIT:
            play = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_LEFT:
               player.xSpeed = -5
            elif e.key == K_RIGHT:
               player.xSpeed = 5
            elif e.key == K_UP:
               player.ySpeed = -5
            elif e.key == K_DOWN:
               player.ySpeed = 5
        elif e.type == KEYUP:
            if e.key == K_LEFT:
               player.xSpeed = 0
            elif e.key == K_RIGHT:
               player.xSpeed = 0
            elif e.key == K_UP:
               player.ySpeed = 0
            elif e.key == K_DOWN:
                player.ySpeed = 0
    if not finish:
        window.fill(background)

        player.update()

        bullets.draw(window)
        bariers.draw(window)

        bullets.update()
        monsters.update()
        monsters.draw(window)
        player.reset()
        final.reset()

        bulletsTouchWall = sprite.groupcollide(bariers, bullets, False, True)
        bulletsTouchedMonster = sprite.groupcollide(monsters, bullets, True, True)

        if sprite.collide_rect(player, monster):
            finish = True
            font.init()

            lose = font.SysFont('Arial', 70).render('YOU LOSE!', True, (255, 0, 0))
            window.blit(lose, (200, 200))

        elif sprite.collide_rect(player, final):
            finish = True
            font.init()

            win = font.SysFont("Arial", 70).render('YOU WIN!', True, (0, 255, 0))
            window.blit(win, (200, 200))
            
    
    display.update()
    time.delay(40)