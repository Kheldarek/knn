import argparse
import csv
import math
import random
import sys

# argument parse configuration

parser = argparse.ArgumentParser()
parser.add_argument("-k", type=int, help="k for k-NN, default 5", default=5)
parser.add_argument("-m", help="metrics, default = euclides", choices=["euclides", "manhattan"], default="euclides")
parser.add_argument("-t", help="test set type (train, split, cross), default = train",
                    choices=["train", "split", "cross"], default="train")
parser.add_argument("-d", type=int, help="decisive attribute index (default - last)", default=-1)
parser.add_argument("-p", help="learning set percentage(default 25%)", default=0.25)
parser.add_argument("file", help="datafile")
args = parser.parse_args()

# input validation
if args.k > 0:
    print("K = " + repr(args.k))
else:
    print("K can not be zero or negative!")
    sys.exit()

if args.m:
    print("Metrics: " + repr(args.m))

if args.t in ["train", "split"]:
    print("Chosen test set type: " + repr(args.t))
else:
    print("UNSUPPORTED TEST SET!")
    sys.exit()

if args.d:
    print("Chosen index: " + repr(args.d))

if args.p:
    print("Chosen learning set percentage: " + repr(args.p))

if args.file:
    print("Datafile: " + repr(args.file))

learningSet = []


# functions

def readDataFile():
    return csv.reader(open(args.file, "r"))


def fileLenght():
    return sum(1 for line in open(args.file, "r"))


def manhattanDistance(case, neighbour, decisionIndex):
    endIndex = len(case)
    distance = 0
    for index in range(0, endIndex):
        if index != decisionIndex:
            distance = distance + abs(float(case[index]) - float(neighbour[index]))
        else:
            continue
    return float(distance)


def euclidDistance(case, neighbour, decisionIndex):
    endIndex = len(case)
    distance = 0
    for index in range(0, endIndex):
        if index != decisionIndex:
            distance = distance + pow((float(case[index]) - float(neighbour[index])), 2)
        else:
            continue
    return float(math.sqrt(distance))


def addToLearningSet(case):
    learningSet.append(case)


def teach(lineCount):
    file = readDataFile()
    lines = []
    for row in file:
        lines.append(row)

    forTraining = random.sample(lines, lineCount)

    for trainingRow in forTraining:
        if trainingRow:
            addToLearningSet(trainingRow)

    return forTraining


def test(toOmmit):
    positives = 0
    negatives = 0

    rows = readDataFile()

    for case in rows:
        if case in toOmmit:
            continue
        if case == []:
            continue

        if classify(case):
            positives = positives + 1
        else:
            negatives = negatives + 1

    stat = round(float(positives) / float(float(positives) + float(negatives)) * 100, 2)
    print("Correctness: " + str(positives) + " correct answers on " + str(positives + negatives) + " (" + str(
        stat) + "%)")


def classify(case):
    neighbours = []

    if int(args.d) == -1:
        index = len(case) - 1
    else:
        index = int(args.d)

    endIndex = len(learningSet)

    for i in range(0, endIndex):
        if args.m == "euclides":
            distance = euclidDistance(learningSet[i], case, index)
        else:
            distance = manhattanDistance(learningSet[i], case, index)

        decision = learningSet[i][index]
        neighbour = [distance, decision]
        neighbours.append(neighbour)

    neighbours.sort(key=lambda nei: nei[0])

    top = neighbours[:int(args.k)]

    answers = []
    for j in range(0, int(args.k)):
        answers.append(top[j][1])

    rank = {}
    for k in set(answers):
        rank[k] = answers.count(k)

    print("Closest neighbours in k = : " + str(args.k) + " are: " + str(answers))

    classification = max(rank, key=rank.get)
    print("Classification: " + classification)

    if str(classification) == str(case[index]):
        return 1
    else:
        return 0


# run program

dataLength = fileLenght()

if args.t == "split":
    dataLength = math.floor(dataLength * float(args.p))

dataLength = teach(int(dataLength))

if args.t == "split":
    test(dataLength)
else:
    test([])
