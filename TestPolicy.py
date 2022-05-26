from mdp import *
import pickle,random

#Load agent
qTable = pickle.load(open("qTable.pickle", "rb"))
maxRolloutLength = 50

mapInit = [["C","-","-"],["F","-","R"],["A","-","-"]]
currEnv = Environment(copy.deepcopy(mapInit))

actions = ["r", "l", "u", "d"]


rolloutComplete = False
rolloutIndex = 0
totalReward = 0

while rolloutIndex < maxRolloutLength and not rolloutComplete:
	rolloutIndex+=1

	state = State(currEnv)

	#Action Selection
	action = random.choice(actions)
	if state.state in qTable.keys():
		maxAction = action
		maxValue = -1000

		for a in actions:
			if a in qTable[state.state].keys():
				if maxValue < qTable[state.state][a]:
					maxValue = qTable[state.state][a]
					maxAction = a
		action = maxAction
	else:
		action = random.choice(actions)


	#s_(t+1) <- s_t
	nextEnvironment = currEnv.child()

	if action=="r":
		nextEnvironment = MoveRight(nextEnvironment)
	elif action =="l":
		nextEnvironment = MoveLeft(nextEnvironment)
	elif action =="u":
		nextEnvironment = MoveUp(nextEnvironment)
	elif action =="d":
		nextEnvironment = MoveDown(nextEnvironment)

	reward = CalculateReward(currEnv, nextEnvironment)
	totalReward+=reward

	currEnv = nextEnvironment

	#Check if complete
	if len(currEnv.playerPos)==0 or currEnv.totalCrystals==currEnv.collectedCrystals:
		rolloutComplete = True

print ("Total Reward: "+str(totalReward))

