import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import seaborn as sns
import os


totalRealPoints = 0
totalNewPoints = 0
for playerdata in os.listdir('data/2014-15'):

  print(f"Player: {playerdata}")

  filename = 'data/2014-15/' + playerdata
  #data = json.load(open('data/2014-15/CurryStephen.json'))
  data = json.load(open(filename))

  # Make a list of dicts for the shot data from list of dicts in resultsSets
  dataList = [l for l in data["resultSets"] if l["name"] == "Shot_Chart_Detail"]

  if (len(dataList) != 1):
    print(f"Warning! {len(dataList)} data sets found!")

  dataDF = pd.DataFrame(dataList[0]["rowSet"], columns = dataList[0]["headers"])

  # Create a column to correspond to a real point value
  dataDF['REAL_POINTS'] = [3 if x == '3PT Field Goal' else (2 if x == '2PT Field Goal' else -1) for x in dataDF['SHOT_TYPE']]

  # Calculate a new column, which is the new point value
  #dataDF['NEW_POINTS'] = [ 1 + (1.0/x) if x != 0 else 1 for x in dataDF['SHOT_DISTANCE']]
  dataDF['NEW_POINTS'] = [ 1 + x for x in dataDF['SHOT_DISTANCE']]

#myplot = dataDF.plot(x='LOC_X', y='LOC_Y', kind = 'hexbin', figsize = [10,6],
#  title='Steph Curry Shots', colormap='viridis', gridsize=100)
#colors = dataDF['SHOT_MADE_FLAG'].map({0:'r',1:'b'})
#myplot = dataDF.plot(x='LOC_X', y='LOC_Y', kind = 'scatter', figsize = [10,6],
#  title='Steph Curry Shots', colormap='viridis',c=colors)
# myplot = sns.scatterplot(x='LOC_X',y='LOC_Y',data=dataDF,hue='SHOT_MADE_FLAG')

  # Create a column to confirm I understand shot distance column
#dataDF['CALC_SHOT_DISTANCE'] = [sqrt( x*x + (y-40)(y-40) ) for (x,y) in (dataDF['LOC_X'],dataDF['LOC_Y'])]
  dataDF['CALC_SHOT_DISTANCE'] = np.sqrt( dataDF['LOC_X']*dataDF['LOC_X'] + (dataDF['LOC_Y'])*(dataDF['LOC_Y']) )


#checkDistance = dataDF.plot(x='SHOT_DISTANCE',y='CALC_SHOT_DISTANCE',kind='scatter')
#checkLocY = dataDF.plot(x='LOC_X',y='LOC_Y',kind='scatter')
#plt.show()

  # Calculate the total number of points scored by the player during this season
  madeDF = dataDF[ dataDF['SHOT_MADE_FLAG'] == 1]
  playerRealPoints = madeDF['REAL_POINTS'].sum()
  print(f"Player scored {totalRealPoints} points in this season")
  totalRealPoints = totalRealPoints + playerRealPoints

  playerNewPoints = madeDF['NEW_POINTS'].sum()
  print(f"Player scored {totalNewPoints} new points in this season")
  totalNewPoints = totalNewPoints + playerNewPoints


# Normalize the new points to the old points
normFactor = totalRealPoints / totalNewPoints
print(f"{totalRealPoints} real points scored off of field goals")
print(f"{totalNewPoints} new points scored off of field goals")
print(f"Normalization factor is {normFactor}")
# dataDF['NEW_POINTS'] = normFactor * dataDF['NEW_POINTS']
# madeDF = dataDF[ dataDF['SHOT_MADE_FLAG'] == 1]
# totalRealPoints = madeDF['REAL_POINTS'].sum()
# print(f"Player scored {totalRealPoints} points in this season")

# totalNewPoints = madeDF['NEW_POINTS'].sum()
# print(f"Player scored {totalNewPoints} (normalized) new points in this season")



