# Step 1
# Script for creating intial pseudo-randomized list of stimuli (without practice trials)
# Creates reference sheet to use for making other counterbalanced lists

import random
import csv

with open("pairs1.txt", "U") as f:
    pairs = f.readlines()

pairs = [line.rstrip("\n") for line in pairs]

# Second half of target items
# example: arm.jpg;bottle.jpg;pepper.jpg;clock.jpg;arch.jpg
# First item = target (competitor from pairs1.txt set)
# etc.
# Fifth item = competitor (target from pairs1.txt set)
with open("pairs2.txt", "U") as f:
    pairs2 = f.readlines()

pairs2 = [line.rstrip("\n") for line in pairs2]

### Prepare to create filler trials
# Read in list of filler items
with open("fillers.txt", "U") as f:
    fillers = f.readlines()

fillers = [line.rstrip("\n") for line in fillers]

# Trial length is variable
# Each trial can include either 2, 3, or 4 actions
len2 = []
len3 = []
len4 = []

# Equally divide filler items to trial lengths
random.shuffle(fillers)
for i in range(1, 33):
    len2.append(fillers.pop())

for i in range(1, 49):
    len3.append(fillers.pop())

len4 = fillers[:]

# Randomize list of candidate fillers for len2 trials, assign to blocks
# Assign half (or 1/3 or 1/4) to event1 (filler1_len2) and half to event2 (filler2_len2)
# Assign half (or 1/3 or 1/4) to block1, half to block2
random.shuffle(len2)
random.shuffle(len3)
random.shuffle(len4)

fillerLists = {"filler1_len2_block1": len2[0:8],
				"filler1_len2_block2": len2[8:16],
				"filler2_len2_block1": len2[16:24],
				"filler2_len2_block2": len2[24:32],
				"filler1_len3_block1": len3[0:8],
				"filler1_len3_block2": len3[8:16],
				"filler2_len3_block1": len3[16:24],
				"filler2_len3_block2": len3[24:32],
				"filler3_len3_block1": len3[32:40],
				"filler3_len3_block2": len3[40:48],
				"filler1_len4_block1": len4[0:8],
				"filler1_len4_block2": len4[8:16],
				"filler2_len4_block1": len4[16:24],
				"filler2_len4_block2": len4[24:32],
				"filler3_len4_block1": len4[32:40],
				"filler3_len4_block2": len4[40:48],
				"filler4_len4_block1": len4[48:56],
				"filler4_len4_block2": len4[56:64]}

# Create empty lists to store finished trials
finishedFillerTrials = {"fillerTrials_len2_block1": [],
						"fillerTrials_len2_block2": [],
						"fillerTrials_len3_block1": [],
						"fillerTrials_len3_block2": [],
						"fillerTrials_len4_block1": [],
						"fillerTrials_len4_block2": []}

# For each of the filler trials, randomly pick an action for each event in trial (each action only used once)
# Filler trial building function
def buildFillerTrials(trialLength, block):
    import random
    # Four possible actions per trial
    actions = ["rotate", "fade", "expand", "shrink"]

    # For trials with less than 4 events, use placeholder
    placeholder = "nothing.jpg static"

    # For filler trials, there is no competitor, use placeholder2
    placeholder2 = ";nothing.jpg"

    item1 = "filler1_len" + str(trialLength) + "_block" + str(block)
    item1 = fillerLists[item1]

    item2 = "filler2_len" + str(trialLength) + "_block" + str(block)
    item2 = fillerLists[item2]

    if trialLength > 2:
        item3 = "filler3_len" + str(trialLength) + "_block" + str(block)
        item3 = fillerLists[item3]

    if trialLength > 3:
        item4 = "filler4_len" + str(trialLength) + "_block" + str(block)
        item4 = fillerLists[item4]

    for i in range(0, len(item1)):
        action1 = random.sample(actions, 1)
        event1 = item1[i] + " " + action1[0]
        sub_actions = [x for x in actions if x != action1[0]]
        action2 = random.sample(sub_actions, 1)
        event2 = item2[i] + " " + action2[0]

        if trialLength > 2:
            sub_actions2 = [x for x in sub_actions if x != action2[0]]
            action3 = random.sample(sub_actions2, 1)
            event3 = item3[i] + " " + action3[0]

        if trialLength > 3:
            action4 = [x for x in sub_actions2 if x != action3[0]]
            event4 = item4[i] + " " + action4[0]

        if trialLength == 2:
            output = "fillerTrials_len2" + "_block" + str(block)
            finishedFillerTrials[output].append("2;" + event1 + ";" + event2 + ";" + placeholder + ";" + placeholder + placeholder2)

        if trialLength == 3:
            output = "fillerTrials_len3" + "_block" + str(block)
            finishedFillerTrials[output].append("3;" + event1 + ";" + event2 + ";" + event3 + ";" + placeholder + placeholder2)

        if trialLength == 4:
            output = "fillerTrials_len4" + "_block" + str(block)
            finishedFillerTrials[output].append("4;" + event1 + ";" + event2 + ";" + event3 + ";" + event4 + placeholder2)

