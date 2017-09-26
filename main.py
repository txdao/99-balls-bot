# -*- coding: utf-8 -*-
# imports
import neat
import game_wrapper
import os
import time
import numpy as np

TARGET_LEVEL = 100
game = game_wrapper.Game(use_existing_game=True)

def get_fitness_score(state, new_state, level):
    """
    given some information from the previous play,
    compute a score for the gene.
    """
    diff = state[:-1] - new_state[1:]
    removed = np.sum(diff)
    n_balls = np.sum(state)
    f_ball_removed = removed/n_balls

    lowest_ball = 0
    for i in range(7, 0, -1):
        if sum(new_state[i]) > 0:
            lowest_ball = i
            break

    f_lowest_ball = (lowest_ball+1)/8
    f_level = level/TARGET_LEVEL
    score = f_ball_removed + f_level - 2*f_lowest_ball
    return score, f_ball_removed, f_lowest_ball, f_level

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        score = 1
        f_ball_history = []

        while score > 0:
            state, circle_location = game.update_game_state()
            state_ = state.reshape(-1, 1)
            action = net.activate(np.append(state_, circle_location))
            game.release_circle((action[0]-.5)*90)
            game.current_level_img = game.get_current_level_img()
            while not game.is_new_level:
                time.sleep(.1) #wait until next level
                game.is_new_level = game.check_if_new_level()
            new_state, _ = game.update_game_state()
            level = 1
            score, f_ball_removed, _, _ = get_fitness_score(state, new_state, level)
            f_ball_history.append(f_ball_removed)

        genome.fitness = np.mean(f_ball_history) + level/100
        game.reset_game()

def train_neural_net(games):
    """
    Prepares configuration file,
    runs simulation until fitness threshold or max iterations is reached
    """
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
    try:
        game.start_game()
        time.sleep(1)

        # train neural net
        winner = train_neural_net(game)

        # save winning data etc (on interupt?).
        return game
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run()