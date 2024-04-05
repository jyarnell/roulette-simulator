

import random
import globals

total_bet = 160
def spins():
    global winning_number
    winning_number = int(random.choice(list(globals.slots.keys())))
    return winning_number


def win_loss(winning_number):
    if (winning_number >= 13 and winning_number <= 36):
        win = 20
    elif (winning_number in (2,3,5,6,7,8,10,11)):
        win = 10
    else:
        win = total_bet * -1

    return win


def gamble(balance):
    global adj_bankroll

    # Lost the entire round
    if balance < total_bet:
        prompt =  "You have insufficient funds at $%s" % balance
        adj_bankroll = balance
        return(prompt, adj_bankroll)

    spins()
    adj_bankroll = balance + win_loss(winning_number)
    if adj_bankroll > balance:
        prompt =  f'You won with an ending balance of ${adj_bankroll} number {winning_number}.'
    else:
        prompt =  f'You lost with an ending balance of ${adj_bankroll} number {winning_number}.'
    return (prompt, adj_bankroll)


bankroll = int(input("What is your starting balance (in whole $$): "))
roll_cnt = 0
max_bank = 0
while bankroll > 160 or roll_cnt > 1000:
    if bankroll > max_bank:
        max_bank = bankroll
    (prompt, balance) = gamble(bankroll)
    print(prompt)
    bankroll = balance
    roll_cnt += 1

print(f'Final rolls: {roll_cnt} Max Bankroll: {max_bank}')