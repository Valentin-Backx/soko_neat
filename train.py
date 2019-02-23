import neat
import pickle
import mySoko
import sys

class SokoAppWrapper():
    def __init__(self,genome,n,config):
        self.genome = genome
        self.n = n
        self.config  = config
        self.fitness = 0

    def run(self):
        result = mySoko.SokobanApp(self.genome,self.n,self.config,100000).play(True)
        wonGame = result['wonGame'] #has he won the level?
        nPlays = result['nPlays'] #number of games played?
        playerToCratesScore = result['playerToCratesScore']
        cratesToTargetScore = result['cratesToTargetScore']
        exploredTilesRatio = result['exploredTilesRatio']
        impossibleMoves = result['impossibleMoves']

        self.fitness = wonGame*3000 -impossibleMoves*20 - nPlays*1.5 + playerToCratesScore * 20 + cratesToTargetScore * 500 + exploredTilesRatio * 500

        return self.fitness


def evolutionary_driver(n=100):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,'config')

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(False))

    # p.run(eval_genomes,n)
    pe = neat.ParallelEvaluator(16,eval_genome)

    winner = p.run(pe.evaluate,n=n)

    pickle.dump(winner,open('winner.pkl','wb'))

#fonction monothreadée pour le debuggage
def eval_genomes(genomes,config):
    for genomeid,genome in genomes:
        SokoAppWrapper(genome,50,config).run()

def eval_genome(genome,config):
    top_score=0
    return SokoAppWrapper(genome,50,config).run()


    # return genome.fitness

def main():
    if len(sys.argv)>1:
        evolutionary_driver(int(sys.argv[1]))
    else:
        evolutionary_driver()

if __name__ == "__main__":
    main()