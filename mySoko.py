import pygame
import pygame.locals
import configparser
import imageCache
import game
import agent
global MAP_TILE_WIDTH,MAP_TILE_HEIGHT
global GAME

class Level(object):
    def load_file(self, filename="level.map",headless=False):
        parser = configparser.ConfigParser()
        parser.read(filename)
        
        self.tileset = parser.get("level", "tileset")

        self.map = parser.get("level", "map").split("\n")

        self.tilesize = int(parser.get("level","tilesize"))

        self.width = len(self.map[0])
        self.height = len(self.map)
        if not headless:
            self.groundTile = pygame.transform.scale(pygame.image.load("ground_tile.png").convert_alpha(),(MAP_TILE_WIDTH,MAP_TILE_HEIGHT))
            self.wallTile = pygame.transform.scale(pygame.image.load("wall_tile.png").convert_alpha(),(MAP_TILE_WIDTH,MAP_TILE_HEIGHT))
            self.guy = pygame.transform.scale(pygame.image.load("guy.png").convert_alpha(),(100,100))
            self.crateImage = pygame.transform.scale(pygame.image.load("crate.png").convert_alpha(),(MAP_TILE_WIDTH,MAP_TILE_HEIGHT))
            self.targetImage = pygame.transform.scale(pygame.image.load("target.png").convert_alpha(),(MAP_TILE_WIDTH,MAP_TILE_HEIGHT))

    def getCratesWallsTargets(self):
        crates = []
        walls = []
        targets = []
        for map_y,line in enumerate(self.map):
            for map_x,c in enumerate(line):
                if(c=="b"):
                    crates+=[(map_x,map_y)]
                if(c=="#"):
                    walls+=[(map_x,map_y)]
                if(c=="*"):
                    targets+=[(map_x,map_y)]
        return crates,walls,targets



    def getPlayerPos(self):
        for map_y,line in enumerate(self.map):
            for map_x,c in enumerate(line):
                if(c=="p"):
                    return map_x,map_y
    def getPlayerImage(self):
        return self.guy
    def getCrateImage(self):
        return self.crateImage

    def render(self,screen):

        # image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
        
        # tiles = MAP_CACHE[self.tileset]

        image=None
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if c == "." or c =="p":
                    image=self.groundTile,
                if c == "#":
                    GAME.addWall(map_x,map_y)
                    image = self.wallTile,
                if c == "*":
                    image = self.groundTile,self.targetImage
                for i in image:
                    screen.blit(i,(map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
    


class SokobanApp:
    def __init__(self,genome,maxPlays,config,framerate):
        self.genome = genome
        self.maxPlays = maxPlays
        self.cratesGoalRatio = 0
        self.nPlays = 0
        self.config = config
        self.won = False
        self.framerate = framerate
        self.impossibleMoves=0

    
    def winCallback(self):
        self.game_over=True
        self.won = True

    def setCratesRatio(self,ratio):
        self.cratesGoalRatio = ratio

# if __name__ == "__main__":
    def play(self,hideTraining):
        global MAP_TILE_WIDTH,MAP_TILE_HEIGHT
        global GAME


        MAP_TILE_WIDTH = 100
        MAP_TILE_HEIGHT = 100

        if not hideTraining:
            pygame.init()
            screen = pygame.display.set_mode((1500, 800))

        level = Level()

        level.load_file('level.map',hideTraining)

        GAME_SIZE_X = len(level.map[0])
        GAME_SIZE_Y = len(level.map)

        GAME = game.Game(
            playerPos=level.getPlayerPos(),
            playerImage=None if hideTraining else level.getPlayerImage(),
            crateImage=None if hideTraining else level.getCrateImage(),
            screen=None if hideTraining else screen,
            tileWidth=MAP_TILE_WIDTH,
            tileHeight=MAP_TILE_HEIGHT,
            gameSize =(GAME_SIZE_X,GAME_SIZE_Y),
            winCallback = self.winCallback,
            setCratesRatio = self.setCratesRatio
            )

        if not hideTraining:
            MAP_CACHE = imageCache.TileCache(level.tilesize)

            clock = pygame.time.Clock()

        crates,walls,targets = level.getCratesWallsTargets()
        GAME.addCrates(crates)
        GAME.addWalls(walls)
        GAME.addTargets(targets)

        GAME.addPlayer()

        self.nGroundTiles = GAME_SIZE_X*GAME_SIZE_Y - len(walls) - len(crates) - len(targets) - 1#(Player)

        self.agent = agent.Agent(self.genome,self.config,{"walls":walls,"gameSize":(GAME_SIZE_X,GAME_SIZE_Y),"targetsPos":targets,"playerPos":GAME.player.pos,"cratesPos":crates})

        self.game_over = False


        while not self.game_over:
            if not hideTraining:
                level.render(screen)
                clock.tick(self.framerate)

            moveDecision =  self.agent.moveDecision(GAME.getCratesPos(),GAME.player.pos)
            
            if not hideTraining:
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        self.game_over = True
            res=True
            if not self.game_over:
                if moveDecision == 0:
                    res = GAME.movePlayer(-1,0)
                if moveDecision == 1:
                    res = GAME.movePlayer(1,0)
                if moveDecision == 2:
                    res = GAME.movePlayer(0,-1)
                if moveDecision == 3:
                    res = GAME.movePlayer(0,1)
                if not res:
                    self.impossibleMoves+=1
                self.nPlays+=1

                # elif event.type == pygame.locals.KEYDOWN:
                #     if event.key == pygame.K_LEFT or event.key == ord('q'):
                #         GAME.movePlayer(-1,0)
                #     if event.key == pygame.K_RIGHT or event.key == ord('d'):
                #         GAME.movePlayer(1,0)
                #     if event.key == pygame.K_UP or event.key == ord('z'):
                #         GAME.movePlayer(0,-1)
                #     if event.key == pygame.K_DOWN or event.key == ord('s'):
                #         GAME.movePlayer(0,1)
            
            if self.nPlays>=self.maxPlays:
                self.game_over=True

            if not hideTraining:
                GAME.drawSprites()
                pygame.display.flip()

        playerToCratesScore,cratesToTargetScore = self.agent.getFinalScores()
        
        return {
            "wonGame":self.won,
            "nPlays":self.nPlays,
            "cratesToTargetScore":cratesToTargetScore,
            "playerToCratesScore":playerToCratesScore,
            "exploredTilesRatio":len(GAME.player.tilesExplored)/self.nGroundTiles,
            "impossibleMoves":self.impossibleMoves
        }