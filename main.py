import random
import pygame, sys
from pygame.math import Vector2

class Snake:
    def __init__(self):

        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.crunch_sound = pygame.mixer.Sound('attributes/crunch.wav')

    def spawn(self):
        for block in self.body:
            x = int(block.x * cell_size)
            y = int(block.y * cell_size)
            block_rect = pygame.Rect(x,y, cell_size, cell_size)
            pygame.draw.rect(screen, (141, 61, 255), block_rect)

    def move(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def grow(self):
        self.new_block = True

    def crunch(self):
        self.crunch_sound.play()

    def die(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Apple:
    def __init__(self):
        self.random()

    def random(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def spawn_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)


class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Apple()

    def update(self):
        self.snake.move()
        self.hit()
        self.check_over()

    def display(self):
        self.fruit.spawn_fruit()
        self.snake.spawn()
        self.display_score()

    def check_over(self):
        if not 0 <= self.snake.body[0].x <= cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake.die()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.die()

    def hit(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.random()
            self.snake.grow()
            self.snake.crunch()


    def display_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True, (0, 0, 0))
        score_x = int(cell_size * cell_number - 50)
        score_y = int(cell_size * cell_number - 50)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        screen.blit(score_surface, score_rect)



    def game_over(self):
        pygame.quit()
        sys.exit()


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
apple = pygame.image.load('icons/apple2.png').convert_alpha()
game_font = pygame.font.Font('attributes/Sticky Notes.ttf', 75)
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
main_game = MAIN()
screen.fill((175, 215, 70))

menu = True
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((78, 220, 92))

    menu_surface = game_font.render("Click The Up Arrow To Play", True, (0, 0, 0))
    score_x = int(cell_size * cell_number - 420)
    score_y = int(cell_size * cell_number - 400)
    menu_rect = menu_surface.get_rect(center=(score_x, score_y))
    screen.blit(menu_surface, menu_rect)
    pygame.display.update()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            menu = False
            run = True
        elif event.key == pygame.K_DOWN:
            pygame.quit()




while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)


    screen.fill((78, 220, 92))
    main_game.display()
    pygame.display.update()
    clock.tick(60)