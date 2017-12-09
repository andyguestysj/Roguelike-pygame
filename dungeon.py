import pygame
import random
import sprites
import time

class DungeonGenerator:
    def __init__(self, game):
        self.game = game

    def generate(self):
        self.coin_spawn_chance = 0.75
        self.max_steps = 1000
        self.floor_type = 3
        self.wall_type = 0
        self.enemy_spawn_chance = 0.1
        self.enemy_min_distance = 10
        self.exit_placed = False

        self.game.title_screen("Placing floor", 500)
        self.generate_floor()
        
        self.game.title_screen("Placing walls")
        corner_floor_coords = self.generate_walls()
        
        self.game.title_screen("Dropping coins", 500)
        self.add_coins()

        self.game.title_screen("Spawning monsters", 500)
        self.add_enemies()

        self.game.title_screen("Some finishing touches", 1000)
        self.place_corner_floors(corner_floor_coords)

    def generate_floor(self):
        self.step = 0
        self.walker = Walker(0, 0, 1)
        while self.step < self.max_steps:
            self.place_floor(self.walker.x, self.walker.y)
            self.walker.step()
            self.step += 1

    def generate_walls(self):
        corner_floors = []
        for floor in self.game.layers["FLOOR"]:
            for y in range(int(floor.pos.y - 1), int(floor.pos.y + 2)):
                for x in range(int(floor.pos.x - 1), int(floor.pos.x + 2)):
                    if not (x == int(floor.pos.x) and y == int(floor.pos.y)):
                        if not self.get_sprites_at([self.game.layers["WALLS"]], x, y) and not self.get_sprites_at([self.game.layers["FLOOR"]], x, y):
                            sprites.Wall(self.game, x, y, self.wall_type)
                            a, b, c, d = self.get_neighbours(self.game.layers["FLOOR"], x, y)
                            if a+b+c+d:
                                corner_floors.append((x, y))
        for wall in self.game.layers["WALLS"]:
            top, right, bottom, left = self.get_neighbours(self.game.layers["WALLS"], wall.pos.x, wall.pos.y)
            if not self.place_exit(wall, (top, right, bottom, left)):
                wall.update_sprite(top + right * 2 + bottom * 4 + left * 8)
        return corner_floors

    def add_enemies(self):
        for floor in self.game.layers["FLOOR"]:
            a, b, c, d = self.get_neighbours(self.game.layers["WALLS"], floor.pos.x, floor.pos.y)
            if a + b + c + d == 0 and not self.get_sprites_at([self.game.layers["ENEMIES"], self.game.layers["PLAYER"], self.game.layers["PICKUPS"]], floor.pos.x, floor.pos.y):
                if random.random() < self.enemy_spawn_chance:
                    self.place_enemy(floor.pos.x, floor.pos.y)

    def place_exit(self, wall, neihbours):
        top, right, bottom, left = neihbours
        if not self.exit_placed:
            if not top and not bottom and right and left:
                self.exit_placed = True
                wall.change_type(1)
                return True
        return False


    def place_enemy(self, x, y):
        for enemy in self.game.layers["ENEMIES"]:
            if self.distance_squared((x, y), (enemy.pos.x, enemy.pos.y)) < self.enemy_min_distance:
                return
        enemy_type = random.randint(0, 3)
        sprites.Enemy(self.game, x, y, enemy_type)

    def add_coins(self):
        for floor in self.game.layers["FLOOR"]:
            if floor.pos.x != 0 and floor.pos.y != 0:
                a, b, c, d = self.get_neighbours(self.game.layers["WALLS"], floor.pos.x, floor.pos.y)
                if a + b + c + d == 3 and random.random() < self.coin_spawn_chance and not self.get_sprites_at([self.game.layers["PICKUPS"]], floor.pos.x, floor.pos.y):
                    self.place_coin(floor.pos.x, floor.pos.y)
        index = len(self.game.layers["PICKUPS"]) - 1
        self.game.layers["PICKUPS"].sprites()[index].change_type(1)

    def place_coin(self, x, y):
        sprites.Pickup(self.game, x, y, 0)

    def place_floor(self, x, y):
        sprites.Floor(self.game, x, y, self.floor_type)

    def place_corner_floors(self, coords):
        for coord in coords:
            self.place_floor(*coord)

    def get_neighbours(self, layer, x, y):
        count = 0
        top, right, bottom, left = 0, 0, 0, 0
        for el in layer:
            if count > 3:
                break
            if el.pos.x == x and el.pos.y == y - 1:
                top = 1
                count += 1
            elif el.pos.x == x + 1 and el.pos.y == y:
                right = 1
                count += 1
            elif el.pos.x == x and el.pos.y == y + 1:
                bottom = 1
                count += 1
            elif el.pos.x == x - 1 and el.pos.y == y:
                left = 1
                count += 1
        return (top, right, bottom, left)

    def get_sprites_at(self, layers, x, y):
        sprites = []
        for layer in layers:
            for sprite in layer:
                if sprite.pos.x == x and sprite.pos.y == y:
                    sprites.append(sprite)
        return sprites

    def distance_squared(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        delta_x = x2 - x1
        delta_y = y2 - y1
        return delta_x * delta_x + delta_y + delta_y

class Walker:
    def __init__(self, x, y, turn_chance):
        self.x = x
        self.y = y
        self.turn_chance = turn_chance
        self.dir = random.randint(0, 3)

    def step(self):
        if random.random() < self.turn_chance:
            self.dir = random.randint(0, 3)
        if self.dir == 0:
            self.y -= 1
        elif self.dir == 1:
            self.x += 1
        elif self.dir == 2:
            self.y += 1
        else:
            self.x -= 1

    def spawn_new(self, turn_chance):
        return Walker(self.x, self.y, turn_chance)