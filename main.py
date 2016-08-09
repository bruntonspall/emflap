### Author: Michael Brunton-Spall
### Description: Energetic Mechanical Flap
### Category: Games
### License: MIT
### Appname: EMFlap

import pyb
import math
import ugfx
import buttons
import database

ugfx.init()
ugfx.enable_tear()
buttons.init()
buttons.disable_menu_reset()

score = 0
grid_size = 8;
bird_colour = ugfx.YELLOW
back_colour = ugfx.BLACK
pipe_colour = ugfx.BLUE
edge_x = math.floor(ugfx.width()/grid_size)-2
edge_y = math.floor(ugfx.height()/grid_size)-2
gap=8
high_score = database.database_get("emflap.highscore",0)

def play_game():
    global score
    pipe_heights = []
    score = 0
    playing = True
    x = 6
    y = 17
    dx = 1
    dy = -2

    def randint(lower, upper):
        return (pyb.rng() % (upper-lower))+lower


    def randomise_pipes():
        pipe_heights = [13, 11, 16]
        last_height = 17
        for i in range(0,50):
            r = randint(last_height-5,last_height+5)
            if r > 22: 
                r = 22
            if r < 8:
                r = 8
            pipe_heights.append(r)
            last_height = r
        return pipe_heights

    def draw_bird(x,y):
        ugfx.area((x+1)*grid_size, (y+1)*grid_size, grid_size, grid_size, bird_colour)

    def draw_pipe(x,height):
        ugfx.area((x+1)*grid_size, 0, grid_size, (height+1)*grid_size, pipe_colour)
        ugfx.area((x+1)*grid_size, ((height+gap)*grid_size), grid_size, ugfx.height()-(height+gap)*grid_size, pipe_colour)

    def draw_everything():
# We draw the bird at X, and pipes every X*10 locations.
        ugfx.area(0,0,ugfx.width(), ugfx.height(), back_colour)
        draw_bird(10,y)
        for i in range(0,len(pipe_heights)):
            draw_pipe(10+i*10-x,pipe_heights[i])
        #ugfx.text(30,10, "Bird %d,%d Pipe: %d,%d" % (x,y,pipe_heights[x//10],pipe_heights[x//10]+gap), ugfx.WHITE)
        ugfx.text(30,10, "Score %d" % (score), ugfx.WHITE)
    
    pipe_heights = randomise_pipes()
    start = pyb.millis()
    while playing:
        if buttons.is_pressed("BTN_A"):
            dy = -2

        if buttons.is_pressed("BTN_MENU"):
            break

        if y < 0 or y > 30:
            break
        if x > 500:
            break

        elapsed = pyb.millis()-start
        if elapsed > 100:
            draw_everything()
            if x % 10 == 0:
                score += 1
                if y <= pipe_heights[x//10]:
                    break
                if y >= pipe_heights[x//10]+gap:
                    break
            x += dx
            y += dy
            dy += 1
            start = pyb.millis()


ugfx.text(50,120,"Press A to play", ugfx.YELLOW)
running = True
while running:
    play_game()
    ugfx.text(50,100,"You lose!", ugfx.YELLOW)
    ugfx.text(50,120,"Score: %d" % (score), ugfx.YELLOW)
    if score > high_score:
        ugfx.text(50,140, "New High Score: %d" % (score), ugfx.YELLOW)
        high_score = score
        database.database_set("emflap.highscore",high_score)
    else:
        ugfx.text(50,140, "High Score: %d" % (high_score), ugfx.YELLOW)

    ugfx.text(50,180,"Press [A] to Play again", ugfx.YELLOW)
    ugfx.text(50,200,"Press [B] to Quit", ugfx.YELLOW)
    while True:
        if buttons.is_triggered("BTN_A"):
            break
        if buttons.is_triggered("BTN_B"):
            running = False
            break
        pyb.delay(10)
