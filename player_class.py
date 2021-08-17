from clearing import clear
from time import sleep

from card_deck import Card, Deck

class Player:
    
    def __init__(self, name, balance):
        # In-game attributes
        self.name = name
        self.balance = balance
        self.hands = [[],[]] # A new player has no cards at the beginning. Furthermore, a player can have up to 2 hands (splitting once)
        self.hands_separate_values = [[],[]] # Integer value of each card in order
        self.bet_on_hands = [0,0] # In terms of chips
        self.hands_values = [0,0] # Sum of value of the cards in hand
        # To report results at the end of the game
        self.initial_balance = balance # Stored to compare with final balance and report overall wins/losses
        # 'State' Booleans; default values
        self.playing = True
        self.standing_one = False
        self.standing_two = False # Used for the second hand after splitting
        self.doubling = False
    
    # Returns the number of hands; useful for splitting function
    def __len__(self):
        non_empty_hands = [hand for hand in self.hands if len(hand) > 0]
        return len(non_empty_hands)
        
    def add_card(self, card,index=0): # Also used for 'Hitting'
        self.hands[index].append(card)
        self.hands_separate_values[index].append(card.value)
        self.hands_values[index] += card.value
        
    def show_cards(self,index=0): # Print the player's cards
        # Rather cosmetic: checks correct form of possessive
        if self.name[-1] in ['s','S']:
            print(self.name+"' cards: ")
        else:
            print(self.name+"'s cards: ")
        # Prints all current player's cards
        if len(self) > 1 and index == 0: 
            print("(Left hand)")
        elif len(self) > 1 and index == 1:
            print("(Right hand)")
        print(*self.hands[index], sep=', ')
        print('')
        
    def clear_cards(self):
        self.hands = [[],[]]
        self.hands_separate_values = [[],[]]
        self.hands_values = [0,0]
    
    def stand(self,index=0):
        if index == 0:
            self.standing_one = True
        elif index == 1:
            self.standing_two = True
    
    def bet(self):
        while self.bet_on_hands[0] == 0:
            try:
                print(f"Current balance: {self.balance}.")
                amount = int(input(f"Please place your bet, {self.name} (must add up to min. 2, max. 500): "))
            except ValueError:
                print("Incorrect format. Please try again; make sure to insert an integer. ")
                sleep(3)
                continue
            else:
                if amount+self.bet_on_hands[0] in range(2,501) and amount <= self.balance:
                    self.bet_on_hands[0] += amount
                    self.balance -= amount
                elif amount <= self.balance:
                    print(f"Invalid: amount exceeds current balance. ")
                    sleep(3)
                elif amount+self.bet_on_hands[0] not in range(2,501):
                    print(f"The placed amount is invalid ({amount+self.bet_on_hands[0]} chips not in 2-500 limit). ")
                    sleep(3)
            finally:
                clear()
        
        print(f"A bet of {amount} chips has been placed. Total chips on table from {self.name}: {self.bet_on_hands[0]}. \n")
        sleep(3)
        clear()
    
    # Note: one CANNOT double down after your split in this 'casino', so this function only applies for the first (and only) hand
    def double_down(self, dealer, deck):
        print(f"Double Down! {self.name} receives another card...\n")
        sleep(3)
        self.balance -= self.bet_on_hands[0]
        self.bet_on_hands[0] = 2*self.bet_on_hands[0]
        self.add_card(deck.deal_one())
        self.show_cards()
        dealer.show_first_card()
        if self.hands_values[0] < 21 or 11 in self.hands_separate_values[0] and self.hands_values[0]-10 < 21:
            print(f"{self.name} has not gone bust, so they must stand on the present cards. ")
            sleep(3)
            self.stand()
        else:
            pass # Will continue in the loop
        self.doubling = True
    
    # Similarly, one CANNOT ask for Insurance after splitting: either at the beginning of the player's round or not at all
    # However, one CAN split after Insurance
    def insurance(self, list_of_insured): # For the first player to ask for Insurance
        print(f"\n{self.name} has placed a side bet of {0.5*self.bet_on_hands[0]} on a blackjack for the house.\n")
        sleep(3)
        self.insurance_bet = 0.5*self.bet_on_hands[0]
        self.balance -= self.insurance_bet
        list_of_insured.append(self)
        
    # (See collecting_insurance function below for the potential collection of other such side bets)
    
    def split(self):
        print(f"\n{self.name} has decided to split pairs. The amount of the initial bet has been assigned to both hands.\n ")
        self.balance -= self.bet_on_hands[0]
        self.hands = [[self.hands[0][0]],[self.hands[0][1]]]
        self.hands_separate_values = [[self.hands_separate_values[0][0]],[self.hands_separate_values[0][1]]]
        self.bet_on_hands = [self.bet_on_hands[0],self.bet_on_hands[0]]
        self.hands_values = [self.hands_values[0]*0.5,self.hands_values[0]*0.5]