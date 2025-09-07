import pygame, csv, os


# Class for Tiles
class Tile(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Assets", image_name))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        


    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap():
    def __init__(self, file_name, surfacex):
        self.tile_size = 44
        self.width = 0
        self.height = 0
        self.tiles = self.load_tiles(file_name)
        self.map_surface = pygame.Surface((self.map_width, self.map_height))
        self.surfacex = surfacex
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface, offset_x, offset_y):
        surface.blit(self.map_surface, (0 - offset_x, 0 - offset_y))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for line in data:
                map.append(list(line))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '1':
                    tiles.append(Tile('grass.png', x * self.tile_size, y * self.tile_size))
                elif tile == '2':
                    tiles.append(Tile('dirt.png', x * self.tile_size, y * self.tile_size))
                elif tile == '3':
                    tiles.append(Tile('block.png', x * self.tile_size, y * self.tile_size))
                x += 1

            y += 1
        self.map_width, self.map_height = x * self.tile_size, y * self.tile_size
        return tiles