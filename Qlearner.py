from mdp import *
import random, pickle,copy

#Hyperparameters
totalEpisodes = 100
maxRolloutLength = 50
learningRate = 0.1
discountFactor = 0.95
epsilon = 0.85
epsilonDecay = 0.01
random.seed(1)

actions = ["r", "l", "u", "d"]
qTable = {}#state->actions->values

for i in range(0, totalEpisodes):
	mapInit = [["C","-","-"],["F","-","-"],["A","-","-"]]
	currEnv = Environment(copy.deepcopy(mapInit))
	SARs = []
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


		if random.random()>epsilon:
			action = random.choice(actions)
		if epsilon<1:
			epsilon+=epsilonDecay


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

		SARs.append([state.state, action, reward])
		currEnv = nextEnvironment

		#Check if complete
		if len(currEnv.playerPos)==0 or currEnv.totalCrystals==currEnv.collectedCrystals:
			rolloutComplete = True

	print ("Episode: "+str(i)+" total reward: "+str(totalReward))

	# Q-update
	for j in range(len(SARs)-1, 0, -1):
		oldQValue = 0#assume 0 initialization
		optimalFutureValue = -10

		if SARs[j][0] in qTable.keys():
			if SARs[j][1] in qTable[SARs[j][0]].keys():
				oldQValue = qTable[SARs[j][0]][SARs[j][1]]

			if j+1<len(SARs)-1:
				for a in actions:
					if a in qTable[SARs[j+1][0]].keys():
						if optimalFutureValue < qTable[SARs[j+1][0]][a]:
							optimalFutureValue = qTable[SARs[j+1][0]][a]
			else:
				optimalFutureValue = 0

		newQValue = oldQValue + learningRate*(SARs[j][2] + discountFactor*optimalFutureValue - oldQValue)

		if not SARs[j][0] in qTable.keys():
			qTable[SARs[j][0]] = {}

		qTable[SARs[j][0]][SARs[j][1]] = newQValue

pickle.dump(qTable,open("qTable.pickle", "wb"))



