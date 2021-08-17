from clearing import clear
from game import intro, gameplay, game_conclusion

def main():
	clear()
	list_of_players = intro()
	players_dict = gameplay(list_of_players)
	game_conclusion(players_dict)

if __name__ == '__main__':
    main()