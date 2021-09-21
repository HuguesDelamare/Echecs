from view.main_view import View
from controller.player_controller import PlayerController
from controller.tournament_controller import TournamentController
import sys


class Controller:
    def __init__(self):
        self.view = View()
        self.playerController = PlayerController()
        self.tournamentController = TournamentController()

    def main_menu(self):
        while True:
            self.view.show_main_menu()
            val = input(': ')
            if val == "1":
                self.playerController.insert_new_player()
            elif val == "2":
                self.tournamentController.insert_new_tournament()
            elif val == "3":
                ongoing_tournaments = self.tournamentController.\
                    get_ongoing_tournaments()
                if ongoing_tournaments == -1:
                    self.main_menu()
            elif val == "4":
                self.reports_menu()
            elif val == "5":
                sys.exit()
            else:
                continue

    def reports_menu(self):
        while True:
            try:
                self.view.show_reports_menu()
                val = int(input(': '))
                if isinstance(val, int):
                    reports = self.tournamentController.get_reports(val)
                    if reports == -1:
                        self.main_menu()
                else:
                    raise ValueError
            except ValueError:
                print('Enter a number please.')
                continue
