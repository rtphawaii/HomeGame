import sys
sys.path.append('../pokerlib')

from argparse import ArgumentParser
from pokerlib import Player, PlayerSeats
from pokerlib import Table
from pokerlib import HandParser as HandParser
from pokerlib.enums import Rank, Suit
import random
import copy
class Table():
    def __init__(self,smallblind,bigblind):
        self.list=[]
        self.order=[]
        self.startingorder=[]
        self.pot=0
        self.smallblind=smallblind
        self.bigblind=bigblind
        self.currentprice=self.bigblind
        self.bet=[]
        self.board=[]
        self.deck=[]
        self.rank=[]
        self.preflop=True
        self.rivercheck=False
        self.gameover=False
        self.round=1
    def createdeck(self):
        '''create the deck'''
        self.deck = [(rank, suit) for rank in Rank for suit in Suit]
        self.shuffledeck()
    def shuffledeck(self):
        random.shuffle(self.deck)
    def addplayer(self,player):
        '''add a player to the game'''
        self.list.append(player)
    def pickdealer(self):
        '''pick a dealer'''
        self.order=self.list
        random.shuffle(self.order)
        return self.order[0].name
            
    def deal(self):
        '''deal hands'''
        for x in self.list:
            x.hand.append(self.deck.pop())
            x.hand.append(self.deck.pop())
    def flop(self):
        '''deals flop'''
        print('flop')
        #burn one card
        self.deck.pop()
        #deal 3 cards to the board
        self.board.append(self.deck.pop())
        self.board.append(self.deck.pop())
        self.board.append(self.deck.pop())
        print(self.board)
    def turn(self):
        '''deals turn'''
        print('turn')
        #burn one card
        self.deck.pop()
        #deal 1 card to the board
        self.board.append(self.deck.pop())
        print(self.board)
        
    def river(self):
        '''deals river'''
        print('river')
        #burn one card
        self.deck.pop()
        #deal 1 card to the board
        self.board.append(self.deck.pop())
        print(self.board)
        
    def bets(self):
        '''betting mechanism'''
        #start collecting the first round of bets starting from next to the big blind
        raise_offset=1
        #find the big blind index in self.order
        if self.preflop==True:
            #option to straddle (needs building)
            
            #find the player that is big blind
            player_to_find = self.bet[-1][0]
            found_index = None
            for index, player in enumerate(self.order):
                if player == player_to_find:
                    found_index = index
                    #the action starts one player after the big blind if there has not been a straddle
                    found_index+=1
                    #set an endpoint, the betting should end before reaching the end index based on the loop parameters
                    end_index=found_index
                    break
        else:
            #when it is post flop,river, turn, action starts after the dealer and ends on the dealer
            self.bet=[(self.list[-1],0)]
            found_index=1
            end_index=1
        #once the index of the big blind player is found, loop around starting from the person next to them
        if found_index is not None:
            #everything should be in a while loop that resets betting if someone raises
            continue_loop = True
            while continue_loop:
                    #continue through the betting process as normal unless someone raises
                    continue_loop=False
                    #betting loop starts
                    for offset,player in enumerate(self.order[found_index:] + self.order[:end_index]):
                        #betting ends if everyone has folded except for one player 
                        if len(self.order)<=1:
                            continue_loop=False
                            return
                        #a player needs to place a valid bet that is a fold, call, check, or raise
                        while True:
                            playerbet = player.placebet(self.bet[-1][1])
                            if playerbet == -1 or playerbet == self.bet[-1][1] or playerbet > self.bet[-1][1]:
                                break  # Exit the while loop
                            else:
                                print("Invalid bet. Please enter another bet.")
                        #remove the player from the order if they fold
                        if playerbet==-1:
                            index = self.order.index(player)
                            self.order.pop(index)
                            print('fold')
                        #player raises, evaluate bets for everyone again starting from the next player around to the player that raises
                        elif playerbet>self.bet[-1][1]:
                            #add the bet to the betting log
                            self.bet.append((player,playerbet))
                            #the player object that raised and needs to be found
                            player_to_find = self.bet[-1][0]
                            #find the index of the player that raised
                            for index, player in enumerate(self.order):
                                if player == player_to_find:
                                    found_index = index
                                    found_index+=1
                            #end the betting action on the person before the person that is raising 
                            end_index=found_index-1
                            print('raise')
                            raise_offset=0
                            continue_loop=True
                            break  # Break out of the loop to restart (enter the start of the first while loop)
                        else:
                            #if the bet is a call then it is simply added and we move to the next better
                            self.bet.append((player,playerbet))
    def evaluate(self):
        '''determine winner and give pot'''
        hands=[]
        if len(self.order)==1:
            self.order[0].balance+=self.pot
            print(f'everyone else folded... {self.order[0].name} wins {self.pot}')
        else:
            #add each hand to hands
            for x in self.order:
                x.hand=HandParser(x.hand)
                x.hand+=self.board
                hands.append((x,x.hand))
            #evaluate the best hand and player
            max_player = max(hands, key=lambda x: x[1])
            winner_index = hands.index(max_player)
            winners = []  # List to store players with the maximum hand value
            # Iterate through handlist excluding the winner_index
            winners.append(max_player[0])
            #check to see if there are any other winners
            for index, (player, hand) in enumerate(hands):
                if index != winner_index:
                    if hand == max_player[1]:
                        winners.append(player)
            #if there is one winner add the pot to their balance
            if len(winners)==1:
                winners[0].balance+=self.pot
                print(f'{winners[0].name} wins {self.pot}','with',winners[0].hand.handenum)
            #if there is more than one winner split the pot between them
            else:
                for x in winners:
                    print(x, 'wins with:',x.handscore)
                    x.balance+=self.pot/len(winners)
    def fold_check(self):
        if len(self.order)==1:
            self.order[0].balance+=self.pot
            print(f'everyone else folded... {self.order[0].name} wins {self.pot}')
            self.gameover=True
  
        
    def potcalc(self):
        #takes the latest bets from each player unless the player bet then folded
        latest_bets = {}
        for player, bet in reversed(self.bet):
            if player not in latest_bets and bet != -1:
                latest_bets[player] = bet
            elif player not in latest_bets:
                latest_bets[player] = 0
            elif bet != -1:
                continue  # Skip if player already has a non-negative bet
            elif latest_bets[player] != -1:
                latest_bets[player] = 0  # Treat -1 bet as 0 if there's no previous non-negative bet
            #subtract the latest bet for each player from their balance
            player.balance-=latest_bets[player]
        if all(value > 0.2 for value in latest_bets.values()):
            self.pot -= 0.1
        return sum(value for value in latest_bets.values())
    def Round(self,bet=0):
        '''execute one round'''
        #reset hands
        for x in self.list:
            x.hand=[]
        if self.round==1:
            #pick a dealer
            self.pickdealer()
            self.startingorder=copy.deepcopy(self.order)
        #create a new deck
        self.createdeck()
        #shuffle the deck
        self.shuffledeck()
        #deal each player 2 cards 
        self.deal()
        #preflop
        #add small and big blinds to betting log
        self.bet.append((self.order[1],self.smallblind))
        self.bet.append((self.order[2],self.bigblind))
        #add the small and big blind to the pot
        self.pot=self.smallblind+self.bigblind
        print('order:',[x.name for x in self.order])
        self.bets()
        print(self.bet)
        self.pot=self.potcalc()
        print('pot:',self.pot)
        self.fold_check()
        
        if self.gameover==False:
            #flop
            self.flop()
            self.preflop=False
            self.bet=[]
            self.bets()
            print(self.bet)
            self.pot+=self.potcalc()
            print('pot:',self.pot)
            self.fold_check()
        if self.gameover==False:
            #turn
            self.turn()
            self.preflop=False
            self.bet=[]
            self.bets()
            print(self.bet)
            self.pot+=self.potcalc()
            print('pot:',self.pot)
            self.fold_check()
        if self.gameover==False:
            #river
            self.river()
            self.preflop=False
            self.bet=[]
            self.bets()
            print(self.bet)
            self.pot+=self.potcalc()
            print('pot:',self.pot)
            self.rivercheck=True
            self.fold_check()
            self.evaluate()
        for x in self.list:
            print(x,'  ','balance:',x.balance)
            print(x, x.hand)
        
        #reset variables for next round
        self.order=[]
        self.pot=0
        self.currentprice=self.bigblind
        self.bet=[]
        self.board=[]
        self.deck=[]
        self.rank=[]
        self.preflop=True
        self.rivercheck=False

        #change order for next round
        self.round+=1
        self.gameover=False
        self.order=self.startingorder[-1:]+self.startingorder[:-1]
        
   
    
        
class Player():
    def __init__(self,name,buy):
        self.name=name
        self.balance=buy
        self.hand=[]
        self.currentbet=0
        self.handscore=0
    def __repr__(self):
        return (f'player {self.name}')
    def placebet(self, current_price, valid=True):
        '''place a bet'''
        if valid == False:
            while True:
                try:
                    bet = float(input(f'{self.name}, price is {current_price}, Invalid Bet Size, what is your new bet (0 for check, -1 for fold): '))
                    if bet <= self.balance:  # Check if bet is within balance
                        return bet
                    else:
                        print("Invalid bet. Bet exceeds balance.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        else:
            while True:
                try:
                    bet = float(input(f'{self.name}, price is {current_price}, place your bet (0 for check, -1 for fold): '))
                    if bet <= self.balance:  # Check if bet is within balance
                        return bet
                    else:
                        print("Invalid bet. Bet exceeds balance.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

    
        