# Loop through lists for different sets of filler trials to make
# Three lengths
fillerLens = [2, 3, 4]
# Two blocks
fillerBlocks = [1, 2]

for lens in fillerLens:
    for blocks in fillerBlocks:
        buildFillerTrials(lens, blocks)

# Assign 1/2 of fillers in each block to A and 1/2 in each to B
finishedFillerTrials_blocked = {}
	
def assignBlocks(fillerList):
	for lens in fillerLens:
		for blocks in fillerBlocks:
			i = "fillerTrials_len" + str(lens) + "_block" + str(blocks)
			currentList = fillerList[i]
			j = i + "A"
			finishedFillerTrials_blocked[j] = currentList[0:4]
			k = i + "B"
			finishedFillerTrials_blocked[k] = currentList[4:8]

assignBlocks(finishedFillerTrials)

### Prepare to create target trials
# Equally divide target pairs into A vs. B blocks
# First 12 after randomizing go to A blocks
aBlockPair1 = random.sample(pairs, 12)

# Remaining 12 go to B blocks
bBlockPair1 = [x for x in pairs if x not in aBlockPair1]

# Start with empty lists for pair 2 items
aBlockPair2 = []
bBlockPair2 = []

# Find original index of pair1 item assigned to A block
# Use that index to find corresponding item in pair2
# Assign that item to B block
for i in aBlockPair1:
    bBlockPair2.append(pairs2[pairs.index(i)])

for i in bBlockPair1:
    aBlockPair2.append(pairs2[pairs.index(i)])

# Assign half of items to len3, half to len4
aBlock_pair1_len3 = aBlockPair1[0:6]
aBlock_pair1_len4 = aBlockPair1[6:12]

aBlock_pair2_len3 = aBlockPair2[0:6]
aBlock_pair2_len4 = aBlockPair2[6:12]

# Alternate which items are len3 vs. len4
bBlock_pair1_len3 = bBlockPair1[6:12]
bBlock_pair1_len4 = bBlockPair1[0:6]

bBlock_pair2_len3 = bBlockPair2[6:12]
bBlock_pair2_len4 = bBlockPair2[0:6]

aBlock_len3 = aBlock_pair1_len3 + aBlock_pair2_len3
aBlock_len4 = aBlock_pair1_len4 + aBlock_pair2_len4

bBlock_len3 = bBlock_pair2_len3 + bBlock_pair1_len3
bBlock_len4 = bBlock_pair2_len4 + bBlock_pair1_len4

blockLists = {"aBlock_len3": aBlock_len3, 
				"aBlock_len4": aBlock_len4, 
				"bBlock_len3": bBlock_len3, 
				"bBlock_len4": bBlock_len4}
targetLists = {}

def separateFilenames(trialLength, block):
    target = "target_len" + str(trialLength) + "_block" + block
    targetLists[target] = []
    nontarget1 = "nontarget1_len" + str(trialLength) + "_block" + block
    targetLists[nontarget1] = []
    nontarget2 = "nontarget2_len" + str(trialLength) + "_block" + block
    targetLists[nontarget2] = []
    nontarget3 = "nontarget3_len" + str(trialLength) + "_block" + block
    targetLists[nontarget3] = []
    competitor = "competitor_len" + str(trialLength) + "_block" + block
    targetLists[competitor] = []

    loopThrough = block.lower() + "Block_len" + str(trialLength)
    currentList = blockLists[loopThrough]

    for i in currentList:
        names = i.split(";")
        targetLists[target].append(names[0])
        targetLists[nontarget1].append(names[1])
        targetLists[nontarget2].append(names[2])
        targetLists[nontarget3].append(names[3])
        targetLists[competitor].append(names[4])

# Two trial lengths
targetLens = [3, 4]
# Two blocks
targetBlocks = ["A", "B"]

for lens in targetLens:
    for blocks in targetBlocks:
        separateFilenames(lens, blocks)

finishedTargetTrials = {"len3_aBlockGiven": [],
						"len3_bBlockGiven": [],
						"len3_aBlockNew": [],
						"len3_bBlockNew": [],
						"len4_aBlockGiven": [],
						"len4_bBlockGiven": [],
						"len4_aBlockNew": [],
						"len4_bBlockNew": []}

