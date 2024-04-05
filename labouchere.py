'''labouchere.py

PURPOSE:    This script runs the Labouchere gambling method in American
            Roulette. This script just allows for keeping a constant bet on
            RED, and does not allow for betting on black, evens, or odds.

FURTHER
READING:    For information on how this method works, see the following:
            https://en.wikipedia.org/wiki/Labouch%C3%A8re_system

            The gamble() function is based off of the code given in the
            aforementioned website.

AUTHOR:     Nicholas P. Taliceo
            ntaliceo@gmail.com  |  www.NicholasTaliceo.com

DATE:       August 06, 2017
'''

import random
import globals

def spins():
    slots = globals.slots

    global winning_number
    winning_number = int(random.choice(list(slots.keys())))
    return winning_number


def win_loss(winning_number):
    if (winning_number % 2 == 0) and (winning_number != 0):
        win = True
    else:
        win = False
    return win


def gamble(sequence, balance):
    global adj_bankroll

    # Won
    if len(sequence) < 1:
        prompt =  "You won with an ending balance of $%s" % balance
        adj_bankroll = balance
        return(prompt, adj_bankroll)

    # If the sequence is of length 1, the bet is the number in the sequence.
    # Otherwise, it is the first number added to the last number.
    if len(sequence) is 1:
        bet = sequence[0]
    else:
        bet = sequence[0] + sequence[-1]

    # Lost the entire round
    if bet > balance:
        prompt =  "You have insufficient funds at $%s" % balance
        adj_bankroll = balance
        return(prompt, adj_bankroll)

    spins()

    if win_loss(winning_number):
        # Won
        return gamble(sequence[1:-1], balance+bet)
    else:
        # Lost bet
        return gamble(sequence+[bet], balance-bet)


sequence = [5, 5, 5]
bankroll = int(input("What is your starting balance (in whole $$): "))
while bankroll > 0:
    (prompt, balance) = gamble(sequence, bankroll)
    print(prompt)
    bankroll = balance
    sequence = [5, 5, 5]
