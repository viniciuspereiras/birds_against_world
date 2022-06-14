
import pygame
import random
import os

class Game:
    def __init__(self) -> None:
        self.author = "Vinicius Pereira"
        self.version = "0.0.1"
        self.title = "Birds against the world"

game = Game()
pygame.init()


images_path = os.path.join("images")
flowers_path = os.path.join(images_path, "flowers")
enemies_path = os.path.join(images_path, "enemies")

DISPLAY = pygame.display.set_mode((640, 640))
pygame.display.set_caption(game.title)


background = pygame.image.load(os.path.join(images_path, "background.png"))


backgound = pygame.transform.scale(background, (640, 640))
RED = (255, 0, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
ACELERATION = 0.15

class Bird:
    def __init__(self) -> None:
        self.x = 640 / 2
        self.y = 0
        self.width = 60
        self.velocity = pygame.Vector2()
        self.velocity.xy = 3, 0
        self.image = pygame.image.load(os.path.join(images_path, 'bird.png'))
        self.image = pygame.transform.scale(self.image, (self.width, self.width))
    def create(self):
        DISPLAY.blit(self.image, (self.x, self.y))

    def invert_image(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Plane:
    def __init__(self) -> None:
        self.x = random.choice([0, 580])
        self.y = random.randint(40, 320)
        self.velocity = pygame.Vector2()
        self.velocity_random = random.randint(3, 8)
        if self.velocity_random > 6:
            self.width = 70
            self.image = pygame.image.load(os.path.join(enemies_path, 'fast.png'))
            self.image = pygame.transform.scale(self.image, (self.width, self.width))
        else:
            self.width = 80
            self.image = pygame.image.load(os.path.join(enemies_path, 'slow.png'))
            self.image = pygame.transform.scale(self.image, (self.width, self.width))
        if self.x == 580:
            self.velocity.xy = -self.velocity_random, 0
        else:
            self.velocity.xy = self.velocity_random, 0
        if self.x == 0:
            self.invert_image()
    
    def create(self):
        DISPLAY.blit(self.image, (self.x, self.y))

    def invert_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def remove(self):
        DISPLAY.blit(backgound, (self.x, self.y))


class Flower:
    def __init__(self) -> None:
        self.x = random.randint(0, 600)
        self.y = random.randint(0, 600)
        self.width = 80
        self.height = 60
        self.images = get_all_files_in_folder(flowers_path)
        print(self.images)
        self.image = random.choice(self.images)
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale(self.image, (self.width, self.width))

    def create(self):
        DISPLAY.blit(self.image, (self.x, self.y))

    def remove(self):
        DISPLAY.blit(background, (self.x, self.y))


def create_flower():
    flower = Flower()
    return flower

def write(display, text, size, font, color, x, y):
    font = pygame.font.SysFont(font, size)
    text = font.render(text, 1, color)
    textpos = text.get_rect()
    textpos.centerx = x
    textpos.centery = y
    display.blit(text, textpos)

def get_all_files_in_folder(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files



def start():
    global bird
    global flower
    global flowers
    global plane
    global planes
    global score
    global run 
    global game_over
    
    bird = Bird()
    flower = Flower()
    flowers = []
    for i in range(0, 2):
        flowers.append(create_flower())
    planes = []
    plane = Plane()
    planes.append(plane)
    score = 0
    run = True
    start_menu = False
    game_over = False

start_menu = True
while start_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_menu = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_menu = False
                game_over = False
                start()
                run = True
                
    DISPLAY.blit(backgound, (0, 0))
    write(DISPLAY, game.title, 30, "consolas", RED, 640 / 2, 640 / 2 - 50)
    write(DISPLAY, "Press SPACE to start :)", 30, "consolas", BLACK, 640 / 2, 640 / 2)
    pygame.display.update()

while run:
    DISPLAY.blit(background, (0, 0))
    write(DISPLAY, "Score: " + str(score), 50, None, BLACK, 80, 20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    for flower in flowers:
        flower.create()
        if bird.x + bird.width / 2 > flower.x and bird.x < flower.x + flower.width / 2 and bird.y + bird.width / 2 > flower.y and bird.y < flower.y + flower.width / 2:
            score += 1
            flowers.remove(flower)
            if len(flowers) <= 1:
                flowers.append(create_flower())
            bird.velocity.y += ACELERATION


    plane.x += plane.velocity.x
    try:
        planes[-1].create()
    except:
        planes.append(Plane())
    if plane.x <= 0 - plane.width or plane.x >= 580 + plane.width:
        planes.remove(plane)
        plane = Plane()
        planes.append(plane)

    
    if bird.x + bird.width / 2 > plane.x and bird.x < plane.x + plane.width / 2 and bird.y + bird.width / 2 > plane.y and bird.y < plane.y + plane.width / 2:
        # Bird hit the plane
        game_over = True
        run = False
        
    bird.create()
    first_flower = False
    bird.y += bird.velocity.y
    bird.x += bird.velocity.x

 
    
    if bird.x + bird.width / 2 > DISPLAY.get_width(): #right
        bird.velocity.x = -3
        bird.invert_image()
    if bird.x + bird.width / 2 < 0: #left
        bird.velocity.x = 3
        bird.invert_image()
    
    if bird.y + bird.width / 2 > DISPLAY.get_height(): # down
        impact_velocity = bird.velocity.y 
        bird.velocity.y = -3
        # Bird is falling
        game_over = True
        run = False
    if bird.y - bird.width / 2 < 0: # up
        bird.velocity.y = 0
        bird.y = bird.width / 2
    
    bird.velocity.y += ACELERATION

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird.velocity.y = -4
    
    pygame.display.update()
    pygame.time.delay(10)

while game_over:
    DISPLAY.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start()
                run = True
                game_over = False

    write(DISPLAY, "GaMe OvEr", 100, "consolas", ORANGE, 640 / 2, 640 / 2 - 50)
    write(DISPLAY, "Close to try again :(", 30, "consolas", BLACK, 640 / 2, 640 / 2)
    pygame.display.update()

