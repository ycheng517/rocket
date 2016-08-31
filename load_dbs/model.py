from nba_py import game
from pymongo import MongoClient

seasons = ['2013-14', '2014-15', '2015-16']

client = MongoClient("52.41.52.130", 27017)
db = client.nba_stats

games = db.game_summary.find()


for game in games:
    print game['GAME_ID']
    print ("SEASON YEAR STRING: %s" % (game['SEASON'] + '-' + str(int(game['SEASON'][2:]) + 1)))
    home_team_stats = db.team_stats.find_one({"TEAM_ID": int(game["HOME_TEAM_ID"]),
                                              })
    print "home_team_stats"
    print home_team_stats
    home_team_opp_stats = db.team_opponent_stats.find_one({"TEAM_ID": game["HOME_TEAM_ID"],
                                                           "SEASON_YEAR": game['SEASON'] + '-' + str(int(game['SEASON'][2:]) + 1)})
    print "home_team_opp_stats"
    print home_team_opp_stats
    visitor_team_stats = db.team_stats.find_one({"TEAM_ID": game["VISITOR_TEAM_ID"],
                                                 "SEASON_YEAR": game['SEASON'] + '-' + str(int(game['SEASON'][2:]) + 1)})
    print "visitor_team_stats"
    print visitor_team_stats
    visitor_team_opp_stats = db.team_opponent_stats.find_one({"TEAM_ID": game["VISITOR_TEAM_ID"],
                                                              "SEASON_YEAR": game['SEASON'] + '-' + str(int(game['SEASON'][2:]) + 1)})
    print "visitor_team_opp_stats"
    print visitor_team_opp_stats
    
    #get all players who played in the game:
    active_players = db.game_logs.find({'GAME_ID': game['GAME_ID']})

    for player in active_players:
        # get average stats
        avg_stats = db.player_avg_stats.find_one({'PLAYER_ID': player['PLAYER_ID'],
                                              'SEASON_ID': player['SEASON_ID']})
        if player['MIN'] > 15:
            sample = {}
            output = player['PTS']
            sample['PLAYER_ID'] = player['PLAYER_ID']
            sample['SEASON_ID'] = player['SEASON_ID']
            sample['PLAYER_NAME'] = player['PLAYER_NAME']
            sample['AGE'] = avg_stats['AGE']
            sample['GAME_ID'] = game['GAME_ID']
            sample['AVG_MIN'] = avg_stats['MIN']
            sample['AVG_FGA'] = avg_stats['FGA']
            sample['AVG_FGM'] = avg_stats['FGM']
            sample['AVG_FTA'] = avg_stats['FTA']
            sample['AVG_FTM'] = avg_stats['FTM']
            sample['AVG_FG3A'] = avg_stats['FG3A']
            sample['AVG_FG3M'] = avg_stats['FG3M']
            sample['AVG_REB'] = avg_stats['REB']
            sample['AVG_DREB'] = avg_stats['DREB']
            sample['AVG_AST'] = avg_stats['AST']
            sample['AVG_STL'] = avg_stats['STL']
            sample['AVG_BLK'] = avg_stats['BLK']
            sample['AVG_BLKA'] = avg_stats['BLKA']
            sample['AVG_PF'] = avg_stats['PF']
            sample['AVG_PFD'] = avg_stats['PFD']
            sample['AVG_TOV'] = avg_stats['TOV']
            print type(player['TEAM_ID'])
            print type(game['HOME_TEAM_ID'])
            if player['TEAM_ID'] == str(game['HOME_TEAM_ID']):
                print "this is being called"
                # team stats
                sample['TEAM_W_PCT'] = home_team_stats['W_PCT']
                sample['TEAM_PLUS_MINUS'] = home_team_stats['PLUS_MINUS']
                sample['TEAM_FGA'] = home_team_stats['FGA']
                sample['TEAM_FGM'] = home_team_stats['FGM']
                sample['TEAM_FG3A'] = home_team_stats['FG3A']
                sample['TEAM_FG3M'] = home_team_stats['FG3M']
                sample['TEAM_FTA'] = home_team_stats['FTA']
                sample['TEAM_FTM'] = home_team_stats['FTM']
                sample['TEAM_REB'] = home_team_stats['REB']
                sample['TEAM_DREB'] = home_team_stats['DREB']
                sample['TEAM_AST'] = home_team_stats['AST']
                sample['TEAM_STL'] = home_team_stats['STL']
                sample['TEAM_BLK'] = home_team_stats['BLK']
                sample['TEAM_BLKA'] = home_team_stats['BLKA']
                sample['TEAM_TOV'] = home_team_stats['TOV']
                sample['TEAM_PF'] = home_team_stats['PF']
                sample['TEAM_PFD'] = home_team_stats['PFD']

                # opponent stats allowed
                sample['OPP_W_PCT'] = visitor_team_opp_stats['W_PCT']
                sample['OPP_PLUS_MINUS'] = visitor_team_opp_stats['PLUS_MINUS']
                sample['OPP_FGA'] = visitor_team_opp_stats['OPP_FGA']
                sample['OPP_FGM'] = visitor_team_opp_stats['OPP_FGM']
                sample['OPP_FG3A'] = visitor_team_opp_stats['OPP_FG3A']
                sample['OPP_FG3M'] = visitor_team_opp_stats['OPP_FG3M']
                sample['OPP_FTA'] = visitor_team_opp_stats['OPP_FTA']
                sample['OPP_FTM'] = visitor_team_opp_stats['OPP_FTM']
                sample['OPP_REB'] = visitor_team_opp_stats['OPP_REB']
                sample['OPP_DREB'] = visitor_team_opp_stats['OPP_DREB']
                sample['OPP_AST'] = visitor_team_opp_stats['OPP_AST']
                sample['OPP_STL'] = visitor_team_opp_stats['OPP_STL']
                sample['OPP_BLK'] = visitor_team_opp_stats['OPP_BLK']
                sample['OPP_BLKA'] = visitor_team_opp_stats['OPP_BLKA']
                sample['OPP_TOV'] = visitor_team_opp_stats['OPP_TOV']
                sample['OPP_PF'] = visitor_team_opp_stats['OPP_PF']
                sample['OPP_PFD'] = visitor_team_opp_stats['OPP_PFD']
                                
            elif player['TEAM_ID'] == str(game['VISITOR_TEAM_ID']):
                sample['TEAM_W_PCT'] = visitor_team_stats['W_PCT']
                sample['TEAM_PLUS_MINUS'] = visitor_team_stats['PLUS_MINUS']
                sample['TEAM_FGA'] = visitor_team_stats['FGA']
                sample['TEAM_FGM'] = visitor_team_stats['FGM']
                sample['TEAM_FG3A'] = visitor_team_stats['FG3A']
                sample['TEAM_FG3M'] = visitor_team_stats['FG3M']
                sample['TEAM_FTA'] = visitor_team_stats['FTA']
                sample['TEAM_FTM'] = visitor_team_stats['FTM']
                sample['TEAM_REB'] = visitor_team_stats['REB']
                sample['TEAM_DREB'] = visitor_team_stats['DREB']
                sample['TEAM_AST'] = visitor_team_stats['AST']
                sample['TEAM_STL'] = visitor_team_stats['STL']
                sample['TEAM_BLK'] = visitor_team_stats['BLK']
                sample['TEAM_BLKA'] = visitor_team_stats['BLKA']
                sample['TEAM_TOV'] = visitor_team_stats['TOV']
                sample['TEAM_PF'] = visitor_team_stats['PF']
                sample['TEAM_PFD'] = visitor_team_stats['PFD']

                # opponent stats allowed
                sample['OPP_W_PCT'] = home_team_opp_stats['W_PCT']
                sample['OPP_PLUS_MINUS'] = home_team_opp_stats['PLUS_MINUS']
                sample['OPP_FGA'] = home_team_opp_stats['OPP_FGA']
                sample['OPP_FGM'] = home_team_opp_stats['OPP_FGM']
                sample['OPP_FG3A'] = home_team_opp_stats['OPP_FG3A']
                sample['OPP_FG3M'] = home_team_opp_stats['OPP_FG3M']
                sample['OPP_FTA'] = home_team_opp_stats['OPP_FTA']
                sample['OPP_FTM'] = home_team_opp_stats['OPP_FTM']
                sample['OPP_REB'] = home_team_opp_stats['OPP_REB']
                sample['OPP_DREB'] = home_team_opp_stats['OPP_DREB']
                sample['OPP_AST'] = home_team_opp_stats['OPP_AST']
                sample['OPP_STL'] = home_team_opp_stats['OPP_STL']
                sample['OPP_BLK'] = home_team_opp_stats['OPP_BLK']
                sample['OPP_BLKA'] = home_team_opp_stats['OPP_BLKA']
                sample['OPP_TOV'] = home_team_opp_stats['OPP_TOV']
                sample['OPP_PF'] = home_team_opp_stats['OPP_PF']
                sample['OPP_PFD'] = home_team_opp_stats['OPP_PFD']
            print(sample)
            break

    # get scoring averages for all players who played in the game
    
    
    # calculate the top 8 players in minutes played
    #------------------------------------------- for home_log in home_game_logs:
        #--------------------------------------------------- del home_log['_id']
        #----------------------------------- db.basic_model.insert_one(home_log)
        #-------- db.basic_model.update_one(home_log, {"$set": home_team_stats})
        #- db.basic_model.update_one(home_log, {"$set": visitor_team_opp_stats})
    #------------------------------------- for visitor_log in visitor_game_logs:
        #------------------------------------------------ del visitor_log['_id']
        #-------------------------------- db.basic_model.insert_one(visitor_log)
        #-- db.basic_model.update_one(visitor_log, {"$set": visitor_team_stats})
        #- db.basic_model.update_one(visitor_log, {"$set": home_team_opp_stats})
