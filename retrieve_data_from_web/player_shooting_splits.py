import pandas
from nba_py import player as nba_py_player
from utilities import season_to_season_id


class PlayerShootingSplits(object):
    def __init__(self, db, seasons):
        self.db = db
        self.seasons = seasons
        self.get_player_shooting_splits()

    def get_player_shooting_splits(self):
        for season in self.seasons:
            player_list = nba_py_player.PlayerList(season=season).info()
            if isinstance(player_list, pandas.DataFrame):
                for index, row in player_list.iterrows():
                    if self.db.player_shooting_splits.count({"SEASON_ID": season_to_season_id(season),
                                                             "PLAYER_ID": str(row.PERSON_ID)}) > 0:
                        print("shooting splits of {} {} already exists, skipping".format(season, row.DISPLAY_FIRST_LAST))
                        continue
                    print("retrieving player shooting splits for {} {}".format(season, row.DISPLAY_FIRST_LAST))
                    shooting_splits = nba_py_player.PlayerShootingSplits(player_id=row.PERSON_ID, season=season).shot_5ft()
                    if isinstance(shooting_splits, pandas.DataFrame):
                        shooting_splits = shooting_splits.to_dict("records")
                    if shooting_splits:
                        for shooting_range in shooting_splits:
                            shooting_range['PLAYER_ID'] = str(row.PERSON_ID)
                            shooting_range['SEASON_ID'] = season_to_season_id(season)
                            shooting_range['PLAYER_NAME'] = row.DISPLAY_FIRST_LAST
                        self.db.player_shooting_splits.insert_many(shooting_splits)
                    else:
                        print("shooting splits of {} {} not found".format(season, row.DISPLAY_FIRST_LAST))
