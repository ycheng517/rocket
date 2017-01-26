from nba_py import team
from nba_py import game
from nba_py import player
from nba_py.constants import *
import pandas as pd
import pprint

ap = player.PlayerSummary("977")
full_dict = {}
pprint.pprint(ap.headline_stats().to_dict())
print "*" * 40
pprint.pprint(ap.info().to_dict())
