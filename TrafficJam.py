import pygame
import sys
import random
import pickle
import os

os.chdir(os.path.dirname(__file__))

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("./music.mp3")
pygame.mixer.music.play(-1)

WIDTH = 600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Traffic Jam")
font = "font.ttf"
font2 = pygame.font.Font("./font.ttf", 80)

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, enemies):
    pygame.sprite.Sprite.__init__(self)
    
    self.image = pygame.transform.scale(pygame.image.load("Images/player.png"), (84, 84))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.vel = 15
    self.score = 0
    self.enemies = enemies

  def update(self):
    screen.blit(self.image, (self.rect))

    keys_pressed = pygame.key.get_pressed()

    self.score += 1

    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
      if self.rect.x > 98:
        self.rect.x -= self.vel

    if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
      if self.rect.x < 418:
        self.rect.x += self.vel

  def isColliding(self, func):
    for enemy in self.enemies:
      if self.rect.colliderect(enemy.rect):
        func(self.score)
        

class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.transform.scale(pygame.image.load(random.choice(["Images/obstacle0.png", "Images/obstacle1.png", "Images/obstacle2.png", "Images/obstacle3.png"])), (84, 84))
    self.rect = self.image.get_rect()
    self.rect.x = random.randint(98, 418)
    self.rect.y = random.randint(-110, -50)
    self.vel = 15

  def update(self):
    screen.blit(self.image, self.rect)

    if self.rect.y < 800:
      self.rect.y += self.vel
    else:
      self.rect.y = random.randint(-70, -50)
      self.rect.x = random.randint(98, 418)
      self.image = pygame.transform.scale(pygame.image.load(random.choice(["Images/obstacle0.png", "Images/obstacle1.png", "Images/obstacle2.png", "Images/obstacle3.png"])), (84, 84))


