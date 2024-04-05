
import random
import globals
import sys

wait_for_misses = 3
colBet = 0
rowBet = 0
last_bet = 0
bet = 1
cnt = 0
cnt_since_col1, cnt_since_col2, cnt_since_col3 = 0,0,0
cnt_since_row1, cnt_since_row2, cnt_since_row3 = 0,0,0

def spins():
    global cnt_since_col1, cnt_since_col2, cnt_since_col3
    global cnt_since_row1, cnt_since_row2, cnt_since_row3
    global winning_number

    winning_number = int(random.choice(list(globals.slots.keys())))

    num = globals.slots["%s"%winning_number]
    col, row = num[1], num[2]

    if (col == 1):
        cnt_since_col1, cnt_since_col2, cnt_since_col3 = 0, cnt_since_col2+1, cnt_since_col3+1
    if (col == 2):
        cnt_since_col1, cnt_since_col2, cnt_since_col3 = cnt_since_col1+1, 0, cnt_since_col3+1
    if (col == 3):
        cnt_since_col1, cnt_since_col2, cnt_since_col3 = cnt_since_col1+1, cnt_since_col2+1, 0
    if (col == 0):
        cnt_since_col1, cnt_since_col2, cnt_since_col3 = cnt_since_col1+1, cnt_since_col2+1, cnt_since_col3+1

    if (row == 1):
        cnt_since_row1, cnt_since_row2, cnt_since_row3 = 0, cnt_since_row2+1, cnt_since_row3+1
    if (row == 2):
        cnt_since_row1, cnt_since_row2, cnt_since_row3 = cnt_since_row1+1, 0, cnt_since_row3+1
    if (row == 3):
        cnt_since_row1, cnt_since_row2, cnt_since_row3 = cnt_since_row1+1, cnt_since_row2+1, 0
    if (row == 0):
        cnt_since_row1, cnt_since_row2, cnt_since_row3 = cnt_since_row1+1, cnt_since_row2+1, cnt_since_row3+1

    return winning_number


def win_loss(winning_number):
    global colBet
    global rowBet
    num = globals.slots["%s"%winning_number]
    col, row = num[1], num[2]

    if (colBet > 0 and col == colBet) or (rowBet > 0 and row == rowBet):
        win = 1
    elif (colBet > 0 and col != colBet) or (rowBet > 0 and row != rowBet):
        win = -1
    else:
        win = 0
    return win


def gamble(balance, bet, last_bet):
    global wait_for_misses
    global colBet
    global rowBet
    global cnt
    global cnt_since_col1, cnt_since_col2, cnt_since_col3
    global cnt_since_row1, cnt_since_row2, cnt_since_row3

    #handle no current bet
    if colBet == 0 and rowBet == 0 and (cnt_since_col1 >=wait_for_misses or cnt_since_col2 >=wait_for_misses or cnt_since_col3 >=wait_for_misses):
        if cnt_since_col1 >=wait_for_misses:
            colBet = 1
            # print("Betting Col: %s - %s,%s,%s"%(colBet, cnt_since_col1, cnt_since_col2,cnt_since_col3))
        elif cnt_since_col2 >=wait_for_misses:
            colBet = 2
            # print("Betting Col: %s - %s,%s,%s"%(colBet, cnt_since_col1, cnt_since_col2,cnt_since_col3))
        else:
            colBet = 3
            # print("Betting Col: %s - %s,%s,%s"%(colBet, cnt_since_col1, cnt_since_col2,cnt_since_col3))

    elif rowBet == 0 and rowBet == 0 and (cnt_since_row1 >=wait_for_misses or cnt_since_row2 >=wait_for_misses or cnt_since_row3 >=wait_for_misses):
        if cnt_since_row1 >=wait_for_misses:
            rowBet = 1
            # print("Betting Row: %s - %s,%s,%s"%(rowBet, cnt_since_row1, cnt_since_row2,cnt_since_row3))
        elif cnt_since_row2 >=wait_for_misses:
            rowBet = 2
            # print("Betting Row: %s - %s,%s,%s"%(rowBet, cnt_since_row1, cnt_since_row2,cnt_since_row3))
        else:
            rowBet = 3
            # print("Betting Row: %s - %s,%s,%s"%(rowBet, cnt_since_row1, cnt_since_row2,cnt_since_row3))

    spins()

    did_win = win_loss(winning_number)
    if did_win == 1:
        # Won
        prompt = ("%s: Won, resetting to 1 unit" % winning_number, balance+(bet*2), 1, 0)
        colBet,rowBet = 0, 0
        return prompt
    elif did_win == -1 and bet >= 8:
        # Lost bet
        prompt = ("%s: Lost, giving up after too many tries: %s units." %(winning_number, bet), balance-bet, 1, 0)
        colBet, rowBet = 0, 0
        return prompt
    elif did_win == -1 :
        # Lost bet
        new_bet = last_bet + bet
        prompt = ("%s: Lost, increasing bet to: %s units.(%s,%s)" %(winning_number, new_bet, bet, last_bet), balance-bet, new_bet, bet)
        return prompt
    else:
        return ("%s: No Bet" %(winning_number), balance, bet, last_bet)

runs = 100
win_cnt = 0
loss_cnt = 0
if len(sys.argv) > 1 :
    bankroll = int(sys.argv[1])
else:
    bankroll = int(input("What is your starting number of units: "))

if len(sys.argv) > 2 :
    runs = int(sys.argv[2])
start_units = bankroll

while runs > 0:
    while bankroll > 0 and start_units * 1.5 >= bankroll:
        (prompt, balance, new_bet, new_last_bet) = gamble(bankroll, bet, last_bet)
        cnt += 1
        # print("%s - Number: %s - balance: %s"%(cnt,prompt, balance))
        bankroll = balance
        bet = new_bet
        last_bet = new_last_bet

    # print("%s - balance: %s"%(cnt, balance))
    bankroll = start_units
    cnt = 0
    runs -= 1
    if balance > 0:
        win_cnt += 1
    else:
        loss_cnt += 1

print("Wins: %s - Losses: %s"%(win_cnt, loss_cnt))