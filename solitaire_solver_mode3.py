import numpy as np
from collections import namedtuple
import copy
import json
import pickle
import random

moves = 0

def swap(t1, t2):
    return t2, t1


acc = 1664525
ctrl = 1013904223
mod = pow(2, 32)

def nextSeed(seed):
    return (acc*seed + ctrl)%mod

def getSuitForCard(cardNum):
    return (cardNum-1)/13 + 1

def createDup(curState, dupState):
    dupState = copy.deepcopy(curState)

def findPossibleCards(cardNum, possibleCard1, possibleCard2):
    suit = getSuitForCard(cardNum)
    cardVal = (cardNum-1)%13 + 1
    if cardVal == 13:
        return
    possibleSuit1 = -1
    possibleSuit2 = -1
    if suit == 1 or suit == 4:
        possibleSuit1 = 2
        possibleSuit2 = 3

    else:
        possibleSuit1 = 1
        possibleSuit2 = 4

    possibleCard1 = cardVal + 1 + 13*(possibleSuit1 - 1)
    possibleCard2 = cardVal + 1 + 13 * (possibleSuit2 - 1)

def performMove(curState, states):
    score = curState["score"]
    tableau = curState["tableau"]
    tableauTop = curState["tableauTop"]
    foundation = curState["foundation"]
    discard = curState["discard"]
    stock = curState["stock"]

    for i in range(0,7):
        # check for foundation move
        if tableauTop[i] == -1:
            continue
        last_card = len(tableau[i]) - 1
        cardNum = tableau[i][last_card]
        foundationPile = (cardNum-1)/13
        if len(foundation[foundationPile]) == (cardNum-1)%13:
            #FOUNDATION MOVE POSSIBLE
            dupState = {}
            dupState = copy.deepcopy(curState)
            dupState["foundation"][foundationPile].append(cardNum)

            dupState["score"] = dupState["score"] + 15
            if dupState["tableauTop"][i] == len(dupState["tableau"][i]) - 1:
                dupState["tableauTop"][i] = dupState["tableauTop"][i] - 1
                dupState["score"] = dupState["score"] + 5

            dupState["tableau"][i].pop()
            states.append(dupState)


        for j in range(0, 7):
            if j == i:
                continue
            for k in range(tableauTop[i], len(tableau[i])):
                if tableauTop[i] == -1:
                    continue
                cardNum = tableau[i][k]
                possibleCard1 = -1
                possibleCard2 = -1

                suit = getSuitForCard(cardNum)
                cardVal = (cardNum - 1) % 13 + 1
                if cardVal == 13:
                    possibleCard1 = -1
                else:
                    possibleSuit1 = -1
                    possibleSuit2 = -1
                    if suit == 1 or suit == 4:
                        possibleSuit1 = 2
                        possibleSuit2 = 3

                    else:
                        possibleSuit1 = 1
                        possibleSuit2 = 4

                    possibleCard1 = cardVal + 1 + 13 * (possibleSuit1 - 1)
                    possibleCard2 = cardVal + 1 + 13 * (possibleSuit2 - 1)


                if possibleCard1 == -1:
                    if tableauTop[j] == -1 and tableauTop[i] > 0:
                        dupState1 = {}
                        dupState1 = copy.deepcopy(curState)


                        cardsToMove = len(tableau[i]) - k
                        

                        if dupState1["tableauTop"][i] == k:
                            dupState1["tableauTop"][i] = dupState1["tableauTop"][i] - 1
                            dupState1["score"] = dupState1["score"]
                        

                        for q in range(k, len(tableau[i])):
                            dupState1["tableau"][j].append(dupState1["tableau"][i][q])

                        for q in range(0, cardsToMove):
                            dupState1["tableau"][i].pop()

                        dupState1["tableauTop"][j] = dupState1["tableauTop"][j] + 1
                        states.append(dupState1)




                if tableauTop[j] > -1:
                    last_card = len(tableau[j]) - 1
                    if tableau[j][last_card] == possibleCard1 or tableau[j][last_card] == possibleCard2:
                        dupState2 = {}
                        dupState2 = copy.deepcopy(curState)

                        cardsToMove = len(tableau[i]) - k
                        for q in range(k, len(tableau[i])):
                            dupState2["tableau"][j].append(dupState2["tableau"][i][q])

                        for q in range(0, cardsToMove):
                            dupState2["tableau"][i].pop()
                    
                        fl = 0
                        
                        if k == tableauTop[i]:
                            dupState2["tableauTop"][i] = dupState2["tableauTop"][i] - 1
                            dupState2["score"] = dupState2["score"] + 5
                            fl = 1
                        else:
                            cardNum = dupState2["tableau"][i][k-1]
                            cardVal = (cardNum - 1) % 13 + 1
                            cardSuit = getSuitForCard(cardNum)
                            if len(foundation[(cardNum-1)/13]) == (cardNum - 1)%13:
                                fl = 1

                        if fl == 1:
                            states.append(dupState2)

    dupState3 = {}
    dupState3 = copy.deepcopy(curState)

    if len(dupState3["stock"]) > 0:

        dupState3["discard"].append(dupState3["stock"][-1])
        dupState3["stock"].pop()
        if len(dupState3["stock"]) > 0:
            dupState3["discard"].append(dupState3["stock"][-1])
            dupState3["stock"].pop()
            if len(dupState3["stock"]) > 0:
                dupState3["discard"].append(dupState3["stock"][-1])
                dupState3["stock"].pop()
        states.append(dupState3)

    dupState4 = {}
    dupState4 = copy.deepcopy(curState)


    if len(dupState4["discard"]) > 0:
        cardNum = dupState4["discard"][-1]
        foundationPile = (cardNum - 1) / 13
        if len(dupState4["foundation"][foundationPile]) == (cardNum-1) % 13:
            # FOUNDATION MOVE POSSIBLE
            dupState5 = {}
            dupState5 = copy.deepcopy(curState)


            dupState5["foundation"][foundationPile].append(cardNum)
            dupState5["discard"].pop()
            dupState5["score"] = dupState5["score"] + 15

            states.append(dupState5)

        possibleCard1 = -1
        possibleCard2 = -1

        suit = getSuitForCard(cardNum)

        cardVal = (cardNum - 1) % 13 + 1
        if cardVal == 13:
            possibleCard1 = -1
        else:
            possibleSuit1 = -1
            possibleSuit2 = -1
            if suit == 1 or suit == 4:
                possibleSuit1 = 2
                possibleSuit2 = 3

            else:
                possibleSuit1 = 1
                possibleSuit2 = 4

            possibleCard1 = cardVal + 1 + 13 * (possibleSuit1 - 1)
            possibleCard2 = cardVal + 1 + 13 * (possibleSuit2 - 1)


        for q in range(0,7):
            if possibleCard1 == -1:
                if tableauTop[q] == -1:
                    dupState6 = {}
                    dupState6 = copy.deepcopy(curState)

                    dupState6["tableau"][q].append(cardNum)
                    dupState6["tableauTop"][q] = dupState6["tableauTop"][q] + 1
                    dupState6["discard"].pop()
                    dupState6["score"] = dupState6["score"] + 10
                    states.append(dupState6)

            if tableauTop[q] > -1:
                last_card = len(tableau[q]) - 1
                if tableau[q][last_card] == possibleCard1 or tableau[q][last_card] == possibleCard2:
                    dupState2 = {}
                    dupState2 = copy.deepcopy(curState)
                    dupState2["tableau"][q].append(cardNum)
                    dupState2["discard"].pop()
                    dupState2["score"] = dupState2["score"] + 10
                    states.append(dupState2)


    if len(stock) == 0:
        dupState7 = {}
        dupState7 = copy.deepcopy(curState)

        while len(dupState7["discard"]) > 0:
            dupState7["stock"].append(dupState7["discard"][-1])
            dupState7["discard"].pop()


        states.append(dupState7)

