### Author: Michael Brunton-Spall
### Description: Energetic Mechanical Flap
### Category: Games
### License: MIT
### Appname: EMFlap

import pyb
import math
import ugfx
import buttons

ugfx.init()
ugfx.enable_tear()
buttons.init()
buttons.disable_menu_reset()


def play_game():
    grid_size = 8;
    time = 0
    bird_colour = ugfx.YELLOW
    back_colour = ugfx.BLACK
    pipe_colour = ugfx.BLUE
    score = 0
    edge_x = math.floor(ugfx.width()/grid_size)-2
    edge_y = math.floor(ugfx.height()/grid_size)-2
    gap=7

    def draw_bird(x,y):
        ugfx.area((x+1)*grid_size, (y+1)*grid_size, grid_size, grid_size, bird_colour)

    def draw_pipe(x,height):
        ugfx.area((x+1)*grid_size, 0, grid_size, (height+1)*grid_size, pipe_colour)
        ugfx.area((x+1)*grid_size, ((height+gap)*grid_size), grid_size, ugfx.height()-(height+gap)*grid_size, pipe_colour)

    pipe_heights = [13,11,14,11,12,14,13,15,15,17,16]
    ugfx.area(0,0,ugfx.width(), ugfx.height(), back_colour)
    playing = True
    x = 6
    y = 15
    dx = 0
    dy = -2
    time = 0

    def draw_everything():
# We draw the bird at X, and pipes every X*10 locations.
        ugfx.area(0,0,ugfx.width(), ugfx.height(), back_colour)
        draw_bird(x,y)
        ugfx.text(30,10, "Bird %d,%d" % (time,y), ugfx.WHITE)
        for i in range(0,len(pipe_heights)):
            draw_pipe(i*10-time,pipe_heights[i])
    
    start = pyb.millis()
    while playing:
        if buttons.is_pressed("BTN_A"):
            dy = -4

        if buttons.is_pressed("BTN_MENU"):
            break

        if y < 0 or y > 28:
            break
        if x > 200:
            break;

        draw_everything()
        elapsed = pyb.millis()-start
        if elapsed > 100:
            x += dx
            y += dy
            dy += 1
            time += 1
            start = pyb.millis()


ugfx.text(50,120,"Press A to play", ugfx.YELLOW)
running = True
while running:
    play_game()
    ugfx.text(50,120,"You lose!", ugfx.YELLOW)
    ugfx.text(50,140,"Press [A] to Play again", ugfx.YELLOW)
    ugfx.text(50,160,"Press [B] to Quit", ugfx.YELLOW)
    while True:
        if buttons.is_triggered("BTN_A"):
            break
        if buttons.is_triggered("BTN_B"):
            running = False
            break
        pyb.delay(10)
