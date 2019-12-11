import pandas as pd
import numpy as np
import json
import os
import sys


totalRealPoints = 0
totalNewPoints = 0
totalShotsMade = 0
totalShotDistance = 0

# Rows list will hold player data dictionaries which will then be put into
# a dictionary
rows = []

season = '2018-19'
directory = 'data/' + season

for playerdata in os.listdir(directory):

  playerDict = {}

  print(f"Player: {playerdata}")
  playerDict["NAME"] = playerdata.replace(".json","")

  filename = directory + '/' + playerdata
  data = json.load(open(filename))

  # Make a list of dicts for the shot data from list of dicts in resultsSets
  dataList = [l for l in data["resultSets"] if l["name"] == "Shot_Chart_Detail"]

  if (len(dataList) != 1):
    print(f"Warning! {len(dataList)} data sets found!")

  dataDF = pd.DataFrame(dataList[0]["rowSet"], columns = dataList[0]["headers"])

  # Create a column to correspond to a real point value
  dataDF['REAL_POINTS'] = [3 if x == '3PT Field Goal' else (2 if x == '2PT Field Goal' else -1) for x in dataDF['SHOT_TYPE']]

 # Create a column to confirm I understand shot distance column
  dataDF['CALC_SHOT_DISTANCE'] = np.sqrt( dataDF['LOC_X']*dataDF['LOC_X'] + 
    (dataDF['LOC_Y'])*(dataDF['LOC_Y']) )

  factor = 0.04210526 # set min value to 2, and have 3 at 23.75 ft
  # Calculate new points
  dataDF['NEW_POINTS'] = [ 2 + factor*x for x in dataDF['SHOT_DISTANCE']]

  
  playerShotCount = dataDF['SHOT_ATTEMPTED_FLAG'].sum()

  # Calculate the total number of points scored by the player during this season
  madeDF = dataDF[ dataDF['SHOT_MADE_FLAG'] == 1]

# Check for close range shots with shot distance
  # If not close range, check to see if it's still a two point shot
  # Everything else is a three
  #dataDF['RANGE'] = [1 if x < 10 else (2 if y == 2 else 3) for x,y in (dataDF['SHOT_DISTANCE'],dataDF['REAL_POINTS']) ]
  madeDF['RANGE'] = [1 if x < 100 else (2 if y == 2 else 3) for x,y in zip(madeDF['CALC_SHOT_DISTANCE'],madeDF['REAL_POINTS']) ]
  #madeDF['RANGE'] = [2 if y == 2 else 3 for y in madeDF['REAL_POINTS'] ]
  #madeDF['RANGE'] = [1 if x < 10 for x in madeDF['SHOT_DISTANCE'] ]


  playerRealPoints = madeDF['REAL_POINTS'].sum()
  playerShotsMade = madeDF['SHOT_MADE_FLAG'].sum()
  #playerShotDistance = madeDF['SHOT_DISTANCE'].sum()
  playerShotDistance = madeDF['CALC_SHOT_DISTANCE'].sum()
  if playerShotCount > 0:
    playerAvgShotDistance = playerShotDistance / playerShotCount
  else:
    playerAvgShotDistance = 0
  print(f"Player scored {playerRealPoints} points in this season")
  totalRealPoints = totalRealPoints + playerRealPoints
  totalShotsMade = totalShotsMade + playerShotsMade
  totalShotDistance = totalShotDistance + playerShotDistance

  playerNewPoints = madeDF['NEW_POINTS'].sum()
  print(f"Player scored {playerNewPoints} new points in this season")
  totalNewPoints = totalNewPoints + playerNewPoints

  #Add to new dataframe that stores new values
  playerDict["REAL_POINTS"] = playerRealPoints
  playerDict["NEW_POINTS"] = playerNewPoints
  playerDict["AVG_SHOT_DIST"] = playerAvgShotDistance
  playerDict["SHOT_COUNT"] = playerShotCount
  playerDict["REAL_POINTS_PER_SHOT"] = playerRealPoints / playerShotCount
  playerDict["NEW_POINTS_PER_SHOT"] = playerNewPoints / playerShotCount  
  playerDict["POINT_GAIN"] = playerNewPoints - playerRealPoints
  if playerRealPoints > 0:
    playerDict["POINT_GAIN_FRAC"] = playerNewPoints / playerRealPoints
  else:
    playerDict["POINT_GAIN_FRAC"] = 0

  #Calculate percentage of shots from each range category
  playerShort = 100*madeDF[ madeDF['RANGE'] == 1 ]['RANGE'].sum() / playerShotCount
  playerMid   = 100*madeDF[ madeDF['RANGE'] == 2 ]['RANGE'].sum() / playerShotCount
  playerLong  = 100*madeDF[ madeDF['RANGE'] == 3 ]['RANGE'].sum() / playerShotCount

  playerDict["SHORT_PERC"] = playerShort
  playerDict["MID_PERC"]   = playerMid
  playerDict["LONG_PERC"]  = playerLong

  rows.append(playerDict)

# Calculate the average number of real points and new points
avgReal = np.mean( [ d["REAL_POINTS"] for d in rows ] )
print(f"Average real points scored: {avgReal}")
avgNew = np.mean( [ d["NEW_POINTS"] for d in rows ] )
print(f"Average new points scored: {avgNew}")

# Get new column to account for change vs average
for playerDict in rows:
  playerDict["REAL_DIFF_AVG"] = 100 * ( playerDict["REAL_POINTS"] - avgReal ) / avgReal
  playerDict["NEW_DIFF_AVG"] = 100 * ( playerDict["NEW_POINTS"] - avgNew ) / avgNew
  playerDict["DIFF_AVG_CHANGE"] = playerDict["NEW_DIFF_AVG"] - playerDict["REAL_DIFF_AVG"]

# Normalize the new points to the old points
normFactor = ( totalRealPoints - 2*totalShotsMade ) / totalShotDistance
print(f"{totalRealPoints} real points scored off of field goals")
print(f"{totalNewPoints} new points scored off of field goals")
print(f"Normalization factor is {normFactor}")

# Instantiate DataFrame
playerDF = pd.DataFrame(rows)
playerDF = playerDF.set_index('NAME')
print(playerDF.head())
outfilename = season + '-player-data.csv'
playerDF.to_csv(outfilename)