def checkLastState(state):
    q = 0
    for i in range(0,7):
        if state["tableauTop"][i] > 0:
            q = q + 1

    if q > 0 or len(state["discard"]) > 0:
        return False
    else:
        return True

def saveDeck(moves, x):
    w = 0
    for i in range (0,4):
        w = w + 13 - len(x["foundation"][i])
    state1["moves"] = moves + w
    print x
    print state1
    mydict.append(state1)
    output = open('solitaire_solved_decks_with_seed_mode_3.pkl', 'wb')
    pickle.dump(mydict, output)
    output.close()

def calculateNext5Moves(states, iter, moves):
    for i in range(0,3):
        moves = moves + 1
        p = len(states)
        print p
        for j in range(0, p):

            if checkLastState(states[j]):
                saveDeck(moves, states[j])

                return
            performMove(states[j], states)

        q = 0
        while q < p:
            del states[0]
            q = q+1

    max_score = -1
    for q in range(0, len(states)):
        if max_score < states[q]["score"]:
            max_score = states[q]["score"]

    q = 0
    while q < len(states) and q < 1000:
        if(max_score != states[q]["score"]):
            del states[q]

        else:
            q = q+1

    print max_score

    while len(states) > 1000:
        del states[1000]

    np.random.shuffle(states)

    while len(states) > 20:
        del states[20]


    if iter < 70:
        calculateNext5Moves(states, iter + 1, moves)



loop = 0
while(loop<500000):
    loop = loop+1
    seed = random.randint(1, 1000000000)
    initalSeed = seed
    cards = []
    cards = np.arange(1, 53)
    n = 51
    while n > 0:
        seed = nextSeed(seed)
        p = seed % n
        cards[n], cards[p] = swap(cards[n], cards[p])
        n = n - 1

    tableau = []
    tableauTop = []
    foundation = []

    for i in range(0,4):
        y = []
        foundation.append(y)


    discard = []
    stock = []
    c = 0
    for i in range(0,7):
        x = []
        for j in range(0, i+1):
            x.append(cards[c])
            c = c + 1
        tableau.append(x)
        tableauTop.append(len(x) - 1)


    print tableau
    print tableauTop

    for i in range(28, 52):
        stock.append(cards[i])

    print stock
    print
    state1 = {}
    state1["score"] = 0
    state1["tableau"] = tableau
    state1["tableauTop"] = tableauTop
    state1["foundation"] = foundation
    state1["discard"] = discard
    state1["stock"] = stock
    state1["seed"] = initalSeed
    print state1

    pkl_file = open('solitaire_solved_decks_with_seed_mode_3.pkl', 'rb')
    mydict = pickle.load(pkl_file)
    pkl_file.close()

    states = []
    states.append(state1)
    iter = 0
    moves = 0
    calculateNext5Moves(states, iter, moves)


