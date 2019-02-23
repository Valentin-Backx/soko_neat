import neat
import pickle
import mySoko

genome = pickle.load(open('winner.pkl','rb'))

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,'config')

result,genome = mySoko.SokobanApp(genome,50,config,15).play(False)




score = result['score'] #ration crate@target/nTotalCrates ?
wonGame = result['wonGame'] #has he won the level?
nPlays = result['nPlays'] #number of games played?
playerToCratesScore = result['playerToCratesScore']
cratesToTargetScore = result['cratesToTargetScore']
exploredTilesRatio = result['exploredTilesRatio']

fitness = wonGame*3000 + 1000*score - nPlays*1.5 + playerToCratesScore * 100 + cratesToTargetScore * 500 + exploredTilesRatio * 500

print("wongame ",wonGame," score ",score," nPlays ",nPlays," playerToCratesScore ",playerToCratesScore," cratesToTargetScore ",cratesToTargetScore," exploredTilesRatio ",exploredTilesRatio)

print("fitness: "+str(fitness))