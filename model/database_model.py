from tinydb import TinyDB, where
from tinydb.operations import add, set
from datetime import datetime


class DatabaseModel:
    def __init__(self, database_table):
        self.database_table = database_table

    # Will insert the given player in the PlayerTable
    def playerInsertDB(self, serialized_player):
        TinyDB("./database/tournament_database.json").table(self.database_table).insert(serialized_player)

    # Will insert the given tournament in the TournamentTable
    def tournamentInsertDB(self, serialized_player):
        TinyDB("./database/tournament_database.json").table(self.database_table).insert(serialized_player)

    # Get and return the player by his ID
    def select_tournament_player_by_id(self, selected_player):
        result = TinyDB("./database/tournament_database.json").table('playerTable').get(doc_id=selected_player)
        return result

    # Get all the players in PlayerTable and return them as list
    def get_all_tournament_players(self):
        try:
            list_of_players = []
            player_database = TinyDB("./database/tournament_database.json").table('playerTable')
            if len(player_database) >= 8:
                for player in player_database:
                    list_of_players.append(player)
                return list_of_players
            else:
                print(str(len(player_database)) + 'players registred, need at least 8 to start a tournament.')
        except TypeError:
            print('error')

    def get_all_tournament(self):
        try:
            tournament_list = []
            tournament_database = TinyDB("./database/tournament_database.json").table('TournamentTable')
            for tournament in tournament_database:
                tournament_list.append(tournament)
            return tournament_list
        except Exception as e:
            print(e)

    # Will check if there's any tournament ongoing and return a list of them
    def get_all_ongoing_tournament(self):
        try:
            ongoing_tournament_list = []
            tournament_database = TinyDB("./database/tournament_database.json").table('TournamentTable')
            for tournament in tournament_database:
                if tournament['tournament_ongoing'] is True:
                    ongoing_tournament_list.append(tournament)
                else:
                    pass
            return ongoing_tournament_list

        except Exception as e:
            print(e)

    # Insert the results of match from a turn in the tournament turn
    def update_tournament_turn(self, tournament, result):
        try:
            tournament_database = TinyDB("./database/tournament_database.json").table('TournamentTable')
            tournament_database.update(add('tournament_turns', result),
                                       (where('tournament_name') == tournament['tournament_name']))
        except Exception as e:
            print(e)

    # Return the number of played turn of a given tournament
    def get_tournament_turn_count(self, tournament):
        tournament_database = TinyDB("./database/tournament_database.json").table('TournamentTable')
        tournament = tournament_database.search(where('tournament_name') == tournament['tournament_name'])[0]
        tournament_turns_count = len(tournament['tournament_turns'])
        if tournament_turns_count == 0:
            tournament_turns_count += 1
        elif tournament_turns_count == 4:
            tournament_turns_count = 5
        else:
            tournament_turns_count += 1
        return tournament_turns_count

    # Get the last turn played from a tournament and return it
    def get_last_played_turn_of_tournament(self, tournament_name):
        tournament_database = TinyDB("./database/tournament_database.json").table('TournamentTable')
        tournament = tournament_database.search(where('tournament_name') == tournament_name)
        last_turn = tournament[0]['tournament_turns'][-1]
        player_list = []
        for turn in last_turn:
            for match in last_turn[turn]:
                player_list.extend(match)
        return player_list

    def end_tournament(self, tournament_name):
        tournament_database = TinyDB("./database/tournament_database.json").table('TournamentTable')
        tournament_database.update(set('tournament_ongoing', False), (where('tournament_name') == tournament_name))
        tournament_database.update(set('tournament_date_end', str(datetime.now().strftime("%d/%m/%Y %H:%M"))),
                                   (where('tournament_name') == tournament_name))

    def get_all_tournament(self):
        tournament_database = TinyDB("./database/tournament_database.json").table('TournamentTable')
        tournament_database.all()

        return tournament_database

    def get_all_players(self):
        tournament_database = TinyDB("./database/tournament_database.json").table('playerTable')
        tournament_database.all()
        return tournament_database

    def get_all_turns_from_tournament(self, tournament_id):
        tournament_database = TinyDB("./database/tournament_database.json").table('TournamentTable')
        tournament_turns = tournament_database.get(doc_id=tournament_id)['tournament_turns']
        return tournament_turns

    def get_tournament_players_from_tournament(self, tournament_id):
        tournament_database = TinyDB("./database/tournament_database.json").table('TournamentTable')
        tournament_players_list = tournament_database.get(doc_id=tournament_id)['tournament_players_list']
        return tournament_players_list
