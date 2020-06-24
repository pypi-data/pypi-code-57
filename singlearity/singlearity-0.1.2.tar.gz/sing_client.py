from __future__ import print_function
import sys
#sys.path.insert(1, '/Users/jsilver/baseball/pybaseball/api-client')
import os
import time
import singlearity as sing
import pdb
from singlearity.models.state import State
from singlearity.models.player import Player
from singlearity.models.team import Team
from singlearity.models.venue import Venue
from singlearity.models.atmosphere import Atmosphere 
from singlearity.models.matchup import Matchup
#from singlearity.models.pa_sim import PaSim

from singlearity.rest import ApiException
from pprint import pprint
import pandas as pd
pd.options.display.max_rows = 999

# Defining host is optional and default to http://localhost
configuration = sing.Configuration()
#configuration.host = "http://www.singlearity.ai"
#configuration.host = "http://www.singlearity.ai:5000"
#configuration.host = "https://beta3-api.singlearity.com"
configuration.host = os.environ.get('SINGLEARITY_API_SERVER')
configuration.api_key['SINGLEARITY_API_KEY'] = os.environ.get("SINGLEARITY_API_KEY", "")

# Enter a context with an instance of the API client
with sing.ApiClient(configuration) as api_client:

    # Create an instance of the API class
    sing = sing.APIsApi(api_client)
    

##########################
#Task: Let's try to sign a veteran RH 1B or DH to platoon against LHPs
##########################
def get_best_veteran():
    candidate_batters = (sing.get_players(position= ["1B", "DH"], 
                      bat_side = ["R"], age_min = 32)) #bug tofix active=False will crash the server
    pprint(candidate_batters)
    lefty_pitcher = sing.get_players(name="James Paxton")[0]   
    #candidate_pitchers = sing.get_players(position=["P"], active=True)[0:20]
    candidate_pitchers = [lefty_pitcher]
    atmosph = Atmosphere(sing.get_venues(stadium_name = "Tropicana")[0], 
             temperature = 70, home_team = sing.get_teams(name = "Rays")[0])
    matchups = []
    for p in candidate_pitchers:
        matchups.extend([Matchup(batter = m, pitcher = p, 
      atmosphere = atmosph, state=State()) for m in candidate_batters])
    results = pd.DataFrame(sing.get_pa_sim(matchups))
    print(results.sort_values(by=['woba_exp'], ascending = False))


def rank_woba():
    candidate_batters = sing.get_players(team_name="Rays", active = True)
    #pitcher = sing.get_players(name="Gerrit Cole" )[0]   #change to generic lhp
    candidate_pitchers = sing.get_players(team_name = "Yankees", active = True)   #change to generic lhp
    atmosph = Atmosphere(sing.get_venues(stadium_name = "Tropicana")[0],
            temperature = 70,
            home_team = sing.get_teams(name = "Rays")[0])
    for j in range(0,5):
        print("HERE")
        matchups = [Matchup(batter = m, pitcher = p, 
         atmosphere = atmosph, state=State()) for m in candidate_batters for p in candidate_pitchers[0:5]]
        print(len(matchups))
        results = pd.DataFrame(sing.get_pa_sim(matchups))
        print(results.sort_values(by=['woba_exp']))

    




get_best_veteran()
rank_woba()

player = sing.get_players(name="Mike Trout")
pprint(player)
team = sing.get_teams(name="Angels")
#pprint(team)

venue = sing.get_venues(stadium_name="Stadium")
#pprint(venue)
venue = sing.get_venues()
#pprint(venue)
venue = sing.get_venues(team_name="Angels")
#pprint(venue)
venue = sing.get_venues(team_name="Rays")
#pprint(venue)




