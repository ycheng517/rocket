import pprint
from Queue import Queue
from threading import Thread
import pymongo

client = pymongo.MongoClient("52.41.48.61", 27017)
db = client.nba_stats

# are there a group of players who do bad against good opponent defense?
# ================================

# find tiers of pts allowed in 2013
all_opp_stats = db.team_opponent_stats.find({'SEASON_YEAR': '2013-14'})
pts_allowed_array = []
reb_allowed_array = []
fg3m_allowed_array = []
for opp_stats in all_opp_stats:
    pts_allowed_array.append(opp_stats['OPP_PTS'])
    reb_allowed_array.append(opp_stats['OPP_REB'])
    fg3m_allowed_array.append(opp_stats['OPP_FG3M'])
pts_allowed_array.sort()
reb_allowed_array.sort()
fg3m_allowed_array.sort()
print pts_allowed_array[9]
print pts_allowed_array[19]
print reb_allowed_array[9]
print reb_allowed_array[19]

all_players = db.basic_model.distinct("PLAYER_ID")

#----------------------------------------------------- global vs_top_10_positive
#----------------------------------------------------- global vs_top_10_negative
#-------------------------------------------------- global vs_bottom_10_positive
#-------------------------------------------------- global vs_bottom_10_negative    

vs_top_10_positive = {}
vs_top_10_negative = {}
vs_bottom_10_positive = {}
vs_bottom_10_negative = {}

vs_top_10_reb_positive = {}
vs_top_10_reb_negative = {}
vs_bottom_10_reb_positive = {}
vs_bottom_10_reb_negative = {}

vs_top_10_fg3m_positive = {}
vs_top_10_fg3m_negative = {}
vs_bottom_10_fg3m_positive = {}
vs_bottom_10_fg3m_negative = {}

q = Queue()
for player in all_players:
    q.put(player)

def worker():
    while True:
        player = q.get()
        vs_top_10 = 0
        vs_bottom_10 = 0
        vs_top_10_reb = 0
        vs_bottom_10_reb = 0
        vs_top_10_fg3m = 0
        vs_bottom_10_fg3m = 0
        game_logs = db.basic_model.find({"PLAYER_ID": player})
        game_count = game_logs.count()
        if game_count > 60: 
            for game in game_logs:
                opponent_pts_allowed = (game['OPP_FGM'] - game['OPP_FG3M']) * 2 + \
                    game['OPP_FG3M'] * 3 + game['OPP_FTM']
                
                # vs. top 10 defense
                if opponent_pts_allowed < pts_allowed_array[9]:
                    vs_top_10 += (game['GAME_PTS'] - game['AVG_PTS'])
                # vs. bottom 10 defense
                if opponent_pts_allowed > pts_allowed_array[19]:
                    vs_bottom_10 += (game['GAME_PTS'] - game['AVG_PTS'])

                # vs. top 10 in REB allowed
                if game['OPP_REB'] < reb_allowed_array[9]:
                    vs_top_10_reb += (game['GAME_PTS'] - game['AVG_PTS'])
                # vs. bottom 10 in REB allowed
                if game['OPP_REB'] > reb_allowed_array[19]:
                    vs_bottom_10_reb += (game['GAME_PTS'] - game['AVG_PTS'])

                # vs. top 10 in FG3M allowed
                if game['OPP_FG3M'] < fg3m_allowed_array[9]:
                    vs_top_10_fg3m += (game['GAME_PTS'] - game['AVG_PTS'])
                # vs. bottom 10 in REB allowed
                if game['OPP_FG3M'] > fg3m_allowed_array[19]:
                    vs_bottom_10_fg3m += (game['GAME_PTS'] - game['AVG_PTS'])

            if (vs_top_10 / game_count) > 0.5:
                vs_top_10_positive[game['PLAYER_NAME']] = vs_top_10 / game_count
            elif (vs_top_10 / game_count) < -0.3:
                vs_top_10_negative[game['PLAYER_NAME']] = vs_top_10 / game_count
            if (vs_bottom_10 / game_count) > 0.5:
                vs_bottom_10_positive[game['PLAYER_NAME']] = vs_bottom_10 / game_count
            elif (vs_bottom_10 / game_count) < -0.3:
                vs_bottom_10_negative[game['PLAYER_NAME']] = vs_bottom_10 / game_count

            if (vs_top_10_reb / game_count) > 0.5:
                vs_top_10_reb_positive[game['PLAYER_NAME']] = vs_top_10_reb / game_count
            elif (vs_top_10_reb / game_count) < -0.3:
                vs_top_10_reb_negative[game['PLAYER_NAME']] = vs_top_10_reb / game_count
            if (vs_bottom_10_reb / game_count) > 0.5:
                vs_bottom_10_reb_positive[game['PLAYER_NAME']] = vs_bottom_10_reb / game_count
            elif (vs_bottom_10_reb / game_count) < -0.3:
                vs_bottom_10_reb_negative[game['PLAYER_NAME']] = vs_bottom_10_reb / game_count

            if (vs_top_10_fg3m / game_count) > 0.5:
                vs_top_10_reb_positive[game['PLAYER_NAME']] = vs_top_10_fg3m / game_count
            elif (vs_top_10_fg3m / game_count) < -0.3:
                vs_top_10_reb_negative[game['PLAYER_NAME']] = vs_top_10_fg3m / game_count
            if (vs_bottom_10_fg3m / game_count) > 0.5:
                vs_bottom_10_fg3m_positive[game['PLAYER_NAME']] = vs_bottom_10_fg3m / game_count
            elif (vs_bottom_10_fg3m / game_count) < -0.3:
                vs_bottom_10_fg3m_negative[game['PLAYER_NAME']] = vs_bottom_10_fg3m / game_count
        q.task_done()


for t in range(8):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

q.join()




print "top 10 positive:\n=================="
pprint.pprint( vs_top_10_positive)
print "top 10 negative: \n================="
pprint.pprint(vs_top_10_negative)
print "bottom 10 positive: \n=============="
pprint.pprint(vs_bottom_10_positive)
print "bottom 10 negative: \n=============="
pprint.pprint(vs_bottom_10_negative)

print "top 10 FG3M positive:\n=================="
pprint.pprint( vs_top_10_fg3m_positive)
print "top 10 FG3M negative: \n================="
pprint.pprint(vs_top_10_fg3m_negative)
print "bottom 10 FG3M positive: \n=============="
pprint.pprint(vs_bottom_10_fg3m_positive)
print "bottom 10 FG3M negative: \n=============="
pprint.pprint(vs_bottom_10_fg3m_negative)

print "top 10 REB positive:\n=================="
pprint.pprint( vs_top_10_reb_positive)
print "top 10 REB negative: \n================="
pprint.pprint(vs_top_10_reb_negative)
print "bottom 10 REB positive: \n=============="
pprint.pprint(vs_bottom_10_reb_positive)
print "bottom 10 REB negative: \n=============="
pprint.pprint(vs_bottom_10_reb_negative)