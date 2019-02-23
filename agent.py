import neat

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
		walls = []
		for wall in self.walls:
			# walls+=[(wall[0]-player[0])/self.gameSize[0],(wall[1]-player[1])/self.gameSize[1]]
			walls+=[(wall[0])/self.gameSize[0],(wall[1])/self.gameSize[1]]
		lenWall = len(walls)
		for w in range(0,39-int(lenWall/2)):
			walls+=[0,0] #on considere maxi 40 murs, on met des 0 pour les murs absents [PROBLEME DE GENERALISATION (OVERFITTING)]

		cratesRelToPlayer = []
		for crate in crates:
			cratesRelToPlayer+=[(crate[0]-player[0])/self.gameSize[0],(crate[1]-player[1])/self.gameSize[1]]
			# cratesRelToPlayer+=[(crate[0])/self.gameSize[0],(crate[1])/self.gameSize[1]]

		cratesRelToTargets = []
		for crate in crates:
			for target in self.targets:
				cratesRelToTargets+=[(crate[0]-target[0])/self.gameSize[0],(crate[1]-target[1])/self.gameSize[1]]

		input =tuple(
			#[self.gameSize[0],self.gameSize[1]]+
			walls+#walls positions relative to player (on considère maxi 40 murs)
			cratesRelToPlayer+#crates positions relative to player
			cratesRelToTargets
		)
			
		ouput = self.neural_network.activate(input)

		o = ouput[0]
		# print(o)
		if(o > 0 and o<0.25):
			return 0
		if(o>=0.25 and o<0.5):
			return 1
		if o>=0.5 and o<0.75:
			return 2
		if o >=0.75 and o <=1:
			return 3
		

