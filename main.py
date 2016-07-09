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


numbers = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}

####### P1 GLOBALS #######

#Add global variables for your algoritm here



####### P2 GLOBALS #######

#Add global variables for your algoritm here



####### GAME STATISTICS #######

GAMES_LOST = [0, 0, 0, 0, 0]
ROUNDS_LOST = [0, 0, 0, 0, 0]
DICE_WHEN_WIN = []


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
    CURRENT_BET = []

    for i in range(PLAYERS):
        CURRENT_BET.append([0,1])
    return

#Player roll - Generates a dice roll for each player
# and saves it as a global list
def pl_roll ():
    global PLAYER_ROLLS
    PLAYER_ROLLS = []

    for i in range(PLAYERS):
        PLAYER_ROLLS.append( roll(i) )
    return

#CHECK FUNCTION - checks if the bet is true or false
def check (amount, name):
    Roll = PLAYER_ROLLS
    Pool = []
    #Correcting for 'staircase rolls'
    for i in Roll:
        if i.sort() == [1, 2, 3, 4]:
            i = [1, 1, 1, 1, 1]
        elif i.sort() == [1, 2, 3]:
            i = i = [1, 1, 1, 1]
        elif i.sort() == [1, 2]:
            i = [1, 1, 1]
        elif i.sort() == [1]:
            i = [1, 1]

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

    #Resetting amount of dices'
    DICES = range(PLAYERS)
    for i in range(PLAYERS):
        DICES[i] = 4

    #Running a new round'
    new_round ()

    return

#Handler for starting new turn
def new_round ():
    global TURN

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

#Function the decides whose turn it is and activates that player-algoritm
def turn_handler ():
    global INITIATIVE, TURN

    TURN += 1

    if TURN > 1:
        if INITIATIVE == PLAYERS:
            INITIATIVE = 1
        else:
            INITIATIVE += 1

    #Setting the turn
    if INITIATIVE == 1:
        player_1 ()

    elif INITIATIVE == 2:
        player_2 ()

    elif INITIATIVE == 3:
        player_3 ()

    elif INITIATIVE == 4:
        player_4 ()

    elif INITIATIVE == 5:
        player_5 ()

    return


def sepquence (lenght): 
    while lenght > 1:
        lenght += -1
        start ()

    if lenght == 1:
        print 'Lost games: ', GAMES_LOST
        print 'Lost rounds: ', ROUNDS_LOST
        print 'Dice left at the end of game :', DICE_WHEN_WIN
    
    return


#Handler for finding the winner when a player lifts
#UNDER CONSTRUCTION
def lift ():
    global DICES, INITIATIVE

    #"better" is the index-number for the player whose bet has been lifted on and lifter is the index number of the lifter'
    better = (INITIATIVE - 2) % PLAYERS
    lifter = INITIATIVE - 1

    if check (CURRENT_BET[better][0], CURRENT_BET[better][1]):
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
    global CURRENT_BET
    if ((DICE_COUNT+1) // 2) < CURRENT_BET[PLAYERS - 1][0]:
        lift ()
    else:
        CURRENT_BET[0][0] = CURRENT_BET[PLAYERS - 1][0] + 1
        CURRENT_BET[0][1] = CURRENT_BET[PLAYERS - 1][1]

        turn_handler ()

    return

def player_2 ():
    global CURRENT_BET
    if ((DICE_COUNT+1) // 2) < CURRENT_BET[0][0]:
        lift ()
    else:
        CURRENT_BET[1][0] = CURRENT_BET[0][0] + 1
        CURRENT_BET[1][1] = random.randint(1, DICE_RANGE)

        turn_handler () 

    return

sepquence (40)
