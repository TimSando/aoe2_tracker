import datetime
import json
import random
import os

import pandas as pd
from pick import pick


def load_data(
    data_filename: str,
    list_filename: str = "lists.json",
):

    if os.path.exists(data_filename):
        player_data = pd.read_csv(data_filename)
    else:
        player_data = pd.DataFrame()
    with open(list_filename) as f:
        list_info = json.load(f)
        return list_info, player_data


def select_players(ref_list: dict):
    num_players, _ = pick([1, 2, 3, 4, 5, 6, 7], "Please select number of players for tonight's game")
    players = {}
    player_list = ref_list["players"]
    for player in range(num_players):
        _, idx = pick(player_list, "Please select who is playing")
        players[player_list[idx]] = {}
        player_list.pop(idx)
    return players


def assign_civ(ref_list: dict, game_players: dict, player_data):
    """Assign random civ to a player

    Args:
        ref_list (dict): [description]
    """
    all_civs = ref_list["civilisations"]
    # banned_civs = []
    if not "civilisation" in player_data:
        banned_civs = []
    else:
        banned_civs = player_data[player_data["game_date"] == str(datetime.date.today())].civilisation.unique()
    available_civs = [civ for civ in all_civs if civ not in banned_civs]
    for player in game_players:
        civ_allocation = random.choice(available_civs)
        game_players[player]["civilisation"] = civ_allocation
        available_civs.remove(civ_allocation)
        print(f"{player}: {game_players[player]['civilisation']}")
    return game_players


def save_data(player_assignment, filename, player_data):
    player_df = pd.DataFrame.from_dict(player_assignment, orient="index")
    player_df.index.name = "player_name"
    player_df.reset_index(level=0, inplace=True)
    player_df["game_date"] = datetime.date.today()
    player_df["start_time"] = datetime.datetime.now().strftime("%H:%M")
    player_data = pd.concat([player_data, player_df], ignore_index=True, axis=0)
    player_data.to_csv(filename, index=False)


if __name__ == "__main__":
    ref_list, player_data = load_data(data_filename="saved_game_information.csv", list_filename="lists.json")
    game_players = select_players(ref_list)
    player_assignment = assign_civ(ref_list, game_players, player_data)
    save_data(player_assignment, "saved_game_information.csv", player_data)
