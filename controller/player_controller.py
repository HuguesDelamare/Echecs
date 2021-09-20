from model.player_model import PlayerModel as PlayerModel
from model.database_model import DatabaseModel
from view.main_view import View
import datetime


class PlayerController:
    # Set the player birthdate
    def set_player_birthdate(self):
        while True:
            player_birthdate_input = str(input('Choose a birthdate: '))
            try:
                datetime.datetime.strptime(player_birthdate_input, "%d/%m/%Y")
                return player_birthdate_input
            except ValueError:
                print('Asking for %d/%m/%Y format, ' + str(player_birthdate_input) + ' given.')
                continue
            except TypeError:
                print("Value must be minimum 3 characters and letters only.")
                continue
            except EOFError:
                print("Please input something....")
                continue

    # Check if the input has the valid format
    def check_text_input(self, input_value):
        while True:
            try:
                answer = str(input('Player\'s ' + input_value + ': '))
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

    # Set the player gender
    def set_player_gender(self):
        while True:
            try:
                gender_input = str(input('Player gender: [M]ale or [F]emale ?: '))
                if gender_input.lower() == "m" or "f" and len(gender_input) == 1:
                    return gender_input.capitalize()
                else:
                    print("Choose between [M] or [F].")
                    continue
            except TypeError:
                print("Letters only please.")
                continue
            except EOFError:
                print("Please input something....")
                continue

    # Serializing player in a valid format for json DB
    def serialize_player(self, player):
        # Formatting our player into a json object
        serialized_player = {
            "lastname": player.lastname,
            "firstname": player.firstname,
            "birthdate": player.birthdate,
            "gender": player.gender,
            "ranking": player.ranking,
            "points": 0
        }
        return serialized_player

    # Create a new player to insert in DB
    def insert_new_player(self):
        player_firstname = self.check_text_input("firstname")
        player_lastname = self.check_text_input("lastname")
        player_birthdate = self.set_player_birthdate()
        player_gender = self.set_player_gender()
        player_ranking = int(input('Choisis un ranking: '))

        new_player = PlayerModel(player_lastname, player_firstname,
                                 player_birthdate, player_gender, player_ranking, 0)

        # Serializing the new created player
        serialized_player = self.serialize_player(new_player)

        # Inserting th new player in our TinyDB
        DatabaseModel('playerTable').playerInsertDB(serialized_player)

        # Displaying info of the new player created
        View().display_new_player_infos(serialized_player)