def buildTargetTrials(trialLength, block, condition):
    import random
    actions = ["rotate", "fade", "expand", "shrink"]
    placeholder = "nothing.jpg static"

    item1 = "target_len" + str(trialLength) + "_block" + block
    item1 = targetLists[item1]
	
    item2 = "nontarget1_len" + str(trialLength) + "_block" + block
    item2 = targetLists[item2]

    item3 = "nontarget2_len" + str(trialLength) + "_block" + block
    item3 = targetLists[item3]

    if trialLength > 3:
        item4 = "nontarget3_len" + str(trialLength) + "_block" + block
        item4 = targetLists[item4]

    competitors = "competitor_len" + str(trialLength) + "_block" + block
    competitors = targetLists[competitors]

    for i in range(0, len(item1)):
        # in given (repeated) conditions, target item appears in action1 and action3
        if condition == "Given":
            action1 = random.sample(actions, 1)
            event1 = item1[i] + " " + action1[0]
            sub_actions = [x for x in actions if x != action1[0]]
            action2 = random.sample(sub_actions, 1)
            event2 = item2[i] + " " + action2[0]
            sub_actions2 = [x for x in sub_actions if x != action2[0]]
            action3 = random.sample(sub_actions2, 1)
            event3 = item1[i] + " " + action3[0]

        # in new (non-repeated) conditions, target item only appears in action3
        elif condition == "New":
            action1 = random.sample(actions, 1)
            event1 = item2[i] + " " + action1[0]
            sub_actions = [x for x in actions if x != action1[0]]
            action2 = random.sample(sub_actions, 1)
            event2 = item3[i] + " " + action2[0]
            sub_actions2 = [x for x in sub_actions if x != action2[0]]
            action3 = random.sample(sub_actions2, 1)
            event3 = item1[i] + " " + action3[0]

        if trialLength > 3:
            action4 = [x for x in sub_actions2 if x != action3[0]]
            event4 = item4[i] + " " + action4[0]

        if trialLength == 3:
            output = "len3" + "_" + block.lower() + "Block" + condition
            finishedTargetTrials[output].append("3;" + event1 + ";" + event2 + ";" + event3 + ";" + placeholder + ";" + competitors[i])

        if trialLength == 4:
            output = "len4" + "_" + block.lower() + "Block" + condition
            finishedTargetTrials[output].append("4;" + event1 + ";" + event2 + ";" + event3 + ";" + event4 + ";" + competitors[i])

targetConditions = ["Given", "New"]

for lens in targetLens:
    for blocks in targetBlocks:
        for conds in targetConditions:
            buildTargetTrials(lens, blocks, conds)

# Assign trials to Block1 vs. Block2
# 12 of aBlockGivenTrials go to block1, other 12 go to block2
# 6 from pair1 and 6 from pair2
# Within trial lists, 0:12 = pair1
# Within trial lists, 12:24 = pair2
allIndices = {}

