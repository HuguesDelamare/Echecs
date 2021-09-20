
class TournamentModel:
    def __init__(self, name, place, date_start,
                 date_end, rounds, turns,
                 players_list, time_control, description,
                 ongoing):
        self.name = name
        self.place = place
        self.date_start = date_start
        self.date_end = date_end
        self.rounds = rounds
        self.turns = turns
        self.players_list = players_list
        self.time_control = time_control
        self.description = description
        self.ongoing = ongoing
