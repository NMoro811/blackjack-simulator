from time import sleep
from clearing import clear

from player_class import Player

def deal_card_for_all_players(list_of_players, deck):
    # Only works if called after list_of_players is defined
    for player in list_of_players:
        player.add_card(deck.deal_one())
        player.show_cards()
        sleep(2)

def serving(list_of_players, deck, dealer):
    # To be executed at the beginning of each round
    
    # All players place their bets
    for player in list_of_players:
        player.bet()
    
    print("----- FIRST CARD -----")
    # Serves each player & the dealer first card (all face up)
    deal_card_for_all_players(list_of_players, deck) # Players
    dealer.add_card(deck.deal_one()) # Dealer
    dealer.show_first_card()
    sleep(5)

    clear()
    
    print("----- SECOND CARD -----")
    # Serves each player & the dealer second card (all face up except the dealer's second card)
    deal_card_for_all_players(list_of_players, deck) # Players
    dealer.add_card(deck.deal_one()) # Dealer
    dealer.show_first_card()
    sleep(5)

def game_on(list_of_players, players_dict, player):
    
    # In case player runs out of credit
    if player.balance < 2:
        print(f"{player.name} has run out of credit; they cannot play the next round. ")
        player.playing = False
        # When the player leaves the table, we gather their results to be displayed in the ranking at the end of the day
        players_dict[player.name] = round(100*(player.balance - player.initial_balance)/player.initial_balance,2)
        return
    
    # Credit is sufficient; player can choose to continue
    keep_playing = 'z' # Just a dummy value
    
    while keep_playing.upper() not in ['Y','N']:
        keep_playing = input(f"Would you like to join the next round, {player.name}? Type in 'Y' or 'N': ")
        if keep_playing.upper() not in ['Y','N']:
            print("Not a valid choice. Please try again.")
            sleep(3)
            continue
        else:
            break

    if keep_playing.upper() == 'Y':
        print(f"\n{player.name} remains at the table for the next round.")
        sleep(2)
    else:
        print(f"\n{player.name} leaves the table.")
        sleep(2)
        player.playing = False
        # When the player leaves the table, we gather their results to be displayed in the ranking at the end of the day
        players_dict[player.name] = round(100*(player.balance - player.initial_balance)/player.initial_balance,2)
    return players_dict
    
def blackjack(list_of_players, players_dict, player, index=0):
    if len(player) == 1:
        print(f"Blackjack! You are paid {1.5*player.bet_on_hands[0]} chips.")
        sleep(3)
        player.balance += 1.5*player.bet_on_hands[0]
    elif len(player) > 1:
        print(f"Blackjack! But you are paid {player.bet_on_hands[index]} chips (instead of {1.5*player.bet_on_hands[index]}) since you split pairs.")
        sleep(3)
        player.balance += player.bet_on_hands[index]
    player.bet_on_hands[index] = 0
    if index+1 == len(player):
        game_on(list_of_players, players_dict, player) # Ask the player if they want to continue (only if all their hands have been played)
    else:
        pass # Move on to the next hand (in the enclosing While loop) if that was not the last
    
def collecting_insurance(list_of_players, list_of_insured, player):
    # Collects players who can still place an Insurance bet
    available_for_insurance = [player for player in list_of_players if not player.standing_one and player.bet_on_hands[0] > 0 and player.balance >= player.bet_on_hands[0]]
    # Removes the current (i.e., iterated) player from the list since they've asked for it the first
    available_for_insurance.remove(player)
    # Asks the remaining players if they wish to place an Insurance bet too
    for play in available_for_insurance:
        ask_insurance = 'z' # Just a dummy value
        while ask_insurance.upper() not in ['Y','N']:
            ask_insurance = input(f"Would you like to ask for Insurance too, {play.name}? Type in 'Y' or 'N': ")
            if ask_insurance.upper() not in ['Y','N']:
                print("Not a valid choice. Please try again.")
                sleep(3)
                continue
            else:
                break
        if ask_insurance.upper() == 'Y':
            play.insurance(list_of_insured)