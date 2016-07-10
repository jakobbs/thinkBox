import random



####### GLOBAL VARIABLES #######

PLAYERS = 2
DICES = [4, 4]
DICE_RANGE = 6
PLAYER_ROLLS = []
INITIATIVE = 1
DICE_COUNT = 0
CURRENT_BET = []
TURN = 0
BETTING_HISTORY = []

numbers = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}

####### P1 GLOBALS #######

#Add global variables for your algoritm here



####### P2 GLOBALS #######

#Add global variables for your algoritm here



####### GAME STATISTICS #######

GAMES_LOST = [0, 0, 0, 0, 0]
ROUNDS_LOST = [0, 0, 0, 0, 0]
DICE_WHEN_WIN = []
GAME_BETTING_HISTORY = []


####### HELPER FUNCTIONS #######

#Dice roll - Generates a dice roll
def roll (cup):
    dice_roll = []
    for i in range(DICES[cup]):
        dice_roll.append (random.randint(1, DICE_RANGE))
    return dice_roll

#Function to make a list of default bets fitting the amount of players
def clean_bet ():
    global CURRENT_BET
    CURRENT_BET = [0,1]


    return

#Player roll - Generates a dice roll for each player
# and saves it as a global list
def pl_roll ():
    global PLAYER_ROLLS
    PLAYER_ROLLS = []

    for i in range(PLAYERS):
        PLAYER_ROLLS.append( roll(i) )
    return

def checkStair(arr):

    a = sorted(arr)
    while len(a):
        if len(a) != a.pop():
            return False
    return True

#CHECK FUNCTION - checks if the bet is true or false
def check (amount, name,Roll):
    Pool = []
    #Correcting for 'staircase rolls'
    for i in range(len(Roll)):
        roll = Roll[i]
        if checkStair(roll):
            Roll[i] = [1 for j in range(len(roll)+1)]

    #Pooling all dices together in one list with integers
    for i in Roll:
        Pool.extend(i)

    #Counting occurrances
    counter = []
    check = 0
    for x in range(2, DICE_RANGE+1):
        counter.append(Pool.count(x))

    if name == 1:
        for z in counter:
            if (z + Pool.count(1)) >= amount:
                check = 1
        return check == 1

    else:
        if name in Pool:
            return amount <= (Pool.count(name) + Pool.count(1))

        else:
            return False

#Counts the amount of dices in the game
def count_dices ():
    global DICE_COUNT

    count = 0

    for i in range(PLAYERS):
        count += DICES[i]
    DICE_COUNT = count

    return

#Start new game function
def start ():
    global DICES

    #Create placeholder for game historic
    BETTING_HISTORY.append([])
    #Resetting amount of dices'
    DICES = range(PLAYERS)
    for i in range(PLAYERS):
        DICES[i] = 4

    #Running a new round'
    new_round ()

    return

#Handler for starting new turn
def new_round ():
    global TURN, BETTING_HISTORY

    #Set placeholder for round historic data
    BETTING_HISTORY[-1].append([])

    #Resetting turn count
    TURN = 0

    #Counting dices
    count_dices ()

    #Resetting current bet
    clean_bet ()

    #Make a new roll
    pl_roll ()

    #Running a new turn
    turn_handler ()

    return

def isValidBet(existing,new):
    #check if it is a lift
    if isinstance(new,str):
        if new == "lift":
            return True
    #should be a list with length 2 [amount,name]
    if isinstance(new,list) and len(new) == 2:
        if existing[0] < new[0]:
            return True
        elif existing[0] == new[0] and existing[1] < new[1]:
            return True
    return False


#Function the decides whose turn it is and activates that player-algoritm
def turn_handler ():
    global INITIATIVE, TURN, CURRENT_BET
    #initially no bet i made
    bet = None
    while (bet != "lift"):

        TURN += 1

        if TURN > 1:
            if INITIATIVE == PLAYERS:
                INITIATIVE = 1
            else:
                INITIATIVE += 1

        #Setting the turn
        if INITIATIVE == 1:
            bet = player_1()

        elif INITIATIVE == 2:
            bet = player_2()

        elif INITIATIVE == 3:
            bet = player_3()

        elif INITIATIVE == 4:
            bet = player_4()

        elif INITIATIVE == 5:
            bet = player_5()
        if isValidBet(CURRENT_BET,bet):
            CURRENT_BET = bet[:]
        #if bet is not valid, change the current bet to something that is True for sure and lift
        else:
            print "ATTENTIONE der er sket en fejl"
            CURRENT_BET = [1,1]
            bet = "lift"

        BETTING_HISTORY[-1][-1].append(bet[:])

    lift()
    return


def sepquence (lenght):
    while lenght > 1:
        lenght += -1
        start ()

    if lenght == 1:
        print 'Lost games: ', GAMES_LOST
        print 'Lost rounds: ', ROUNDS_LOST


    return


#Handler for finding the winner when a player lifts
#UNDER CONSTRUCTION
def lift ():
    global DICES, INITIATIVE

    #Find the bet to check. "CURRENT_BET" cant be used as it has the value "lift"
    #the index [-1][-1][-2] is read as from the newest game, take the newest round, and the second newest bet
    betToCheck = BETTING_HISTORY[-1][-1][-2]
    #"better" is the index-number for the player whose bet has been lifted on and lifter is the index number of the lifter'
    better = (INITIATIVE - 2) % PLAYERS
    lifter = INITIATIVE - 1

    if check (betToCheck[0], betToCheck[1],PLAYER_ROLLS):
        if DICES[lifter] == 1:
            DICES[lifter] += -1
            GAMES_LOST[lifter] += 1
            ROUNDS_LOST[lifter] += 1
            DICE_WHEN_WIN.append(DICES)
            INITIATIVE = lifter + 1
            #print 'Game ended'
            #print 'Player ' + str((lifter + 1)) + ' lost the game'


        else:
            ROUNDS_LOST[lifter] += 1
            DICES[lifter] += -1
            INITIATIVE = lifter + 1
            #print 'Player ' + str((lifter + 1)) + ' lost a round'
            #print DICES
            new_round ()

    else:
        if DICES[better] == 1:
            DICES[better] += -1
            GAMES_LOST[better] += 1
            ROUNDS_LOST[better] += 1
            DICE_WHEN_WIN.append(DICES)
            INITIATIVE = better + 1
            #print 'Game ended'
            #print 'Player ' + str((better + 1)) + ' lost the game'


        else:
            ROUNDS_LOST[better] += 1
            DICES[better] += -1
            INITIATIVE = better + 1
            #print 'Player ' + str((better + 1)) + ' lost a round'
            #print DICES
            new_round ()
    return


####### PLAYER FUNCTIONS #######
def player_1 ():
    global CURRENT_BET, INITIATIVE
    if ((DICE_COUNT+1) // 2) < CURRENT_BET[0]:
        return "lift"
    else:
        return [CURRENT_BET[0] + 1, CURRENT_BET[1]]


def player_2 ():
    global CURRENT_BET, INITIATIVE
    if ((DICE_COUNT+1) // 2) < CURRENT_BET[0]:
        return "lift"
    else:
        return [CURRENT_BET[0] + 1, random.randint(1, DICE_RANGE)]



sepquence(4000)
