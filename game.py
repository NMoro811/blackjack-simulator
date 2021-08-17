#### MAIN GAME FUNCTIONALITY

from clearing import clear
from time import sleep
from random import shuffle

from card_deck import Deck
from player_class import Player
from dealer_class import Dealer

from blackjack_funcs import deal_card_for_all_players, serving, game_on, blackjack, collecting_insurance

list_of_players = [] # To be filled with the Player class instances

# Introduction to the game & instructions
def intro():       

    print("Welcome to BlackJack simulator!")
    print("Instructions: (...)")

    # Choose the number of players
    while True:
        try:
            number_of_players = int(input("Choose the number of players (1-8): "))
        except:
            print("\nAn error has occurred. Please revise your input.\n")
            sleep(3)
            continue
        else:
            if number_of_players in range(1,9):
                break
            else:
                print("\nAn error has occurred. Please make sure you input an integer between 1 and 8.\n")
                sleep(3)

    clear()
           
    print(f"{number_of_players} player(s) confirmed.")
    sleep(2)
    username_count = 0

    clear()

    # Create an object for each player and append it to list_of_players
    while username_count < number_of_players:
        username_count += 1
        player_username = input(f"Player {username_count}, please type in your username: ")
        
        # Revising balance input
        while True:
            try:
                player_balance = int(input(f"\nWelcome, {player_username}. Please insert your current chip balance (1 chip = $1): "))
            except:
                print("\nAn error has occurred. Please revise your input.\n")
                sleep(3)
                continue
            else:
                break
                
        clear()
        
        player = Player(player_username,player_balance) # Creates the corresponding Player instance
        list_of_players.append(player) # Adds the player to list_of_players
        
        # Prints a message if all users are ready
        if username_count == number_of_players:
            print("All Blackjack accounts have been set up correctly. Starting the game...")
            sleep(3)
            return list_of_players
        else:
            continue

