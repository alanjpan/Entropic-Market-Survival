# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 21:04:51 2018

@author: Alan Jerry Pan, CPA, CSC
@affiliation: Shanghai Jiaotong University

Program used for experimental study of (i) financial markets, (ii) investor behavior, and (iii) information asymmetry in decision making (business) and risk-taking.

Suggested citation as computer software for reference:
Pan, Alan J. (2018). Entropic Market Survival [Computer software]. Github repository <https://github.com/alanjpan/Entropic-Market-Survival>

Futher expansions may include more financial actions and post-cycle investments.

Note this software's license is GNU GPLv3.
"""


import random
import sys
import time

secure_random = random.SystemRandom()

position = []
money = []

plays = 0
bankrupts = 0
smallloans = 1
actions = [0, 0, 0, 0]

######################################################

actionid = [0, 1, 2, 3]
actionlist = ['recession', 'crash', 'invest', 'shirk']

def recession(player, target):
    global money
    if actions[0] > 0:
        print('Recession!')
        for i in range((len(money))):
            if i == player:
                next
            else:
                money[i] -= 1 + smallloans
        actions[0] -= 1
    else:
        noact()

def crash(p, t):
    global money
    if actions[1] > 0:
        print('Crash!')
        money[t] -= 3
        actions[1] -= 1
    else:
        noact()
        
def invest(p, t):
    global money
    if actions[2] > 0:    
        print('Invest!')
        money[t] += 2
        actions[2] -= 1
    else:
        noact()

def shirk(p, t):
    global money
    if actions[3] > 0:
        print('Shirk!')
        for i in range((len(money))):
            money[i] += 1
        actions[3] -= 1
    else:
        noact()

def noact():
    print('You waste your turn.')
    
######################################################
        
def initsubspace(n):
    global position
    position.clear()
    for i in range(n):
        position.append(i)

def initactionpool(n):
    global spellpool
    for i in range(len(actions)):
        actions[i] = 0
    for j in range(n):
        for k in range(5):
            sid = secure_random.choice(actionid)
            actions[sid] += 1

def initmoney(n):
    global money
    global smallloans

    transfer = 10
    if plays > 0:
        if money[0] < 10:
            print('You acquire another 10 million! Spend it wisely this time.')
            smallloans += 1
        else:
            transfer = money[0]

    money.clear()
    for i in range(n+1):
        money.append(10)
    money[0] = transfer

def scroll():
    count = 0
    print('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('/\t   AVAILABLE ACTIONS')
    for i in range(len(actionid)):
        print('/\t' + actionlist[i] + '\t' + str(actions[i]))
        count += actions[i]
    print('\n' + str(money[0]) + ' million dollars remaining.')
    if count == 0:
        gameover()

def RIP():
    global bankrupts
    for i in range(1, len(money)):
        try:
            if money[i] <= 0:
                print('\nMARKET PARTICIPANT NUMBER ' + str(i) + ' IS BANKRUPT! THE NEXT PARTICIPANT TAKES ITS SPOT!')
                del money[i]
                bankrupts += 1
        except Exception:
            continue

def ENTROPICTURN():
    print('\n!(!&@$)#(@ENTROPIC MARKET\'S TURN*%!(@)#($#')
    
    for i in range(1, len(money)):
        action = secure_random.choice(actionlist)
        target = secure_random.choice(position)
        
        try:
            exec(compile(action + '(' + str(i) + ', ' + str(target) + ')', '', 'exec'))
        except Exception:
            print('Shirking!')
    RIP()
    

def TOSUBSPACE(n):
    initsubspace(n)
    initactionpool(n)
    initmoney(n)
    
    while money[0] >= 0:
        scroll()
        print('\n\nChoose an action! Must type the exact action name!\n')
        cast = input().lower()
        
        print('\nWhich participant? (0-' + str(n) + ')')
        try:
            target = int(input())
            try:
                exec(compile(cast + '(0, ' + str(target) + ')', '', 'exec'))
            except Exception:
                print('You type in gibberish and waste your turn.')
        except Exception:
            print('You need to target a market participant.')
        RIP()
        
        ENTROPICTURN()
        n = len(money) - 1
        if n == 0:
            break
        
    gameover()
        

def gameover():
    global plays
    plays += 1
    print('\n\nXXXXXXXXXXXXXXX[GAME OVER]XXXXXXXXXXXXXXX\n')
    print('You have bankrupted ' + str(bankrupts) + ' participants.')
    print('You have taken ' + str(smallloans) + ' small loans of 10 million dollars.')
    print('100 bankruptcy trophies are needed to escape this market.')
    print(str(money[0]) + ' million dollars are carried to the next round.')
    
    if bankrupts >= 100:
        for char in '. . . . . . . . . .\nYou have survived and escaped the entropic market!\n':
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.30)
    
    print('Play again? (ye/no)')
    if input().lower().startswith('ye'):
        main()
    else:
        sys.exit()
        
def main():    
    print('\n\nXXXXXXXXXX[ENTROPIC MARKET]XXXXXXXXXX\n')
    print('You, an investor, mishappen to stumble upon a completely unpredictable market. You face a number of participants that do things completely at random. Can you survive and escape this entropic market? (ye/no)\n')
    if input().lower().startswith('ye'):
        opp = 0
        op = 0
        while (opp < 1) or (opp > 99):
            try:
                print('How many participants (2-99)?')
                op = int(input())
                if 2 <= op <= 99:
                    TOSUBSPACE(op)
                else:
                    print('Select a desired number of entropic participants.')
            except Exception:
                print('Input valid number.')
            
            opp = op
    else:
        gameover()
        
main()