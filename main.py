import pygame as pg


SCREEN_WIDTH  = 1366
SCREEN_HEIGHT = 768

class State:
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_pos = pg.Vector2(SCREEN_WIDTH / 4,SCREEN_HEIGHT - 40)
    surface = pg.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT))
    player_image = pg.image.load('paddle.png')
    running: bool = True
    velocity: int = 300
    class enemy:
        test = 0
# global state
state = State()

def init_state():
    pg.init()
    pg.display.set_caption("Invaders On Space (definitly original)")
    return

def handle_key(dt):
    keys = pg.key.get_pressed()
    if keys[pg.K_a] or keys[pg.K_LEFT]:
        state.player_pos.x -= state.velocity * dt
    if keys[pg.K_d] or keys[pg.K_RIGHT]:
        state.player_pos.x += state.velocity * dt
    if keys[pg.K_ESCAPE]:
        state.running = False

def main():
    init_state()

    clock = pg.time.Clock()
    dt = 0
    state.player_image = pg.transform.scale(state.player_image, (98, 24))

    while state.running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                state.running = False
        # render stuff here
        state.surface.fill((30,30,30))
        state.surface.blit(state.player_image,state.player_pos)
        
        state.screen.fill((0,0,0))
        state.screen.blit(state.surface,(SCREEN_WIDTH / 4, 0))

        handle_key(dt)
        pg.display.flip()
        dt = clock.tick(60) / 1000

    pg.quit()


if __name__ == "__main__":
    main()