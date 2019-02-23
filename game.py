import pygame

class Game:
    def __init__(self,**kwargs):#,playerPos, playerImage,crateImage,screen):
        self.crates = []
        self.walls = []
        self.targets = []
        self.playerImage = kwargs["playerImage"]
        self.crateImage = kwargs["crateImage"]
        self.screen = kwargs["screen"]
        self.playerPos = kwargs["playerPos"]
        self.MAP_TILE_WIDTH = kwargs["tileWidth"]
        self.MAP_TILE_HEIGHT = kwargs["tileHeight"]
        self.GAME_SIZE_X = kwargs["gameSize"][0]
        self.GAME_SIZE_Y = kwargs["gameSize"][1]
        self.win = kwargs["winCallback"]
        self.setCratesRatio = kwargs["setCratesRatio"]

    def drawSprites(self):
        for x in self.crates:
            x.draw()
        self.player.draw()

    def isThereanything(self,pos):
        for x in self.crates:
            if x.pos==pos:
                return True
        for x in self.walls:
            if x.pos==pos:
                return True
        return False               

    def isValidPos(self,nextPos):
        return not(nextPos[0] < 0 or nextPos[1] < 0 or nextPos[0] > self.GAME_SIZE_X-1 or nextPos[1] > self.GAME_SIZE_Y-1)

    def canGo(self,x,y,dir):
        nextPos = (x+dir[0],y+dir[1])

        if not self.isValidPos((x,y)):
            return False

        for crate in self.crates:
            if crate.pos==(x,y):
                if self.isThereanything(nextPos) or not self.isValidPos(nextPos):
                    return False#la caisse est bloquée par un mur ou par une autre caisse
                else:#on pousse la caisse
                    self.moveCrate(crate,dir)
                    return True
        for w in self.walls:
            if w.pos==(x,y):
                return False
        #il n'y a rien
        return True

    def moveCrate(self,crate,dir):
        crate.move(dir)
        nCrateOnGoal = 0

        for crate in self.crates:
            for target in self.targets:
                if(crate.pos==target):
                    nCrateOnGoal+=1

        self.setCratesRatio(nCrateOnGoal/len(self.crates))
        if nCrateOnGoal==len(self.crates):
            self.win()

    def movePlayer(self,dirX,dirY):


        cg =  self.canGo(
            self.player.pos[0]+dirX,
            self.player.pos[1]+dirY,
            (dirX,dirY)
            )
        if cg:
            self.player.move((dirX,dirY))
        return cg

    def addCrates(self,crates):
        for c in crates:
            self.addCrate(c[0],c[1])

    def addCrate(self,x,y):
        self.crates+=[Crate((x,y),(self.MAP_TILE_HEIGHT,self.MAP_TILE_WIDTH),self.crateImage,self.screen)]
        return self

    def getCratesPos(self):
        return [c.pos for c in self.crates]

    def addWalls(self,walls):
        for w in walls:
            self.addWall(w[0],w[1])

    def addWall(self,x,y):
        self.walls+=[Wall((x,y))]
        return self


    def addPlayer(self):
        self.player = Player(self.playerPos,(self.MAP_TILE_HEIGHT,self.MAP_TILE_WIDTH),self.playerImage,self.screen)

    def addTargets(self,targets):
        self.targets = targets

class Player(pygame.sprite.Sprite):
    def __init__(self, pos,tileSize, playerImage,screen, frames=None):
        super(pygame.sprite.Sprite, self).__init__()
        self.pos = pos
        if playerImage:
            screen.blit(playerImage,(pos[0]*tileSize[0],pos[1]*tileSize[1]))
            self.tileSize = tileSize
            self.screen = screen
            self.playerImage = playerImage
        self.tilesExplored = [self.pos]

    def move(self,dir):
        self.pos = (self.pos[0]+dir[0],self.pos[1]+dir[1])
        if(not self.pos in self.tilesExplored):
            self.tilesExplored += [self.pos]
        # self.rect.x = self.pos[0]*self.tileSize[0]
        # self.rect.y = self.pos[1]*self.tileSize[1]

    def draw(self):
        self.screen.blit(self.playerImage,(self.pos[0]*self.tileSize[0],self.pos[1]*self.tileSize[1]))


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, frames=None):
        super(pygame.sprite.Sprite, self).__init__()
        self.pos = pos

class Crate(pygame.sprite.Sprite):
    def __init__(self, pos,tileSize, crateImage,screen,frames=None):
        super(pygame.sprite.Sprite, self).__init__()
        self.pos = pos
        if crateImage:
            self.screen = screen
            screen.blit(crateImage,(pos[0]*tileSize[0],pos[1]*tileSize[1]))
            self.crateImage = crateImage
            self.tileSize = tileSize

    def move(self,dir):
        self.pos = (self.pos[0]+dir[0],self.pos[1]+dir[1])
        # self.rect.x = dir[0]
        # self.rect.y = dir[1]

    def draw(self):
        self.screen.blit(self.crateImage,(self.pos[0]*self.tileSize[0],self.pos[1]*self.tileSize[1]))


