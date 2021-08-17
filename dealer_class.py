class Dealer():
    def __init__(self):
        self.hands = ['(Face-down card)']
        self.hands_separate_values = [] # Integer value of each card in order
        self.hands_values = 0 # Sum of value of the cards in hand
        
    def add_card(self, card): # Needs to be overwritten after implementing Split since Dealer has only one hand (indexing not supported)
        self.hands.append(card)
        self.hands_separate_values.append(card.value)
        self.hands_values += card.value
      
    def show_first_card(self): # Print the dealer's cards (except the second one)
        print("Dealer's cards: ")
        # Prints only first card; the other one (if served) remains hidden until the end
        if len(self.hands)-1 == 1:
            print(self.hands[1])
        else:
            cards_with_hidden = [self.hands[1],self.hands[0]]
            print(*cards_with_hidden, sep=', ')
        print('') 
    
    def show_all_cards(self): # Print all the dealer's cards; to be used at the end of the round
        print("Dealer's cards: ")
        # Deletes '(Face-down card)' entry if still present
        if self.hands[0] == '(Face-down card)':
            self.hands.pop(0)
        # Prints all current player's cards
        print(*self.hands, sep=', ')
        print('')    
        
    def clear_cards(self):
        self.hands = ['(Face-down card)']
        self.hands_separate_values = []
        self.hands_values = 0