# -*- coding: utf-8 -*-
# imports
import neat
import game_wrapper
import os
import time

game = game_wrapper.Game(use_existing_game=True)

def get_fitness_score(state, new_state):
    """
    given some information from the previous play,
    compute a score for the gene.
    """
    return None

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        state, circle_location = game.update_game_state()

        action = net.activate([state, circle_location])
        game.release_circle(action)
        new_state = game.update_game_state()
        genome.fitness = get_fitness_score(state, new_state)

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
    game.start_game()
    time.sleep(1)

    # train neural net
    winner = train_neural_net(game)

    # save winning data etc (on interupt?).
    return game

if __name__ == '__main__':
    run()