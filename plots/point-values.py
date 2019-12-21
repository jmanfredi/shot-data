import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import json
import seaborn as sns
import os
from plotTools import draw_court

data = json.load(open('../data/2018-19/DeRozanDeMar.json'))

# Make a list of dicts for the shot data from list of dicts in resultsSets
dataList = [l for l in data["resultSets"] if l["name"] == "Shot_Chart_Detail"]

if (len(dataList) != 1):
  print(f"Warning! {len(dataList)} data sets found!")

dataDF = pd.DataFrame(dataList[0]["rowSet"], columns = dataList[0]["headers"])
dataDF = dataDF[ dataDF['LOC_Y'] < 420 ]

# Create a column to correspond to a real point value
dataDF['REAL_POINTS'] = [3 if x == '3PT Field Goal' else (2 if x == '2PT Field Goal' else -1) for x in dataDF['SHOT_TYPE']]
factor = 0.04210526 # set min value to 2, and have 3 at 23.75 ft
dataDF['NEW_POINTS'] = [ 2 + factor*x for x in dataDF['SHOT_DISTANCE']]

dataDF['CALC_SHOT_DISTANCE'] = np.sqrt( dataDF['LOC_X']*dataDF['LOC_X'] + (dataDF['LOC_Y'])*(dataDF['LOC_Y']) )

fig, axes = plt.subplots(1,2,figsize=(8,4))
#axes[0].axis('off')
axes[0].set_yticklabels([])
axes[0].set_xticklabels([])
axes[0].set_xticks([])
axes[0].set_yticks([])
axes[1].axis('off')
fig.suptitle("DeMar DeRozan point values (2018-19)")

minpt = 2
maxpt = max(3,dataDF['NEW_POINTS'].max())
print(f"Minimum is {minpt} and maximum is {maxpt}")

real = axes[0].scatter(
  dataDF['LOC_X'],dataDF['LOC_Y'],
  c=dataDF['REAL_POINTS'],cmap='hot',zorder = 1,
  marker='o',edgecolors='0.5',vmax=maxpt)
draw_court(ax=axes[0],lw=1,outer_lines='True')
axes[0].set_ylim([-50,450])
axes[0].axis('off')
axes[0].text(102,375,'Real NBA',fontsize=14,style='italic')

plt.sca(axes[1])# change the active set of axes
new = axes[1].scatter(
   dataDF['LOC_X'],dataDF['LOC_Y'],c=dataDF['NEW_POINTS'],cmap="hot",
   zorder = 1,marker='o',edgecolors='0.5')
draw_court(ax=axes[1],lw=1,outer_lines='True')
axes[1].set_ylim([-50,450])
axes[1].axis('off')
axes[1].text(72,375,'Bizarro NBA',fontsize=14,style='italic')

plt.tight_layout()

fig.colorbar(new, ax = axes, orientation = 'horizontal', fraction = 0.1, shrink = 1.0,
  aspect = 40,use_gridspec=True,pad=0.01)

plt.savefig('derozan.png')


plt.show()