def gameplay(list_of_players):

    clear()

    # Basic gameplay setup
    players_dict = {} # Used after the game is over to rank all players according to their performance
    dealer = Dealer()
    deck = Deck()
    deck.shuffle()
    round_number = 0

    # Game logic; it goes on until there are no players left at the table
    while len(list_of_players) > 0:
        round_number += 1
        
        # Reshuffle the cards at the beginning of the round if more than half of them have been dealt in previous rounds
        if len(deck) < 0.5*312:
            print("More than half of the cards have been served; the deck is being reshuffled...")
            sleep(3)
            deck = Deck()
            deck.shuffle()
        
        print(f"\n----- ROUND {round_number} BEGINS -----")
        
        serving(list_of_players, deck, dealer)
        list_of_insured = [] # To be used in case someone asks for Insurance
        dealer_showed_card = False # By default
        dealer_checks_card = 0
        
        # Iterate through players
        for player in list_of_players:
            
            clear()
            
            if player.name[-1] in ['s','S']:
                print(f"\n----- ROUND {round_number}: {player.name}' TURN -----")
            else:
                print(f"\n----- ROUND {round_number}: {player.name}'s TURN -----")
            
            # Iterate through each player's hands
            index = 0
            while index in range(0,len(player)):

                # Executed at the beginning of the round and after every 'Hit' 
                # Iterates until player has played all their hands
                while (not player.standing_one and player.bet_on_hands[0] > 0) or (not player.standing_two and player.bet_on_hands[1] > 0):
                    
                    # Player will have already seen their cards if they have chosen to double down; else, they will be shown
                    if not player.doubling:
                        player.show_cards(index)
                        dealer.show_first_card()

                    ## Evaluate if a result has been produced, and ask the player for their choice if that's not the case
                    # Soft hand
                    if player.hands_values[index] > 21 and 11 in player.hands_separate_values[index]:
                        # Soft hand: treat first Ace in player.hands_separate_values as 1 instead of 11 and
                        # return to the beginning of the loop
                        print("Soft value over 21: Ace takes a value of '1'.\n")
                        sleep(2)
                        player.hands_values[index] -= 10 
                        indx = player.hands_separate_values[index].index(11)
                        player.hands_separate_values[index][indx] = 1
                        continue
                    # BUST
                    elif player.hands_values[index] > 21:
                        print("BUST! You lose this hand's bet\n")
                        sleep(2)
                        player.bet_on_hands[index] = 0
                        if index+1 == len(player):
                            game_on(list_of_players, players_dict, player) # Ask the player if they want to continue
                        break
                    # Player has a natural, so the dealer must check the face-down card to decide if it's Blackjack or a stand-off 
                    elif player.hands_values[index] == 21 and dealer.hands_separate_values[0] in [10,11]:
                        # Dealer only needs to check face-down card once
                        if dealer_checks_card == 0:
                            print("Possible Blackjack; the dealer checks the face-down card...\n")
                            sleep(4)
                        # Dealer also has a natural; they show the card and the round is over
                        if dealer.hands_values == 21:
                            print("\nStand-off! You retrieve your bet. All players without naturals lose their bet. \n")
                            sleep(2)
                            dealer.show_all_cards()
                            player.balance += player.bet_on_hands[index]
                            player.bet_on_hands = [0,0]
                            dealer_showed_card = True
                            game_on(list_of_players, players_dict, player) # Ask the player if they want to continue
                            break
                        # Dealer does not have a natural; player has Blackjack
                        else:
                            dealer_checks_card = 1 # Don't check face-down card anymore
                            blackjack(list_of_players, players_dict, player, index)
                            break
                    # Blackjack since a stand-off is not possible
                    elif player.hands_values[index] == 21:
                        blackjack(list_of_players, players_dict, player, index)
                        break

                    # If none of the previous statements apply, it means no result has been produced yet.
                    # Therefore, the player has a choice to make as long as they haven't doubled or split aces in the previous round.
                    # However, 'doubling players' cannot reach this point since they are either standing_one (<21) or have had a result (>= 21)
                    # Note that, due to the above, Insurance cannot be played after Double Down.
                    
                    choices = ['H','HIT', 'ST', 'STAND'] # Two basic options

                    # Equivalent to "If the player's cards are just the two original cards at the beginning"
                    if len(player.hands[0]) == 2 and len(player.hands[1]) == 0:
                        if player.balance >= player.bet_on_hands[index]:
                            choices.extend(['DD', 'DOUBLE DOWN', 'DOUBLE'])
                        card1 = player.hands[0][0] 
                        card2 = player.hands[0][1]
                        if card1.rank == card2.rank and player.balance >= player.bet_on_hands[0]:
                            choices.extend(['SP', 'SPLIT'])
                        if dealer.hands_separate_values[0] == 11 and len(list_of_insured) == 0 and player.balance >= 0.5*player.bet_on_hands[0]: # Dealer's face-up card is an ace & insurance not collected yet
                            choices.extend(['IN', 'INSURANCE'])

                    # Asking the user for their choice based on what options are available from the previous if-clause
                    decision = 'z&+#$%' # Just a dummy value the user will (hardly ever) not enter
                                        # Even if the user were to find this exception it would not affect the functionality below

                    while decision.upper() not in choices:

                        if decision != 'z&+#$%':
                            print("Not a valid choice. Please try again.") # Rather cosmetic; prints for all unexpected user inputs

                        if choices == ['H','HIT', 'ST', 'STAND']:
                            decision = input("Hit (H) or Stand (ST)? ")
                        elif set(['DD','SP','IN']).issubset(set(choices)):
                            decision = input("Hit (H), Stand (ST), Double Down (DD), Split Pairs (SP) or Insurance (IN)? ")
                        elif set(['DD','SP']).issubset(set(choices)):
                            decision = input("Hit (H), Stand (ST), Double Down (DD) or Split Pairs (SP)? ")
                        elif set(['DD','IN']).issubset(set(choices)):
                            decision = input("Hit (H), Stand (ST), Double Down (DD) or Insurance (IN)? ")
                        else:
                            decision = input("Hit (H), Stand (ST) or Double Down (DD)? ")

                    # Result: the user's choice has been stored and can be used now to execute the corresponding function(s) and method(s)
                    if decision.upper() in ['H','HIT']:
                        player.add_card(deck.deal_one(), index)
                        continue
                    elif decision.upper() in ['ST','STAND']:
                        player.stand(index)
                        break
                    elif decision.upper() in ['DD','DOUBLE DOWN','DOUBLE']:
                        player.double_down(dealer, deck)
                        continue
                    elif decision.upper() in ['IN','INSURANCE']:
                        player.insurance(list_of_insured)
                        collecting_insurance(list_of_players, list_of_insured, player)
                        print("\nDealer checks the face-down card...\n")
                        sleep(3)
                        if dealer.hands_values != 21:
                            print("The bet fails; the value of the face-down card is not 10.\n")
                            sleep(2)
                        else:
                            print("It is a Blackjack! The hand is over and all main bets are collected.")
                            sleep(3)
                            for ins in list_of_insured:
                                ins.balance += 2*ins.insurance_bet
                            dealer_showed_card = True
                            break
                    # User has chosen to split pairs
                    else:
                        player.split()
                        if card1.rank == 'Ace':
                            print("With a pair of aces, the player is given one card for each ace and may not draw again. ")
                            sleep(3)
                            player.add_card(deck.deal_one(), 0)
                            player.add_card(deck.deal_one(), 1)
                        else:
                            pass # Player can choose to hit multiple times per hand before standing, so we go back to the beginning of the loop
                
                index += 1
            
            clear()
            
            # All players who haven't played yet must stand on their first two cards if the dealer has showed their second card
            if dealer_showed_card:
                for play in list_of_players:
                    if not play.standing_one and play.bet_on_hands[0] > 0:
                        play.stand(0)
                    if not play.standing_two and play.bet_on_hands[1] > 0:
                        play.stand(1)
                break # Break out of the player iteration
        
        clear()
        
        ## At this point, all players are either out or standing. 
        # Next: if one or more players are standing, dealer reveals hidden card and hands out/collects money. Else, we move on to the
        # next round (unless all players have quit)
        
        standing_one_players = [player for player in list_of_players if player.standing_one and player.bet_on_hands[0] > 0] # Only containing standing players who did not split pairs
        standing_two_players = [player for player in list_of_players if player.standing_two and player.bet_on_hands[1] > 0] # Players standing on a secondary hand
        
        if len(standing_one_players)+len(standing_two_players)> 0 and not dealer_showed_card:
            # Note: if standing_one_players.extend(standing_two_players) <--> if len(...) > 0
            print(f"\n----- ROUND {round_number}: DEALER'S TURN -----")
            print("\nThe dealer has served every player: the face-down card is turned up...\n")
            sleep(4)
            dealer.show_all_cards() # Shows both cards

            ## Dealer game logic
            sleep(2)
            
            # Determines dealer final hand-value
            while dealer.hands_values < 17:
                dealer.add_card(deck.deal_one())
                print("Dealer takes a card.\n")
                sleep(2)
                dealer.show_all_cards()

                if dealer.hands_values > 21 and 11 in dealer.hands_separate_values:
                    # Soft hand: treat first Ace in player.hands_separate_values as 1 instead of 11 and
                    # return to the beginning of the loop
                    print("Soft value over 21: Ace takes a value of '1'.\n")
                    sleep(2)
                    dealer.hands_values -= 10 
                    indx = dealer.hands_separate_values.index(11)
                    dealer.hands_separate_values[indx] = 1
                    continue
                elif dealer.hands_values > 21:
                    sleep(2)
                    print("Dealer busts! All standing players win the amount of their bet.\n")
                    sleep(3)
                    break
                elif dealer.hands_values >= 17:
                    sleep(2)
                    print(f"Dealer stands at {dealer.hands_values}.\n")
                    sleep(3)
                    break
                else:
                    pass
                
        print(f"\n----- PAYOUTS -----")
        # Rewards are collected depending on hand value     
        for player in list_of_players:
            
            if player not in standing_one_players and player not in standing_two_players:
                pass
            else:
                # Iterate through each player's hands
                for index in range(0,len(player)):
                    sleep(2)
                    
                    if len(player) > 1:
                        print(f"{player.name}: Hand No. {index+1}.\n")
                        sleep(3)
                        
                    if index == 0 and player not in standing_one_players or index == 1 and player not in standing_two_players:
                        print("A result has already been produced.\n")
                    elif dealer.hands_values > 21 or player.hands_values[index] > dealer.hands_values:
                        print(f"{player.name} is paid back {2*player.bet_on_hands[index]} chips from this hand.\n")
                        player.balance += 2*player.bet_on_hands[index]
                    elif player.hands_values[index] == dealer.hands_values:
                        print(f"There is a stand-off between {player.name} and the dealer; the player retrieves the bet from this hand.\n")
                        player.balance += player.bet_on_hands[index]
                    elif dealer_showed_card:
                        print(f"{player.name} lost their bet from this hand.\n")
                    else:
                        print(f"{player.name} lost their bet from this hand (stood at {player.hands_values[index]}).\n")
            
                # Ask each standing player if they wish to play the next round; the rest have been asked before
                sleep(3)
                game_on(list_of_players, players_dict, player)
            
            # Stop standing_one, reset bet and cards for all players (not just standing_one) & the dealer
            player.clear_cards()
            player.bet_on_hands = [0,0]
            player.standing_one = False
            player.standing_two = False
            player.doubling = False
        
        clear()
        
        # Clear dealer's cards once all players have been paid/lost their bets
        dealer.clear_cards()
        
        # Runs at the end of every round; reshape the list of players at the table
        list_of_players = [play for play in list_of_players if play.playing]
    return players_dict

def game_conclusion(players_dict):

    sleep(2)
    print("\nAll players have left the table now; the game has concluded.")
    print("\nOverall results from today's game, ranking by gain percentage: ")

    # Sorting the dictionary by gain percentage
    ranking = {k: v for k, v in sorted(players_dict.items(), reverse=True, key=lambda item: item[1])}

    # Closure
    rank_num = 0

    for player in ranking:
        rank_num += 1
        print(f"\n{rank_num})         {player}         {ranking[player]} %")
        
    input("\nThank your for playing! Press Enter to close the program. ")