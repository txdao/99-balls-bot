# -*- coding: utf-8 -*-
# imports
import neat
import webbrowser
#import screen grab
#import mouse control


def launch_game_browser():
    pass

def get_screen_img():
    return None

def get_game_coords(img):
    return None

def init_game_area():
    '''
    create new instance of game
    determine where the game area is
    '''
    # launch browser to https://www.crazygames.com/assets/99-balls/index.html
    launch_game_browser()
    screen_img = get_screen_img()
    game_coords = get_game_coords(screen_img)



    pass

def run():
    # initialize game area
    init_game_area()

    # train neural net

    # save winning data etc (on interupt?).
    pass

if __name__ == '__main__':
    run()