import copy

class Environment:
	def __init__(self, map):
		#String matrix representation of the map, A: Agent, C: Crystal, R: Crystal 2, F: Fire, -: Empty
		self.map = map
		self.totalCrystals = 0
		self.collectedCrystals = 0
		self.playerPos = []
		for x in range(0, len(self.map)):
			for y in range(0, len(self.map[0])):#assumes non-jagged
				if self.map[x][y]=="A":
					self.playerPos = [x,y]
				elif self.map[x][y]=="C":
					self.totalCrystals+=1
				elif self.map[x][y]=="R":
					self.totalCrystals+=1
	
	#Create a child clone 
	def child(self):
		environment = Environment(copy.deepcopy(self.map))
		environment.totalCrystals = self.totalCrystals
		environment.collectedCrystals = self.collectedCrystals
		return environment

class State: 
	def __init__(self, environment):
		#Converts an environment into a state as a 3x3 window centred on the agent
		self.state = ""
		x = environment.playerPos[0]
		y = environment.playerPos[1]
		#grab 3x3
		for xi in range(x-1, x+2):
			for yi in range(y-1, y+2):
				#check if in bounds
				if xi>=0 and xi<len(environment.map) and yi>=0 and yi<len(environment.map[x]):
					self.state+=environment.map[xi][yi]
				else:
					self.state+="X"#out of bounds character

#ACTIONS
def MoveLeft(environment):
	if len(environment.playerPos)>0 and environment.playerPos[0]>0:
		playerPos = environment.playerPos
		leftEnvironment = environment.child()
		if leftEnvironment.map[playerPos[0]-1][playerPos[1]]=="C" or leftEnvironment.map[playerPos[0]-1][playerPos[1]]=="R":
			leftEnvironment.collectedCrystals+=1
		
		if leftEnvironment.map[playerPos[0]-1][playerPos[1]]!="F":
			leftEnvironment.map[playerPos[0]-1][playerPos[1]] = "A"
		
		leftEnvironment.map[playerPos[0]][playerPos[1]] = "-"

		return leftEnvironment.child()
	return environment

def MoveRight(environment):
	if len(environment.playerPos)>0 and environment.playerPos[0]<len(environment.map)-1:
		playerPos = environment.playerPos
		rightEnvironment = environment.child()
		if rightEnvironment.map[playerPos[0]+1][playerPos[1]]=="C" or rightEnvironment.map[playerPos[0]+1][playerPos[1]]=="R":
			rightEnvironment.collectedCrystals+=1
		

		if rightEnvironment.map[playerPos[0]+1][playerPos[1]]!="F":
			rightEnvironment.map[playerPos[0]+1][playerPos[1]] = "A"
		
		rightEnvironment.map[playerPos[0]][playerPos[1]] = "-"
		rightEnvironment.playerPos = [playerPos[0]+1, playerPos[1]]
		return rightEnvironment.child()
	return environment

def MoveUp(environment):
	if len(environment.playerPos)>0 and environment.playerPos[1]>0:
		playerPos = environment.playerPos
		upEnvironment = environment.child()
		if upEnvironment.map[playerPos[0]][playerPos[1]-1]=="C" or upEnvironment.map[playerPos[0]][playerPos[1]-1]=="R":
			upEnvironment.collectedCrystals+=1
		
		if upEnvironment.map[playerPos[0]][playerPos[1]-1]!="F":
			upEnvironment.map[playerPos[0]][playerPos[1]-1] = "A"
		
		upEnvironment.map[playerPos[0]][playerPos[1]] = "-"
		upEnvironment.playerPos = [playerPos[0], playerPos[1]-1]
		return upEnvironment.child()
	return environment

def MoveDown(environment):
	if len(environment.playerPos)>0 and environment.playerPos[1]<len(environment.map[0])-1:
		playerPos = environment.playerPos
		downEnvironment = environment.child()
		if downEnvironment.map[playerPos[0]][playerPos[1]+1]=="C" or downEnvironment.map[playerPos[0]][playerPos[1]+1]=="R":
			downEnvironment.collectedCrystals+=1
		

		if downEnvironment.map[playerPos[0]][playerPos[1]+1]!="F":
			downEnvironment.map[playerPos[0]][playerPos[1]+1] = "A"
		
		downEnvironment.map[playerPos[0]][playerPos[1]] = "-"
		downEnvironment.playerPos = [playerPos[0], playerPos[1]+1]
		return downEnvironment.child()
	return environment

#Calculate reward for transitioning into this environment state
def CalculateReward(environmentPrev, environmentCurr):
		reward = 0
		if len(environmentCurr.playerPos)==0:
			reward+= -1000
		if environmentCurr.totalCrystals==environmentCurr.collectedCrystals:
			reward+= 1000

		if environmentCurr.collectedCrystals>environmentPrev.collectedCrystals:
			reward+=5

		reward-=1

		return float(reward)

#
#print (State(env).state)
