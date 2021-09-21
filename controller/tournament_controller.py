from model.tournament_model import TournamentModel
from model.database_model import DatabaseModel
from view.main_view import View
from datetime import datetime


class TournamentController:
    # Check if the input has the valid format
    def check_text_input(self, input_value):
        while True:
            try:
                answer = str(input('Tournament\'s ' + input_value + ': '))
                if len(answer) >= 3 and answer.isalpha():
                    return answer
                else:
                    raise TypeError
            except TypeError:
                print("Value must be minimum 3 characters and letters only.")
                continue
            except EOFError:
                print("Please input something....")
                continue

    # List every players from DB and
    # ask you to pick 8 of them to play the tournament
    def get_tournament_players(self):
        get_all_players_db = DatabaseModel('playerTable')\
            .get_all_tournament_players()
        View().display_all_players(get_all_players_db)

        players_selected_list = []
        players_selected_count = 0

        while players_selected_count < 8:
            player_selected = int(input('Which player do you wanna select'))
            player = DatabaseModel('playerTable')\
                .select_tournament_player_by_id(player_selected)
            players_selected_list.append(player)
            players_selected_count += 1
        return players_selected_list

    # List every ongoing tournament and
    # ask which one you wanna continue
    def get_ongoing_tournaments(self):
        get_all_ongoing_tournament = DatabaseModel('tournamentTable')\
            .get_all_ongoing_tournament()
        View().display_all_tournaments(get_all_ongoing_tournament)
        while get_all_ongoing_tournament:
            try:
                answer = int(input('Which tournament '
                                   'do you wanna continue ?.'))
                print(answer)
                if 0 < answer <= len(get_all_ongoing_tournament):
                    tournament = get_all_ongoing_tournament[answer - 1]
                    print('We continue the tournament ' + str(answer))
                    play_tournament = self.play_tournament(tournament)
                    if play_tournament == -1:
                        return -1
                else:
                    raise Exception
            except Exception as e:
                print(e)
                continue
        if not get_all_ongoing_tournament:
            print('No tournament ongoing.')

    # Selecting the time control of the tournament
    def set_time_control(self):
        while True:
            try:
                print("The time control is: "
                      "A) Bullet."
                      " B) Blitz."
                      " C) Coup rapide."
                      " [A/B/C] ?")
                time_control_input = input(': ').lower()
                if time_control_input in ('a', 'b', 'c'):
                    return time_control_input
                else:
                    raise TypeError
            except TypeError:
                print("You've to choose between A,B,C")
                continue
            except EOFError:
                print("Please input something....")
                continue

    # Serializing tournament in a valid format for json DB
    def serialize_tournament(self, tournament):
        # Formatting our tournament into a json object
        serialized_tournament = {
            "tournament_name": tournament.name,
            "tournament_place": tournament.place,
            "tournament_date_start": tournament.date_start,
            "tournament_date_end": tournament.date_end,
            "tournament_rounds": tournament.rounds,
            "tournament_turns": tournament.turns,
            "tournament_players_list": tournament.players_list,
            "tournament_time_control": tournament.time_control,
            "tournament_description": tournament.description,
            "tournament_ongoing": True
        }
        return serialized_tournament

    # Create a new tournament to be played and insert in DB
    def insert_new_tournament(self):
        tournament_name = self.check_text_input("Name")
        tournament_place = self.check_text_input("Place")
        tournament_date_start = str(datetime.now().strftime("%d/%m/%Y %H:%M"))
        tournament_date_end = ''
        tournament_rounds = 4
        tournament_players_list = self.get_tournament_players()
        tournament_time_control = self.set_time_control()
        tournament_description = str(input('Choose the description'
                                           ' for your tournament: '))

        new_tournament = \
            TournamentModel(tournament_name,
                            tournament_place,
                            tournament_date_start,
                            tournament_date_end,
                            tournament_rounds,
                            [],
                            tournament_players_list,
                            tournament_time_control,
                            tournament_description,
                            True)

        # Serializing the new created player
        serialized_tournament = self.serialize_tournament(new_tournament)

        # Inserting th new player in our TinyDB
        DatabaseModel('TournamentTable').playerInsertDB(serialized_tournament)

        # Displaying info of the new tournament created
        View().display_new_tournament_infos(serialized_tournament)

        while True:
            answer = \
                input('Do you wanna play the tournament right now ? [Y/n]').\
                lower()
            if answer == "y":
                print("The tournament will start now.")
                self.play_tournament(serialized_tournament)
            elif answer == "n":
                return
            else:
                print('Please choose between [Y]es or [N]o.')
                continue

    # Method to play the 4 turns in the tournament, calling multiple methods
    def play_tournament(self, tournament):
        try:
            turns_count = \
                DatabaseModel('TournamentTable').\
                get_tournament_turn_count(tournament)
            serialized_players_list = \
                self.serialized_players_for_turns(tournament)

            while True:
                if turns_count == 5:
                    print('Tournament is over')
                    DatabaseModel('tournamentTable').\
                        end_tournament(tournament['tournament_name'])
                    return -1
                else:
                    result = []
                    # Preparing the pairs for the different match
                    pairs = \
                        self.creating_pairs(serialized_players_list,
                                            turns_count,
                                            tournament['tournament_name'])
                    print('Turn ' + str(turns_count))

                    # Playing the turn with the new made pairs
                    played_turn = self.play_tournament_turn(pairs, turns_count)

                    # We append the played turned in our tournament turn list
                    result.append(played_turn)

                    # We update the result of the actual tournament
                    # with the new turns results
                    self.update_tournament_turn(tournament, result)

                    # Asking if wanna continue the tournament
                    View().continue_tournament_turns()
                    continue_tournament = input(': ')

                    if continue_tournament == '1':
                        print('Continuing tournament.')
                        turns_count += 1
                        continue
                    elif continue_tournament == '2':
                        print('Leaving tournament.')
                        return -1
        except TypeError:
            print('Error, expecting number got string instead.')
        except EOFError:
            print('Error, expecting something got nothing.')

    # Ending the tournament
    def end_tournament(self, tournament):
        DatabaseModel('tournamentTable').end_tournament(tournament)

    # Updating the tournament turn in DB
    def update_tournament_turn(self, tournament, result):
        # Calling the method to update the tournament with the new turn value
        DatabaseModel('tournamentTable').\
            update_tournament_turn(tournament, result)

    # Playing all the match of the pair list and
    # returning the turn with results
    def play_tournament_turn(self, pairs, turns_count):
        tournament_turns = []
        count = 0
        pairs = list(pairs)
        while count < len(pairs):
            try:
                View().display_tournament_round(pairs[count])
                round_result = input('Who\'s the winner of this round: ')
                if round_result == '1' or\
                        round_result == '2' or\
                        round_result == '3':
                    round_pts_distrib = \
                        self.points_distribution(pairs[count], round_result)
                    tournament_turns.\
                        append(tuple(round_pts_distrib))
                    count += 1
                elif round_result == '':
                    raise EOFError
            except EOFError:
                print("Error, value is empty please select one.")
                continue

        # Pushing the played turn in a new format
        # with the actual round value as key
        serialized_tournament = {
            'Round' + str(turns_count): tournament_turns
        }
        return serialized_tournament

    # Serializing the player list of the tournament in a simpler format
    def serialized_players_for_turns(self, tournament):
        new_format_list = []
        for player in tournament['tournament_players_list']:
            dict = {
                'firstname': player['firstname'],
                'lastname': player['lastname'],
                'ranking': player['ranking'],
                'points': player['points']
            }
            new_format_list.append(dict)
        return new_format_list

    # Distributing the points to players depending on the input value given
    def points_distribution(self, pair, result):
        if result == '1':
            print('Player 1 won, +1pts')
            pair[0]['points'] += 1
        elif result == '2':
            print('Player 2 won, +1pts')
            pair[1]['points'] += 1
        else:
            print('Draw, the two players +0.5pts')
            pair[0]['points'] += 0.5
            pair[1]['points'] += 0.5
        return pair

    # Create a pair of players for the turn
    def creating_pairs(self, playerlist, turns_count, tournament_name):
        try:
            if turns_count == 1:
                # Sorting players based on their ranking
                playerlist.sort(key=lambda e: e['ranking'])

                # Cutting in half our player list
                middle = len(playerlist) // 2

                # Creating a superior and inferior list of players
                superior_players = playerlist[:middle]
                inferior_players = playerlist[middle:]

                # Forming many pairs with players
                # 1 from superior and 1 inferior part
                pairs = zip(superior_players, inferior_players)

                return pairs
            else:
                playerlist = DatabaseModel('TournamentTable').\
                    get_last_played_turn_of_tournament(tournament_name)
                playerlist.sort(key=lambda e: (e['points'], e['ranking']))

                # Cutting in half our player list
                middle = len(playerlist) // 2

                # Creating a superior and inferior list of players
                superior_players = playerlist[:middle]
                inferior_players = playerlist[middle:]

                # Forming many pairs with players
                # 1 from superior and 1 inferior part
                pairs = zip(superior_players, inferior_players)
                for pair in pairs:
                    print(pair)

                return pairs
        except TypeError:
            print('Error, expecting number got string instead.')

    # Method to get the different reports
    def get_reports(self, input_value):
        try:
            # List every players registered
            if input_value == 1:
                self.get_all_players_registred()
            # List every players of a tournament
            elif input_value == 2:
                self.get_players_from_tournament()
            # List every tournaments
            elif input_value == 3:
                self.get_all_tournament()
            # List every turns of a tournamentS
            elif input_value == 4:
                self.get_all_turns_from_tournament()
            # List every match of a tournament
            elif input_value == 5:
                self.get_all_match_from_tournament()
            elif input_value == 6:
                return -1
            else:
                raise ValueError
        except ValueError:
            print('Enter a valid number please.')
            View().show_reports_menu()
            input_value = int(input(': '))
            self.get_reports(input_value)

    def get_all_match_from_tournament(self):
        tournament_list = DatabaseModel('TournamentTable').get_all_tournament()
        View().display_all_tournaments(tournament_list)
        answer = int(input('Which tournament do you wanna select ? : '))
        tournament_turns = DatabaseModel('TournamentTable').\
            get_all_turns_from_tournament(answer)
        View().display_tournament_match(tournament_turns)

    def get_all_turns_from_tournament(self):
        tournament_list = DatabaseModel('TournamentTable').get_all_tournament()
        View().display_all_tournaments(tournament_list)
        answer = int(input('Which tournament do you wanna select ? : '))
        tournament_turns = DatabaseModel('TournamentTable').\
            get_all_turns_from_tournament(answer)
        View().display_tournament_turns(tournament_turns)

    def get_players_from_tournament(self):
        tournament_list = DatabaseModel('TournamentTable').\
            get_all_tournament()
        View().display_all_tournaments(tournament_list)
        tournament_selected = int(input(': '))
        if tournament_selected:
            View().reports_submenu()
            submenu_selected = int(input(': '))
            if submenu_selected == 1:
                all_players = \
                    list(DatabaseModel('TournamentTable').
                         get_tournament_players_from_tournament(
                        tournament_selected))
                all_players.sort(key=lambda e: e['firstname'])
                View().display_all_players(all_players)
            elif submenu_selected == 2:
                all_players = \
                    list(DatabaseModel('TournamentTable').
                         get_tournament_players_from_tournament(
                        tournament_selected))
                all_players.sort(key=lambda e: e['ranking'])
                View().display_all_players(all_players)
            else:
                print('else')

    def get_all_players_registred(self):
        while True:
            View().reports_submenu()
            answer = int(input(': '))
            try:
                if answer == 1:
                    all_players = list(DatabaseModel('playerTable')
                                       .get_all_players())
                    all_players.sort(key=lambda e: e['firstname'])
                    View().display_all_players(all_players)
                    return
                elif answer == 2:
                    all_players = list(DatabaseModel('playerTable')
                                       .get_all_players())
                    all_players.sort(key=lambda e: e['ranking'])
                    View().display_all_players(all_players)
                    return
                else:
                    raise ValueError
            except ValueError:
                print('Wrong value.')
                continue

    def get_all_tournament(self):
        tournament_list = DatabaseModel('TournamentTable').get_all_tournament()
        View().display_all_tournaments(tournament_list)
        return
