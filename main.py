import pygame
import sys
import os
from pprint import pprint


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(os.path.join('data', filename), 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину    
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))  # подгоняем под размер
    screen.blit(fon, (0, 0))  # отрисовываем картинку
    font = pygame.font.Font(None, 30)  # подгружаем шрифт
    text_coord = 50  # координаты текста
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))  # рендерим текст
        intro_rect = string_rendered.get_rect()  # получаем размер текста
        text_coord += 10  # увеличиваем координаты текста
        intro_rect.top = text_coord  # меняем x координату
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)  # отображаем текст

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                '''
                # — означает стену
                @ — положение игрока
                . — пустая клетка
                '''
                return
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('mar.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width + 15
        self.rect.y = pos_y * tile_height + 5
        
    def update(self, event):
        x, y = self.rect.x // tile_width, self.rect.y // tile_height
        if event.key == pygame.K_LEFT:
            if x - 1 >= 0 and level[y][x - 1] != '#':
                self.rect.x -= tile_width
        elif event.key == pygame.K_RIGHT:
            if x + 1 <= 9 and level[y][x + 1] != '#':
                self.rect.x += tile_width
        elif event.key == pygame.K_UP:
            if y - 1 >= 0 and level[y - 1][x] != '#':
                self.rect.y -= tile_height
        elif event.key == pygame.K_DOWN:
            if x + 1 <= 9 and level[y + 1][x] != '#':
                self.rect.y += tile_height

def generate_level(level):
    global player_coords
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':  # трава
                Tile('empty', x, y)
            elif level[y][x] == '#':  # блок
                Tile('wall', x, y)
            elif level[y][x] == '@':  # персонаж
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


if __name__ == "__main__":
    pygame.init()
    FPS = 50
    size = (WIDTH, HEIGHT) = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')}
    tile_width = tile_height = 50

    level = load_level('level.txt')
    player, level_x, level_y = generate_level(level)
    start_screen()  # отображаем заставку

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                player.update(event)
                                 
        screen.fill('black')
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)