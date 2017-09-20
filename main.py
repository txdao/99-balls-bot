# -*- coding: utf-8 -*-
# imports
import neat
import numpy as np
import subprocess
import cv2
import pyscreenshot as ImageGrab
from matplotlib import pyplot as plt
import time
#import mouse control

MIN_MATCH_COUNT = 10
game_area = []

def launch_game_browser(url):
    '''
    launches an instance of the game
    will also move the game window into an appropriate place.
    '''

    command = "cmd /c start chrome " + url + " --new-window"
    subprocess.Popen(command,shell=True)

def get_screen_data():
    im = ImageGrab.grab()
    im.save('screen_grab.png')
    return cv2.imread('screen_grab.png')

def get_game_coords(img):
    '''
    finds the gameplay region
    '''
    template = cv2.imread('game_template_small.png')
    img1 = template
    img2 = img

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w,d = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        coords = [np.int32(dst[0]), np.int32(dst[2])]
        return coords

    else:
        print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
        return None

def init_game_area():
    '''
    create new instance of game
    determine where the game area is
    '''
    # launch browser
    game_url = 'https://www.crazygames.com/assets/99-balls/index.html'
    launch_game_browser(game_url)
    time.sleep(5)
    game_coords = get_game_coords(get_screen_data())
    return game_coords

def get_fitness_score():
    return None

def eval_genomes(genomes, config):
    pass
#    for genome_id, genome in genomes:
#        net = neat.nn.FeedForwardNetwork.create(genome, config)
#        state = get_game_state()
#        action = net.activate(state)
#        perform_action(action)
#        genome.fitness() = get_fitness_score()

def train_neural_net():
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 3000)

    return None

def run():
    # initialize game area
    game_coords = get_game_coords(get_screen_data())
    if game_coords is None:
        game_coords = init_game_area()

    # train neural net
    winner = train_neural_net()

    # save winning data etc (on interupt?).
    pass

if __name__ == '__main__':
    run()