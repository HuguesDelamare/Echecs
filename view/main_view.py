
class View:
    def show_main_menu(self):
        print("1. Create player")
        print("2. Create tournament")
        print("3. Continue tournament")
        print("4. Check reports")
        print("5. Exit")

    def display_new_player_infos(self, serialized_player):
        print('New player ' + serialized_player['firstname'] + ' ' +
              serialized_player['lastname'] + ' has been registred.')

    def display_new_tournament_infos(self, serialized_tournament):
        print('New tournament ' + serialized_tournament['tournament_name'] +
              ' was created the ' +
              serialized_tournament['tournament_date_start'] +
              ' for a total of ' +
              str(serialized_tournament['tournament_rounds']) +
              ' rounds and ' +
              str(len(serialized_tournament['tournament_players_list'])) +
              ' players.')

    def ongoing_tournament_message(self):
        print('A tournament is already ongoing.')

    def continue_tournament_message(self):
        print('Do you wanna continue the tournament ?')

    def display_all_players(self, list_of_players):
        print('--- PLAYERS LIST ---')
        for count, player in enumerate(list_of_players, start=1):
            print(str(count) + ': ' + player['firstname'] +
                  ' ' + player['lastname'] + " |" +
                  " Rank: " + str(player['ranking']))
        print('----------------------')
        print('')

    def display_all_tournaments(self, list_of_tournaments):
        print('--- TOURNAMENTS LIST ---')
        for count, tournament in enumerate(list_of_tournaments, start=1):
            print(str(count) +
                  ". " + tournament['tournament_name'] +
                  " | " + tournament['tournament_place'] +
                  " | " + str(tournament['tournament_date_start']) +
                  " | Turns: " + str(len(tournament['tournament_turns'])))
        print('----------------------')
        print('')

    def display_tournament_round(self, pair):
        print(pair[0]['firstname'] +
              ' VS ' + pair[1]['firstname'])

    def continue_tournament_turns(self):
        print("Turn is over, do you wanna continue or quit ?")
        print("1. Continue")
        print("2. Exit tournament")

    def show_reports_menu(self):
        print('--- REPORTS MENU  ---')
        print("1. List every players registered")
        print("2. List every players of a tournament")
        print("3. List every tournaments")
        print("4. List every turns of a tournament")
        print("5. List every match of a tournament")
        print("6. Exit")

    def reports_submenu(self):
        print('What do you wanna do ?')
        print("1. Sort by alphabetic order.")
        print("2. Sort by Ranking.")
        print(' ')

    def display_tournament_turns(self, list_of_turns):
        print('--- TOURNAMENT TURNS REPORTS ---')
        for count, turn in enumerate(list_of_turns, start=1):
            print(turn)
        print('----------------------')
        print('')

    def display_tournament_match(self, list_of_turns):
        print('--- TOURNAMENT MATCH REPORTS ---')
        for roundCount, turn in enumerate(list_of_turns, start=1):
            print(' ')
            print('ROUND N° ' + str(roundCount))
            for matchCount, match in enumerate(turn['Round'+str(roundCount)], start=1):
                print(
                    str(matchCount) + "." +
                    match[0]['firstname'] +
                    ' ' + match[0]['lastname'] +
                    ' ' + str(match[0]['points']) +
                    ' VS ' + match[1]['firstname'] +
                    ' ' + match[1]['lastname'] + ' ' +
                    str(match[1]['points']))
        print('----------------------')
        print(' ')
