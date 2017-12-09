from settings import *
import random
import math
import pygame

Vector = pygame.math.Vector2

class Spritesheet:
    def __init__(self, filename, tile_size):
        self.texture = pygame.image.load(filename).convert()
        self.tile_width = tile_size[0]
        self.tile_height = tile_size[1]
        image_size = self.texture.get_size()
        self.texture_width = image_size[0]
        self.texture_height = image_size[1]
        self.sheet_width = int(self.texture_width / self.tile_width)
        self.sheet_height = int(self.texture_height / self.tile_height)
        self.count = self.sheet_width * self.sheet_height
        self.sprites = [None for _ in range(self.count)]
        for y in range(0, self.sheet_width):
            for x in range(0, self.sheet_height):
                self.sprites[y * self.sheet_width + x] = self.crop_image((x * self.tile_width, y * self.tile_height), (SPRITE_SIZE, SPRITE_SIZE))

    def crop_image(self, pos, scale=False):
        image = pygame.Surface((self.tile_width, self.tile_height))
        image.blit(self.texture, (0, 0), (pos[0], pos[1], self.tile_width, self.tile_height))
        image.set_colorkey(COLOUR_KEY)
        if scale:
            return pygame.transform.scale(image, (scale[0], scale[1]))
        return image

    def get_image(self, pos):
        return self.sprites[pos[1] * self.sheet_width + pos[0]]

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, character_type):
        self.groups = game.layers["PLAYER"]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_frames(character_type)
        self.image = self.animation_R[0]
        self.rect = self.image.get_rect()
        self.pos = Vector(x, y)
        self.shadow = Shadow(self.game, self)
        self.enemies_killed = 0
        self.coins = 0
        self.lifesteal = 0
        self.damage = PLAYER_STATS[0]
        self.max_health = PLAYER_STATS[1]
        self.health = PLAYER_STATS[1]
        self.hit_resistance = PLAYER_STATS[2]
        self.accuracy = PLAYER_STATS[3]
        self.key = False

    def load_frames(self, player_type):
        self.animation_frame = 0
        self.last_frame_time = 0
        self.animation_R = [self.game.sprite_sheet.get_image(sprites) for sprites in PLAYER_ANIMATION_FRAMES[player_type]]
        self.animation_L = [pygame.transform.flip(image, True, False) for image in self.animation_R]
        self.frame_count = len(self.animation_R)
        self.frames = self.animation_R

    def update(self):
        self.animate()
        self.rect.x = self.pos.x * SPRITE_SIZE
        self.rect.y = self.pos.y * SPRITE_SIZE
        self.shadow.update()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_frame_time > ANIMATION_INTERVAL:
            self.last_frame_time = now
            self.animation_frame = (self.animation_frame + 1) % self.frame_count
            self.image = self.frames[self.animation_frame]

    def move(self, dx=0, dy=0):
        wall = self.collide(self.game.layers["WALLS"], dx, dy)
        if wall and self.key:
            wall.interact()
        if not wall and not self.collide(self.game.layers["ENEMIES"], dx, dy):
            self.pos.x += dx
            self.pos.y += dy
        self.handle_encounters(dx, dy)
        self.handle_pickups()
        if dx > 0:
            self.frames = self.animation_R
        elif dx < 0:
            self.frames = self.animation_L
        self.image = self.frames[self.animation_frame]

    def handle_pickups(self):
        pickup = self.collide(self.game.layers["PICKUPS"])
        if pickup:
            pickup_type = pickup.pick()
            if pickup_type == "coin":
                self.coins += 1
            elif pickup_type == "key":
                self.key = True

    def handle_encounters(self, dx, dy):
        enemy = self.collide(self.game.layers["ENEMIES"], dx, dy)
        if enemy:
            enemy.hit(self)

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def hit(self, attacker):
        hit_chance = attacker.accuracy - self.hit_resistance
        if hit_chance > 1:
            self.health -= attacker.damage
        elif random.random() < hit_chance:
            self.health -= attacker.damage
        if self.health < 1:
            self.game.game_over()
            self.delete()

    def collide(self, layer, dx=0, dy=0):
        for sprite in layer:
            if sprite.pos.x == self.pos.x + dx and sprite.pos.y == self.pos.y + dy:
                return sprite
        return False

    def delete(self):
        self.kill()
        self.shadow.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, character_type):
        self.groups = game.layers["ENEMIES"]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_frames(character_type)
        self.image = self.animation_R[0]
        self.rect = self.image.get_rect()
        self.pos = Vector(x, y)
        self.shadow = Shadow(self.game, self)
        self.type = character_type
        self.damage = ENEMY_STATS[character_type][0] + self.game.stage * 0.001
        self.health = ENEMY_STATS[character_type][1] + self.game.stage * 0.001
        self.hit_resistance = ENEMY_STATS[character_type][2] + self.game.stage * 0.001
        self.accuracy = ENEMY_STATS[character_type][3] + self.game.stage * 0.001

    def load_frames(self, character_type):
        self.animation_frame = 0
        self.last_frame_time = 0
        self.animation_R = [self.game.sprite_sheet.get_image(sprites) for sprites in ENEMY_ANIMATION_FRAMES[character_type]]
        self.animation_L = [pygame.transform.flip(image, True, False) for image in self.animation_R]
        self.frame_count = len(self.animation_R)
        self.frames = self.animation_R

    def update(self):
        self.animate()
        self.rect.x = self.pos.x * SPRITE_SIZE
        self.rect.y = self.pos.y * SPRITE_SIZE
        self.shadow.update()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_frame_time > ANIMATION_INTERVAL:
            self.last_frame_time = now
            self.animation_frame = (self.animation_frame + 1) % self.frame_count
            if self.game.player.pos.x - self.pos.x > 0:
                self.frames = self.animation_R
            else:
                self.frames = self.animation_L
            self.image = self.frames[self.animation_frame]

    def hit(self, attacker):
        hit_chance = attacker.accuracy - self.hit_resistance + BASE_HIT_CHANCE
        if hit_chance < 0.1:
            hit_chance = 0.1
        if hit_chance > 1:
            self.health -= attacker.damage
            self.game.sounds["HIT"][self.type].play()
        elif random.random() < hit_chance:
            self.health -= attacker.damage
            self.game.sounds["HIT"][self.type].play()
        if self.health < 0.01:
            self.kill_bonus()
            self.delete()
            self.game.player.enemies_killed += 1
        self.game.player.heal(self.game.player.lifesteal)
        attacker.hit(self)

    def kill_bonus(self):
        if self.type == 0:
            self.game.player.heal(3)
            self.game.player.lifesteal += 0.005
        elif self.type == 1:
            self.game.player.accuracy += 0.005
        elif self.type == 2:
            self.game.player.damage += 0.001
        elif self.type == 3:
            self.game.player.hit_resistance += 0.005

    def delete(self):
        self.kill()
        self.shadow.kill()

