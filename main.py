# -*- coding: utf-8 -*-
# imports
import neat
import game_wrapper
#from matplotlib import pyplot as plt
import cv2
import os
import time
#import mouse control

def get_fitness_score():
    """
    given some information from the previous play,
    compute a score for the gene.
    """
    return None

def eval_genomes(genomes, config):
    pass
#    for genome_id, genome in genomes:
#        net = neat.nn.FeedForwardNetwork.create(genome, config)
#        state = get_game_state()
#        action = net.activate(state)
#        perform_action(action)
#        genome.fitness() = get_fitness_score()

def train_neural_net(games):
    """
    Prepares configuration file,
    runs simulation until fitness threshold or max iterations is reached
    """
    return None
    # Load configuration.
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config-feedforward')
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
    game = game_wrapper.Game(use_existing_game=True)
    game.start_game()
    time.sleep(1)
    game.current_screen_img = game.get_screen_data()
    cv2.imwrite("screen.png", game.current_screen_img)
    print(game.get_ball_value(0,3))

    # train neural net
    winner = train_neural_net(game)

    # save winning data etc (on interupt?).
    return game

if __name__ == '__main__':
    run()