def getIndices(trialLength, outputFile):
	import random
	
	rangeIndices = range(0, 12)
	
	# Get indices to choose three trials from pair1 (then pair2) for repeated condition in block 1A
	aBlockGiven_1A_pair1_index = random.sample(rangeIndices[0:6], 3)
	aBlockGiven_1A_pair2_index = random.sample(rangeIndices[6:12], 3)
	
	# 6 possible repeated trials for pair1
	rangeIndices_2 = range(0, 6)
	# Remove 3 chosen above from possible repeated trials
	for index in aBlockGiven_1A_pair1_index:
		if index in rangeIndices_2:
			rangeIndices_2.remove(index)
	
	# Trials that weren't chosen for repeated in block 1A will be non-repeated instead
	aBlockNew_1A_pair1_index = rangeIndices_2
	
	# 6 possible repeated trials for pair2
	rangeIndices_3 = range(6, 12)
	# Remove 3 chosen above from possible repeated trials
	for index in aBlockGiven_1A_pair2_index:
		if index in rangeIndices_3:
			rangeIndices_3.remove(index)
	
	# Trials that weren't chosen for repeated in block 1A will be non-repeated instead
	aBlockNew_1A_pair2_index = rangeIndices_3
	
	outputFile["len" + str(trialLength) + "_aBlockGiven_1A_pair1_index"] = aBlockGiven_1A_pair1_index
	outputFile["len" + str(trialLength) + "_aBlockGiven_1A_pair2_index"] = aBlockGiven_1A_pair2_index
	outputFile["len" + str(trialLength) + "_aBlockNew_1A_pair1_index"] = aBlockNew_1A_pair1_index
	outputFile["len" + str(trialLength) + "_aBlockNew_1A_pair2_index"] = aBlockNew_1A_pair2_index
	
	# If repeated in 1A, non-repeated in 2A
	# If non-repeated in 1A, repeated in 2A
	aBlockNew_2A_pair1_index = aBlockGiven_1A_pair1_index
	aBlockGiven_2A_pair1_index = aBlockNew_1A_pair1_index
	aBlockNew_2A_pair2_index = aBlockGiven_1A_pair2_index
	aBlockGiven_2A_pair2_index = aBlockNew_1A_pair2_index
	
	outputFile["len" + str(trialLength) + "_aBlockGiven_2A_pair1_index"] = aBlockGiven_2A_pair1_index
	outputFile["len" + str(trialLength) + "_aBlockGiven_2A_pair2_index"] = aBlockGiven_2A_pair2_index
	outputFile["len" + str(trialLength) + "_aBlockNew_2A_pair1_index"] = aBlockNew_2A_pair1_index
	outputFile["len" + str(trialLength) + "_aBlockNew_2A_pair2_index"] = aBlockNew_2A_pair2_index
	
	
	# Assign trials to B blocks, according to assignment in A blocks
	# if pair2 non-repeated in 1A, pair1 repeated in 1B
	# if pair1 repeated in 1A, pair2 non-repeated in 1B
	# etc.
	bBlockGiven_1B_pair1_index = aBlockNew_1A_pair2_index
	bBlockNew_1B_pair1_index = aBlockGiven_1A_pair2_index
	bBlockGiven_1B_pair2_index = aBlockNew_1A_pair1_index
	bBlockNew_1B_pair2_index = aBlockGiven_1A_pair1_index
	
	outputFile["len" + str(trialLength) + "_bBlockGiven_1B_pair1_index"] = bBlockGiven_1B_pair1_index
	outputFile["len" + str(trialLength) + "_bBlockGiven_1B_pair2_index"] = bBlockGiven_1B_pair2_index
	outputFile["len" + str(trialLength) + "_bBlockNew_1B_pair1_index"] = bBlockNew_1B_pair1_index
	outputFile["len" + str(trialLength) + "_bBlockNew_1B_pair2_index"] = bBlockNew_1B_pair2_index

	bBlockGiven_2B_pair1_index = aBlockNew_2A_pair2_index
	bBlockNew_2B_pair1_index = aBlockGiven_2A_pair2_index
	bBlockGiven_2B_pair2_index = aBlockNew_2A_pair1_index
	bBlockNew_2B_pair2_index = aBlockGiven_2A_pair1_index
	
	outputFile["len" + str(trialLength) + "_bBlockGiven_2B_pair1_index"] = bBlockGiven_2B_pair1_index
	outputFile["len" + str(trialLength) + "_bBlockGiven_2B_pair2_index"] = bBlockGiven_2B_pair2_index
	outputFile["len" + str(trialLength) + "_bBlockNew_2B_pair1_index"] = bBlockNew_2B_pair1_index
	outputFile["len" + str(trialLength) + "_bBlockNew_2B_pair2_index"] = bBlockNew_2B_pair2_index
	
getIndices(3, allIndices)
getIndices(4, allIndices)

# Assemble trials and create reference sheet with counterbalanced conditions listed
# Use indices obtained in previous function to index lists of trials
assembledTrials = {"block1A_len3": [],
					"block2A_len3": [],
					"block1B_len3": [],
					"block2B_len3": [],
					"block1A_len4": [],
					"block2A_len4": [],
					"block1B_len4": [],
					"block2B_len4": []}

