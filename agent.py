import neat

#ground is 0/5
#player is 1/5
#target is 2/5
#crate is 3/5
#wall is 4/5

class Agent:
	def __init__(self,genome,config,gameParameters):
		self.genome=genome
		self.neural_network = neat.nn.FeedForwardNetwork.create(genome,config)
		self.walls = gameParameters["walls"]
		self.gameSize = gameParameters["gameSize"]

		self.targets = gameParameters["targetsPos"]

		self.startPlayerAccumulatedDist = self.calculatePlayerDistScore(gameParameters["cratesPos"],gameParameters["playerPos"])
		self.startCratesAccumulatedDist = self.calculateCratesToTargetsDistScore(gameParameters["cratesPos"],gameParameters["targetsPos"])

	def getFinalScores(self):
		return ((self.startPlayerAccumulatedDist-self.calculatePlayerDistScore(self.crates,self.player))/self.startPlayerAccumulatedDist
			,(self.startCratesAccumulatedDist-self.calculateCratesToTargetsDistScore(self.crates,self.targets))/self.startCratesAccumulatedDist)

	def calculatePlayerDistScore(self,crates,player):
		res=0
		pX,pY = player
		for c in crates:
			res+=((abs(c[0]-pX)**2 + abs(c[1]-pY)**2)**1/2)

		return res

	def calculateCratesToTargetsDistScore(self,crates,targets):
		res=0
		for c in crates:
			for t in targets:
				tx,ty = t
				res+=((abs(c[0]-tx)**2 + abs(c[1]-ty)**2)**1/2)
		return res

	def moveDecision(self,crates,player):
		self.crates = crates
		self.player = player

		game = [0] * (self.gameSize[0] * self.gameSize[1])


		for wall in self.walls:
			# walls+=[(wall[0]-player[0])/self.gameSize[0],(wall[1]-player[1])/self.gameSize[1]]
			game[wall[0]*wall[1]]=1 #wall is 1

		for x in self.crates:
			game[x[0]*x[1]] = 3/5 #crate is 3

		game[self.player[0]*self.player[1]] = 1/5

		for t in self.targets:
			game[t[0]*t[1]] = 2/5

		input =tuple(
			game
		)
			
		output = self.neural_network.activate(input)

		return output.index(max(output))