class Shadow(pygame.sprite.Sprite):
    def __init__(self, game, entity):
        self.groups = game.layers["SHADOWS"]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.entity = entity
        self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

    def load_frames(self):
        self.frames = [self.game.sprite_sheet.get_image(sprites) for sprites in SHADOW_FRAMES]
        self.type = 1

    def update(self):
        self.rect.x = self.entity.rect.x
        self.rect.y = self.entity.rect.y + SPRITE_SIZE

class Pickup(pygame.sprite.Sprite):
    def __init__(self, game, x, y, pickup_type):
        self.groups = game.layers["PICKUPS"]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = pickup_type
        self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.pos = Vector(x, y)
        self.shadow = Shadow(self.game, self)

    def load_frames(self):
        self.animation_frame = 0
        self.last_frame_time = 0
        self.frames = [self.game.sprite_sheet.get_image(sprites) for sprites in PICKUP_ANIMATION_FRAMES[self.type]]
        self.frame_count = len(self.frames)

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_frame_time > ANIMATION_INTERVAL:
            self.last_frame_time = now
            self.animation_frame = (self.animation_frame + 1) % self.frame_count
            self.image = self.frames[self.animation_frame]

    def update(self):
        self.animate()
        self.rect.x = self.pos.x * SPRITE_SIZE
        self.rect.y = self.pos.y * SPRITE_SIZE

    def change_type(self, pickup_type):
        self.type = pickup_type
        self.load_frames()
        self.image = self.frames[0]

    def pick(self):
        self.kill()
        self.shadow.kill()
        if self.type == 0:
            self.game.sounds["COIN"].play()
            return "coin"
        elif self.type == 1:
            self.game.sounds["KEY"].play()
            return "key"

    def delete(self):
        self.kill()
        self.shadow.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, wall_type):
        self.groups = game.layers["WALLS"]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = wall_type
        self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.pos = Vector(x, y)
        self.rect.topleft = self.pos * SPRITE_SIZE

    def load_frames(self):
        self.frames = [self.game.sprite_sheet.get_image(sprites) for sprites in WALL_FRAMES[self.type]]

    def update_sprite(self, ID):
        self.image = self.frames[ID]

    def change_type(self, wall_type):
        self.type = wall_type
        self.load_frames()
        self.image = self.frames[0]

    def delete(self):
        self.kill()

    def interact(self):
        if self.type != 1:
            return
        else:
            self.game.new_level()

class Floor(pygame.sprite.Sprite):
    def __init__(self, game, x, y, floor_type=False):
        self.groups = game.layers["FLOOR"]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_frames()
        if floor_type:
            self.floor_type = floor_type
        else:
            self.floor_type = random.randint(0, 2)
        self.image = self.frames[self.floor_type]
        self.rect = self.image.get_rect()
        self.pos = Vector(x, y)
        self.rect.topleft = self.pos * SPRITE_SIZE

    def load_frames(self):
        self.frames = [self.game.sprite_sheet.get_image(sprites) for sprites in FLOOR_FRAMES]

    def delete(self):
        self.kill()

class UserInterface(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.layers["UI"]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.offset = int(SPRITE_SIZE / 4)
        self.image = pygame.Surface((SCREEN_WIDTH, SPRITE_SIZE + self.offset * 2))
        self.rect = self.image.get_rect()
        self.pos = Vector(0, 0)
        self.load_frames()

    def load_frames(self):
        self.health = [self.game.sprite_sheet.get_image(sprite) for sprite in UI_HEALTH]
        self.key = self.game.sprite_sheet.get_image(UI_KEY)
        self.coin = self.game.sprite_sheet.get_image(UI_COIN)

    def update(self):
        self.image.fill(BLACK)
        for i in range(0, int(self.game.player.max_health / 3)):
            health_bit = int(self.game.player.health - i * 3)
            if health_bit < 1:
                health_bit = 0
            elif health_bit > 3:
                health_bit = 3
            self.image.blit(self.health[health_bit], (self.offset * 2 + SPRITE_SIZE * i, self.offset * 2))
        if self.game.player.key:
            self.image.blit(self.key, (SCREEN_WIDTH - SPRITE_SIZE - self.offset, self.offset / 2))
        self.image.blit(self.coin, (self.offset + SPRITE_SIZE * 8, self.offset))
        text = self.game.font.render(str(self.game.player.coins), False, WHITE, BLACK)
        self.image.blit(text, (self.offset + SPRITE_SIZE * 9 + self.offset, self.offset + self.offset / 4))