def assembleTrialsCreateReferenceSheet(trials, indices):
	# Create reference sheet
	csvfile = open("list1_reference.csv", "wb")
	refwriter = csv.writer(csvfile, delimiter=",")
	refwriter.writerow(['target'] + ['trialType'] + ['givenness'] + ['block'] + ['length'])

	finishedKeys = trials.keys()
	for key in finishedKeys:
		res = key.split("_")
		trialLength = res[0]
		trialType = res[1]
		trialBlock = trialType[0].upper()
		blockString = trialType[0:6]
		trialCondition = trialType.strip(blockString)
		
		if trialBlock == "A":
			withinLoopBlocks = ["1A", "2A"]
		
			for block in withinLoopBlocks:
				outputDict = "block" + block + "_" + trialLength
				
				for i in range(0, 3):
					relevantIndices1 = trialLength + "_" + trialType + "_" + block + "_pair1_index"
					relevantIndices2 = trialLength + "_" + trialType + "_" + block + "_pair2_index"
					assembledTrials[outputDict].append(finishedTargetTrials[key][indices[relevantIndices1][i]])
					assembledTrials[outputDict].append(finishedTargetTrials[key][indices[relevantIndices2][i]])
										
					# Add trial information to reference sheet
					split1 = finishedTargetTrials[key][indices[relevantIndices1][i]].split(";")
					target1 = split1[3].split(" ")[0]
					refwriter.writerow([target1] + ["target"] + [trialCondition.lower()] + [block] + [trialLength[3]])
					
					split2 = finishedTargetTrials[key][indices[relevantIndices2][i]].split(";")
					target2 = split2[3].split(" ")[0]
					refwriter.writerow([target2] + ["target"] + [trialCondition.lower()] + [block] + [trialLength[3]])
		
		elif trialBlock == "B":
			withinLoopBlocks = ["1B", "2B"]
		
			for block in withinLoopBlocks:
				outputDict = "block" + block + "_" + trialLength
				
				for i in range(0, 3):
					relevantIndices1 = trialLength + "_" + trialType + "_" + block + "_pair1_index"
					relevantIndices2 = trialLength + "_" + trialType + "_" + block + "_pair2_index"
					assembledTrials[outputDict].append(finishedTargetTrials[key][indices[relevantIndices1][i]])
					assembledTrials[outputDict].append(finishedTargetTrials[key][indices[relevantIndices2][i]])
					
					# Add trial information to reference sheet
					split1 = finishedTargetTrials[key][indices[relevantIndices1][i]].split(";")
					target1 = split1[3].split(" ")[0]
					refwriter.writerow([target1] + ["target"] + [trialCondition.lower()] + [block] + [trialLength[3]])
					
					split2 = finishedTargetTrials[key][indices[relevantIndices2][i]].split(";")
					target2 = split2[3].split(" ")[0]
					refwriter.writerow([target2] + ["target"] + [trialCondition.lower()] + [block] + [trialLength[3]])
		
		else:
			print "Error!"

	# Add filler trials to reference sheet	
	fillerKeys = finishedFillerTrials_blocked.keys()
	for fillerKey in fillerKeys:
		for i in range(0, 4):
			split1 = finishedFillerTrials_blocked[fillerKey][i].split(";")
			filler = split1[1].split(" ")[0]
			refwriter.writerow([filler] + ["filler"] + ["new"] + ["any"] + ["any"])
		
	csvfile.close()

assembleTrialsCreateReferenceSheet(finishedTargetTrials, allIndices)

# Unpack dictionaries to combine targets and fillers into appropriate blocks
block1A = []
block1B = []
block2A = []
block2B = []

for key in assembledTrials.keys():
	if "block1A" in key:
		for i in range(0, len(assembledTrials[key])):
			block1A.append(assembledTrials[key][i])
	if "block2A" in key:
		for i in range(0, len(assembledTrials[key])):
			block2A.append(assembledTrials[key][i])
	if "block1B" in key:
		for i in range(0, len(assembledTrials[key])):
			block1B.append(assembledTrials[key][i])
	if "block2B" in key:
		for i in range(0, len(assembledTrials[key])):
			block2B.append(assembledTrials[key][i])

for key in finishedFillerTrials_blocked.keys():
	if "1A" in key:
		for i in range(0, len(finishedFillerTrials_blocked[key])):
			block1A.append(finishedFillerTrials_blocked[key][i])
	if "2A" in key:
		for i in range(0, len(finishedFillerTrials_blocked[key])):
			block2A.append(finishedFillerTrials_blocked[key][i])
	if "1B" in key:
		for i in range(0, len(finishedFillerTrials_blocked[key])):
			block1B.append(finishedFillerTrials_blocked[key][i])
	if "2B" in key:
		for i in range(0, len(finishedFillerTrials_blocked[key])):
			block2B.append(finishedFillerTrials_blocked[key][i])

# Randomize the blocks (twice for good measure)
random.shuffle(block1A)
random.shuffle(block1A)
random.shuffle(block1B)
random.shuffle(block1B)
random.shuffle(block2A)
random.shuffle(block2A)
random.shuffle(block2B)
random.shuffle(block2B)

# Combine blocks
allTrials = block1A + block1B + block2A + block2B

# Write completed stimulus list to file
# This script creates the first file (list1_order1)
# Another script creates other lists using this first one as a reference (see below)
wf = open("list1_order1.txt", "w")
for trial in allTrials:
    wf.write(trial)
    wf.write("\n")

wf.close()
