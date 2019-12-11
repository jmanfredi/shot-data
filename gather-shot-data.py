import requests
import json
import time
import os.path

# Define the URL to get all the player IDs
players_url = 'https://stats.nba.com/js/data/ptsd/stats_ptsd.js'
#headers = requests.utils.default_headers()
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
#headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'})
#headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'})
#headers.update({'Accept-Encoding': 'gzip, deflate, br'})

headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive',
  'Host': 'stats.nba.com',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

#print(headers)

# Hard code for now
year = '2014-15'
b_overwrite = False

players_response = requests.get(players_url, headers = headers, timeout = 5)
players_resp_text = players_response.text

players_json_str = players_resp_text[ 
  players_resp_text.find('{') : players_resp_text.rfind('}')+1
  ]

# Make a list of player IDs
# Structure of each entry is: ID, Name, Active (1/0), Rookie year, last year played, ?, ?
players_dict = json.loads(players_json_str)["data"]["players"]
players_year_start = [player[3] for player in players_dict]
players_year_end = [player[4] for player in players_dict]
player_ids = [player[0] for player in players_dict if player[3] <= 2014 and player[4] >= 2015]
player_names = [player[1] for player in players_dict if player[3] <= 2014 and player[4] >= 2015]
player_ids_names = [(player[0],player[1]) for player in players_dict if player[3] <= 2014 and player[4] >= 2015]

#print(player_ids)

# Define the URL format for player shot data
url_1 = 'https://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS='
url_2 = '&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&PlayerPosition=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID='
url_3 = '&PlusMinus=N&Position=&Rank=N&RookieYear=&Season='
url_4 = '&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0'

#'https://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=2014-15&ContextFilter='
#'&ContextMeasure=FGA&DateFrom=&DateTo=&PlayerPosition=&GameID=&GameSegment=&LastNGames=0'
#'&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust='
#'N&PerMode=PerGame&Period=0&PlayerID=2544&PlusMinus=N&Position=&Rank=N&RookieYear=&'
#'Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision'
#'=&mode=Advanced&showDetails=0&showShots=1&showZones=0'

directory_name = 'data/'+year

if not os.path.exists(directory_name):
    print(f"Making directory for {year}")
    os.makedirs(directory_name)

nTimeout = 0
nConnect = 0
nSuccess = 0

prog_count = 0
num_players = len(player_ids)
print(f"Found {num_players} players for {year}")
for id, name in player_ids_names:
  if (prog_count % 50 == 0):
    print(f'Data loaded from {prog_count} out of {num_players} players')

  print(id)
  print(name)
  #id = 2544
  full_url = url_1 + str(year) + url_2 + str(id) + url_3 + str(year) + url_4
  #print(full_url)
  
  try:
    shots = requests.get(full_url, headers = headers, timeout=5).json()
    
    #Open player file
    trimmed_name = name.translate({ord(c): None for c in ',. !@#$-'})
    file_name = 'data/'+year+'/'+trimmed_name + '.json'
    #print(filename)

    if os.path.exists(file_name):
      if b_overwrite:
        print(f"Deleting existing file {file_name}")
        os.remove(file_name)
      else:
        print("Error! Trying to write data to existing file, quitting now")
        print("If you want to overwrite the data, set b_overwrite to true")
        exit()

    with open(file_name,'w') as outfile:
      json.dump(shots,outfile)


  except requests.ConnectionError:
    print(f"Can't connect to site for {name}")
    nConnect += 1
  except requests.Timeout:
    print(f"Timeout! For {name}")
    nTimeout += 1
  else:
    nSuccess += 1
  prog_count = prog_count + 1


print(f'We had {nSuccess} successes')
print(f'We had {nTimeout} timeouts')
print(f'We had {nConnect} connection errors')












