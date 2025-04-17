import pygame
from datetime import datetime
import sys
import random
import psycopg2
import csv
conn = psycopg2.connect(host="localhost", dbname = "lab10", user = "postgres",
                        password = "Dias2005.", port = 5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS score (
      user_id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL, 
      score VARCHAR(255) NOT NULL

)
""")

pygame.init()
player_name = input("Write your name:")
cur.execute("SELECT score FROM score WHERE name = %s", (player_name,))
row = cur.fetchone()

if row:
    score = int(row[0])
    level = (score // 10) + 1
    print(f"Добро пожаловать обратно, {player_name}! Ваш текущий счёт: {score}, уровень: {level}\n\n")
    input("Push enter for start")
    
else:
    score = 0
    speed = 10
    level = 1
    cur.execute("INSERT INTO score (name, score) VALUES (%s, %s)", (player_name, score))
    conn.commit()
    print(f"Привет, {player_name}! Игрок добавлен.")
    input("Push enter for start")
    
    


    
width , height = 500,500
cell_size = 10
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("SNAKE")
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
snake_pos = [100,100]
snake_body=[[100,100],[80,100],[60,100]]
direction = 'RIGHT'
change_to = direction
clock =pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, (0,0,0))

def border():
    if level == 3 or level == 4:
        pygame.draw.rect(screen,red,pygame.Rect(490,0,cell_size,500))
        pygame.draw.rect(screen,red,pygame.Rect(0,0,cell_size,500))

    elif level > 4:
        pygame.draw.rect(screen,red,pygame.Rect(490,0,cell_size,500))
        pygame.draw.rect(screen,red,pygame.Rect(0,0,cell_size,500))
        pygame.draw.rect(screen,red,pygame.Rect(0,490,500,cell_size))
        pygame.draw.rect(screen,red,pygame.Rect(0,0,500,cell_size))

def game_over_screen():
    global word_score
    screen.fill(red)
    screen.blit(game_over, (30, 250))
    word_score = font.render(f"YOUR SCORE:{score}",True,(0,0,0))
    screen.blit(word_score,(150,255))
    pygame.display.update()
    cur.execute("UPDATE score SET score = %s WHERE name = %s", (score, player_name))
    conn.commit()

    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cur.close()
                conn.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cur.close()
                    conn.close()
                    pygame.quit()
                    sys.exit()




def lev():
    global level 
    global speed
    level = (score // 10)+1
    if level == 2:
        speed = 12
    elif level == 3:
        speed = 14
    elif level == 4:
        speed = 16
    elif level == 5:
        speed = 18
    elif level == 6:
        speed = 20
    elif level == 7:
        speed = 22
    elif level == 8:
        speed = 24                    



class apple():
    def __init__(self):
        self.image = pygame.image.load("apple.png")
        self.image = pygame.transform.scale(self.image,(30,30)) 
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, width - 30), random.randint(30, height - 30))
    def eat(self):
        global sec 
        global score 
        snake_head = pygame.Rect(snake_body[0][0], snake_body[0][1], cell_size, cell_size)
        if snake_head.colliderect(self.rect):
            self.rect.center = (random.randint(30, width - 30), random.randint(30, height - 30))
            score += random.randint(1,3)
            return True
        return False
    
   
last_respawn_time = 0
app = apple()

Running = True

while Running:

    now = datetime.now()
    sec = now.second

    if (sec % 8) == 0 and (now.second != last_respawn_time):
        app.rect.center = (random.randint(30, width - 30), random.randint(30, height - 30))
        last_respawn_time = now.second


    screen.fill(black)
    screen.blit(app.image,app.rect)
    app.eat()\

    border()

    font = pygame.font.SysFont("Verdana", 15)
    word_score = font.render(f"SCORE:{score}",True,(255,255,255))
    screen.blit(word_score,(10,10))

    lev()
    word_level = font.render(f"LEVEL:{level}",True,(255,255,255))
    screen.blit(word_level,(430,10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != "UP":
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = 'LEFT'  
    direction = change_to

    if  direction == 'UP':
        snake_pos[1] = (snake_pos[1]-cell_size)% height
    elif direction == 'DOWN':
        snake_pos[1] = (snake_pos[1] + cell_size)%height
    elif direction == 'RIGHT':
        snake_pos[0]= (snake_pos[0] + cell_size)%width 
    elif direction == 'LEFT':
        snake_pos[0] = (snake_pos[0] - cell_size)%width 
 
    snake_body.insert(0,list(snake_pos))
    if not app.eat():
        snake_body.pop()
    

    for block in snake_body:
        pygame.draw.rect(screen,green,pygame.Rect(block[0],block[1],cell_size,cell_size))

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            Running = False
            game_over_screen()
        elif level == 3 or level == 4 :
            if snake_pos[0] == 10 or snake_pos[0] == 480:
                Running = False
                game_over_screen()
        elif level > 4 :
            if snake_pos[0] == 10 or snake_pos[0] == 480:
                Running = False
                game_over_screen()
            if snake_pos[1] == 10 or snake_pos[1] == 480:
                Running = False
                game_over_screen()


    pygame.display.flip()
    clock.tick(speed)
