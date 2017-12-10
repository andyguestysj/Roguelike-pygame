from settings import *
import pygame

class Camera:
    def __init__(self):
        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.calculate_offset(SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_SIZE)

    def calculate_offset(self, w, h, ts):
        self.offsetX = int((w - ts) / 2)
        self.offsetY = int((h - ts) / 2)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.camera.x = -target.rect.x + self.offsetX
        self.camera.y = -target.rect.y + self.offsetY
        