class Background(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.images = []
    self.paths = ["Images/road0.png", "Images/road1.png", "Images/road2.png", "Images/road0.png"]
    for image in self.paths:
        self.images.append(pygame.transform.scale(pygame.image.load(image), (WIDTH, HEIGHT)))
       
    self.index = 0

  def update(self):
    image = self.images[self.index-1]
    screen.blit(image, (0, 0))

    if self.index <= 3:
      self.index += 1
    else:
      self.index = 0

class Text():
  def __init__(self, x, y, font, text, color, size):
    self.font = pygame.font.Font(font, size)
    self.x = x
    self.y = y
    self.text = text
    self.color = color
    self.rect = self.font.render(text, True, color).get_rect()
    self.rect.x = self.x
    self.rect.y = self.y

  def render(self):
    rendered_text = self.font.render(self.text, True, self.color)
    screen.blit(rendered_text, (self.x, self.y))

  def isColliding(self, obj):
    if self.rect.collidepoint(obj):
      return True
    else:
      return False
    
clock = pygame.time.Clock()

def mainMenu():
  title = Text(60, 200, font, "Traffic Jam", (255, 255, 255), 100)
  play = Text(215, 300, font, "Play", (255, 255, 255), 80)
  credit = Text(165, 380, font, "Credits", (255, 255, 255), 80)
  help_button = Text(215, 460, font, "Help", (255, 255, 255), 80)
  while True:
    mouse = pygame.mouse.get_pos()
    clock.tick(30)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if play.isColliding(mouse) == True:
        play.color = (200, 200, 200)
        if event.type == pygame.MOUSEBUTTONDOWN:
          main()
          break
      else:
        play.color = (255, 255, 255)

      if credit.isColliding(mouse) == True:
        credit.color = (200, 200, 200)
        if event.type == pygame.MOUSEBUTTONDOWN:
          credits()
      else:
        credit.color = (255, 255, 255)

      if help_button.isColliding(mouse) == True:
        help_button.color = (200, 200, 200)
        if event.type == pygame.MOUSEBUTTONDOWN:
          help()
      else:
        help_button.color = (255, 255, 255)

    pygame.display.flip()
    screen.fill((0, 0 , 0))
    title.render()
    play.render()
    help_button.render()
    credit.render()

def credits():
  text1 = Text(40, 260, font, "Made by AJDev", (255, 255, 255, 255), 60)
  text2 = Text(70, 310, font, "Made on 5/19/2021", (255, 255, 255, 255), 60)
  text3 = Text(60, 360, font, "Made using python", (255, 255, 255, 255),60)
  text4 = Text(130, 410, font, "and pygame", (255, 255, 255, 255), 60)
  text5 = Text(40, 50, font, "<- Back", (255, 255, 255, 255), 50)
  while True:
    mouse = pygame.mouse.get_pos()
    clock.tick(30)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if text5.isColliding(mouse) == True:
        text5.color = (200, 200, 200)
        if event.type == pygame.MOUSEBUTTONDOWN:
          mainMenu()
          break
      else:
        text5.color = (255, 255, 255)

    pygame.display.flip()
    screen.fill((0, 0 , 0))
    text1.render()
    text2.render()
    text3.render()
    text4.render()
    text5.render()

def help():
  text1 = Text(100, 260, font, "Right and left arrow", (255, 255, 255, 255), 40)
  text2 = Text(90, 310, font, "keys or A and D to move", (255, 255, 255, 255), 40)
  text3 = Text(80, 360, font, "Try not to hit the cars", (255, 255, 255, 255), 40)
  text4 = Text(80, 410, font, "Try to beat the highscore", (255, 255, 255, 255), 40)
  text5 = Text(50, 50, font, "<- Back", (255, 255, 255, 255), 50)
  while True:
    mouse = pygame.mouse.get_pos()
    clock.tick(30)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if text5.isColliding(mouse) == True:
        text5.color = (200, 200, 200)
        if event.type == pygame.MOUSEBUTTONDOWN:
          mainMenu()
          break
      else:
        text5.color = (255, 255, 255)

    pygame.display.flip()
    screen.fill((0, 0 , 0))
    text1.render()
    text2.render()
    text3.render()
    text4.render()
    text5.render()

def gameOver(score):
  with open(r"highscore.dat", "rb") as file:
    highscore = pickle.load(file)

  if score > highscore:
    highscore = score
    with open(r"highscore.dat", "wb") as file:
      pickle.dump(highscore, file)
      
  text1 = Text(40, 90, font, "Game Over", (255, 255, 255, 255), 125)
  retry = Text(30, 700, font, "Retry", (255, 255, 255, 255), 70)
  mainmenu = Text(290, 700, font, "Main Menu", (255, 255, 255, 255), 70)
  score = Text(40, 250, font, f"Score: {score}", (255, 255, 255, 255), 65)

  highscore = Text(40, 330, font, f"Highscore: {highscore}", (255, 255, 255, 255), 65)
  
  while True:
    mouse = pygame.mouse.get_pos()
    clock.tick(30)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if retry.isColliding(mouse) == True:
        retry.color = (200, 200, 200)
        if event.type == pygame.MOUSEBUTTONDOWN:
          main()
          break
      else:
        retry.color = (255, 255, 255)

      if mainmenu.isColliding(mouse) == True:
        mainmenu.color = (200, 200, 200)
        if event.type == pygame.MOUSEBUTTONDOWN:
          mainMenu()
          break
      else:
        mainmenu.color = (255, 255, 255)

    pygame.display.flip()
    screen.fill((0, 0 , 0))
    text1.render()
    retry.render()
    score.render()
    highscore.render()
    mainmenu.render()

def main():
  enemies = pygame.sprite.Group(Enemy(), Enemy())
  player = Player(258, 700, enemies)
  sprites = pygame.sprite.Group(Background(), player)
  score_text = font2.render(f"Score: {player.score}", True, (255, 255, 255))
  count = 0
  fps = 15

  while True:
    clock.tick(fps)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    sprites.update()
    enemies.update()
    screen.blit(score_text, (30, 10))
    pygame.display.flip()

    count += 1
    score_text = font2.render(f"Score: {player.score}", True, (255, 255, 255))
    if count == 30:
      count = 0
      fps += 1
      if player.vel != 10:
        player.vel -= 0.5

    player.isColliding(gameOver)
      

mainMenu()
