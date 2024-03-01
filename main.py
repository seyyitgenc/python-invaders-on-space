import pygame as pg
from enum import Enum

# TODO: later on can add sprite size. for preinitialized sprite sheet

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

PLAYER_PADDING_BOTTOM = 40 
PLAYER_SIZEX = 96
PLAYER_SIZEY = 24

ENEMY_PADDING = 10
ENEMY_SIZEX = 32
ENEMY_SIZEY = 32

PLAYER_VELOCITY = 300
PIXEL_PER_TICK = 10

TICKS_PER_SEC = 30

# todo: impelement projectile
class Projectile:
    def __init__(self):
        pass


class Player:
    def __init__(self, image_path, pos):
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image,(PLAYER_SIZEX, PLAYER_SIZEY)) # scale it down
        self.pos = pos

    def draw(self,surface):
        surface.blit(self.image, self.pos)

    def move(self, dt):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.pos.x -= PLAYER_VELOCITY * dt
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.pos.x += PLAYER_VELOCITY * dt
    
class Enemy:
    class Direction(Enum):
        RIGHT = 1
        LEFT = 2
        DOWN = 3

    def __init__(self, image_path, pos, index):
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (ENEMY_SIZEX, ENEMY_SIZEY)) # scale it down
        self.pos = pos
        self.direction = self.Direction.RIGHT
        self.index = index

    def update(self, dt):
        if self.direction == self.Direction.RIGHT:
            self.pos.x += PIXEL_PER_TICK
        if self.direction == self.Direction.LEFT:
            self.pos.x -= PIXEL_PER_TICK

    def draw(self, surface):
        surface.blit(self.image, self.pos)

class Time:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.dt = 0

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Invaders On Space (definitly original)")
        self.time = Time() 

        self.__initEnemyList()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface = pg.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT))
        self.player = Player('paddle.png',pg.Vector2(SCREEN_WIDTH / 4, SCREEN_HEIGHT - 40))
        self.move_ticks = 0
    def __initEnemyList(self):
        self.enemies = []
        for i in range(6):
            for j in range(4):
                enemy = Enemy('awesomeface.png', pg.Vector2(i * ENEMY_SIZEX + ENEMY_PADDING, j * ENEMY_SIZEY + ENEMY_PADDING), i * 4 + j)
                self.enemies.append(enemy)

    def draw(self):
        self.surface.fill((30,30,30))
        # draw enemies here
        for i in self.enemies:
            i.draw(self.surface)
        self.player.draw(self.surface)
        self.screen.fill((0,0,0))
        self.screen.blit(self.surface,(SCREEN_WIDTH / 4,0))
        pg.display.flip()

    def run(self):
        self.running = True
        self.clock = pg.time.Clock()
        while self.running:
            self.tick()
            self.handle_event()
            self.draw()
            self.update()

    def tick(self):
        self.time.dt = self.clock.tick(60) / 1000
        # fixme: this can be overflow and application may crash. time required to overflow is so high so we can ignore it for now.
        self.move_ticks += 1 

        for index, enemy in enumerate(self.enemies):
            if ((self.move_ticks  + index * 30) % len(self.enemies)) == 0:
                enemy.update(self.time.dt)

    def update(self):
        self.player.move(self.time.dt)
        
    def handle_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.running = False
def main():
    game =  Game()
    game.run()    
    pg.quit()

if __name__ == "__main__":
    main()