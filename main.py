from dungeon import DungeonGenerator
from camera import Camera
from settings import *
from sprites import *
import pygame
import sys
import os

class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.key.set_repeat(KEYBOARD_REPEAT_THRESHOLD, KEYBOARD_REPEAT_INTERVAL)
        pygame.display.set_icon(pygame.image.load(WINDOW_ICON))
        pygame.display.set_caption(SCREEN_TITLE)
        pygame.mouse.set_visible(False)
        self.fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        self.sprite_sheet = Spritesheet(SPRITE_SHEET, (IMAGE_SIZE, IMAGE_SIZE))
        self.font = pygame.font.Font(FONT_FILE, 24)
        self.sounds = {
            "COIN" : pygame.mixer.Sound(PLAYER_PICKUP_COIN_SOUND),
            "KEY" : pygame.mixer.Sound(PLAYER_PICKUP_KEY_SOUND),
            "HIT" : [pygame.mixer.Sound(sound) for sound in HIT_SOUND]
        }
        self.highscore = self.load_highscore()

    def load_highscore(self):
        if os.path.isfile(HIGHSCORE):
            with open(HIGHSCORE, "r") as f:
                return int(f.readline().strip())
        else:
            return 0

    def save_highscore(self):
        with open(HIGHSCORE, "w") as f:
            f.write(str(self.highscore))

    def new(self):
        self.stage = 0
        self.layers = {
            "FLOOR" : pygame.sprite.Group(),
            "SHADOWS" : pygame.sprite.Group(),
            "WALLS" : pygame.sprite.Group(),
            "PICKUPS" : pygame.sprite.Group(),
            "ENEMIES" : pygame.sprite.Group(),
            "PLAYER" : pygame.sprite.Group(),
            "UI" : pygame.sprite.Group()
        }
        self.player = Player(self, 0, 0, 0)
        self.camera = Camera()
        self.UI = UserInterface(self)
        self.generator = DungeonGenerator(self)
        self.new_level()

    def clear_layer(self, layer):
        for sprite in layer:
            sprite.delete()

    def new_level(self):
        self.clear_layer(self.layers["FLOOR"])
        self.clear_layer(self.layers["WALLS"])
        self.clear_layer(self.layers["PICKUPS"])
        self.clear_layer(self.layers["ENEMIES"])
        self.player.pos.x = 0
        self.player.pos.y = 0
        self.player.key = False
        self.generator.generate()
        self.stage += 1

    def game_over(self):
        self.playing = False

    def run(self):
        self.new()
        self.playing = True
        self.restart = False
        while self.playing:
            self.dt = self.clock.tick(FRAMERATE) / 1000
            self.events()
            self.update()
            self.draw()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.layers["SHADOWS"].update()
        self.layers["PICKUPS"].update()
        self.layers["PLAYER"].update()
        self.layers["ENEMIES"].update()
        self.layers["UI"].update()
        self.camera.update(self.player)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pygame.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pygame.K_UP:
                    self.player.move(dy=-1)
                if event.key == pygame.K_DOWN:
                    self.player.move(dy=1)
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()
                if event.key == pygame.K_r:
                    self.restart = True
                    self.game_over()
                    self.end_screen()

    def draw(self):
        self.update()
        self.events()
        self.screen.fill(BACKGROUND_COLOUR)
        for layer in self.layers:
            for sprite in self.layers[layer]:
                if layer != "UI":
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                else:
                    self.screen.blit(sprite.image, sprite.rect)
        #self.draw_grid()
        pygame.display.flip()

    def start_screen(self):
        self.title_screen("PRESS ANY KEY TO START")
        self.wait_for_key()

    def end_screen(self):
        pygame.event.pump()
        self.screen.fill(BACKGROUND_COLOUR)
        if self.restart:
            return
        score = self.stage * STAGE_POINTS + self.player.coins * COIN_POINTS + self.player.enemies_killed * ENEMY_KILL_POINTS
        if score > self.highscore:
            self.highscore = score
            self.save_highscore()
        self.render_text(f"You scored {score}", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 32))
        self.render_text(f"Your best {self.highscore}", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        pygame.display.flip()
        pygame.time.wait(1000)
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FRAMERATE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()
                        self.title_screen("PRESS ANY KEY TO START")
                        continue
                    waiting = False

    def title_screen(self, text, wait=0):
        pygame.event.pump()
        self.screen.fill(BACKGROUND_COLOUR)
        text = self.font.render(text, False, WHITE, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(wait)

    def render_text(self, text, pos):
        text = self.font.render(text, False, WHITE, BLACK)
        text_rect = text.get_rect()
        text_rect.midtop = pos
        self.screen.blit(text, text_rect)

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            pygame.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, SPRITE_SIZE):
            pygame.draw.line(self.screen, LIGHT_GREY, (0, y), (SCREEN_WIDTH, y))

if __name__ == "__main__":
    game = Game()
    game.start_screen()
    while True:
        game.run()
        game.end_screen()