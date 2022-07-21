import os
import math
import matplotlib 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from scipy import stats
from sklearn import preprocessing
from urllib.request import urlopen
from soccerplots.radar_chart import Radar
from mplsoccer import PyPizza, add_image, FontManager
#%matplotlib inline

dataframe = pd.read_csv("Comparison.csv")


## CODE FOR RADAR VIZ

columns_to_keep = ['Session Title','Player Name', 'Distance Per Min', 'HSR Per Minute (Absolute)', 'Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute']

radar_df = dataframe[columns_to_keep]

##filter two players
df = radar_df[(radar_df['Player Name']=='Adam Verdon') | (radar_df['Player Name']=='Liam Kerrigan')]

##filter match day
df = df[(df['Session Title']=='M11 St Pats 2nd Leg MD-0')].reset_index()
df = df.drop(['index','Session Title'],axis=1)

#get parameters
params = list(df.columns)
params = params[1:]

a_values = []
b_values = []

for x in range(len(df['Player Name'])):
    if df['Player Name'][x] == 'Liam Kerrigan':
        a_values = df.iloc[x].values.tolist()
    if df['Player Name'][x] == 'Adam Verdon':
        b_values = df.iloc[x].values.tolist()
        
a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values,b_values]

##RANGE OF RADAR

range_radar=[]
radar_MM = radar_df.drop(['Session Title','Player Name'], axis=1 )
ra = radar_MM.min()
ra = ra.to_list()

rb = radar_MM.max()
rb = rb.to_list()

for x in range(6):
    range_radar.append((ra[x],rb[x]))

#title of radar chart

title = dict(
    title_name='Liam Kerrigan',
    title_color = 'red',
    subtitle_name = 'UCD AFC',
    subtitle_color = 'red',
    title_name_2='Adam Verdon',
    title_color_2 = 'blue',
    subtitle_name_2 = 'UCD AFC',
    subtitle_color_2 = 'blue',
    title_fontsize = 18,
    subtitle_fontsize=15
)

endnote = '@viz created by vida\ndata via STATSports Apex'


### PLOTTING RADAR CHART
radar = Radar(label_fontsize=12, range_fontsize=8)

fig,ax = radar.plot_radar(ranges=range_radar,params=params,values=values,
                         radar_color=['red','blue'],
                         alphas=[.6,.6],title=title,endnote=endnote,
                         compare=True)
#ax_image2 = add_image(
#    ucd_img, fig, left=0.34, bottom=0.12, width=0.13, height=0.127
#)   # these values might differ when you are plotting


## PIZZA CHART VIZ

font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))
						 
#player image and ucd logo
pl_img = Image.open("C:/Users/gaurs/Python/Capstone/Facepack/Liam Kerrigan.png")
ucd_img = Image.open("ucd_logo.png")

columns_pizza =['Session Title','Player Name','Distance Per Min', 'HSR Per Minute (Absolute)','Number Of High Intensity Bursts',
 'High Intensity Bursts Total Distance', 'High Intensity Bursts Maximum Speed',
 'Max Speed', 'Average Speed','Sprints','Max Acceleration','Max Deceleration',
 'HMLD Per Minute', 'HML Distance', 'HML Efforts Total Distance', 'HML Efforts','HML Efforts Maximum Speed']
 
pizza_df = dataframe[columns_pizza]

##select player for pizza viz
pizza_df_player = pizza_df[(pizza_df['Player Name']=='Liam Kerrigan')]

pizza_value_df=[]
pizza_value_df = pizza_df_player.drop(['Session Title','Player Name'], axis=1 )

pizza_values = pizza_value_df.mean()
#ra = ra.to_list()

np_array = np.array(pizza_values)
np_round = np.around(np_array, 2)

pizza_values = list(np_round)


params = [       
       'Distance Per Min', 'HSR Per Minute (Absolute)','Number Of High Intensity Bursts',
       'High Intensity Bursts Total Distance', 'High Intensity Bursts Maximum Speed',
       'Max Speed', 'Average Speed','Sprints','Max Acceleration','Max Deceleration',
       'HMLD Per Minute', 'HML Distance', 'HML Efforts Total Distance','HML Efforts','HML Efforts Maximum Speed' 
	   ]
	   
# calculating the percentile values with scipy stats. Since we have raw values

pvalues = []
for x in range(len(params)):   
    pvalues.append(math.floor(stats.percentileofscore(pizza_df[params[x]],pizza_values[x])))
	
	

# parameter list
params_new = [       
       'Distance p/Min', 'HSR p/Min','Number of HIB',
       'HIB Distance', 'HIB Max Speed',
       'Max Speed', 'Avg Speed','Number of Sprints','Max Accel','Max Decel',
       'HMLD p/Min', 'HML Distance', 'HML Efforts Distance','HML Efforts','HML Efforts Max Speed'     
]
# value list
# The percentile values calculated above
values = pvalues

# color for the slices and text
slice_colors = ["#1A78CF"] * 5 + ["#FF9300"] * 5 + ["#D70232"] * 5
text_colors = ["#000000"] * 10 + ["#F2F2F2"] * 5

# instantiate PyPizza class
baker = PyPizza(
    params=params_new,              # list of parameters
    background_color="#EBEBE9",     # background color
    straight_line_color="#EBEBE9",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=0,               # linewidth of last circle
    other_circle_lw=0,              # linewidth for other circles
    inner_circle_size=20            # size of inner circle
)

# plot pizza
fig, ax = baker.make_pizza(
    values,                          # list of values
    figsize=(8, 8.5),                # adjust figsize according to your need
    color_blank_space="same",        # use same color to fill blank space
    slice_colors=slice_colors,       # color for individual slices
    value_colors=text_colors,        # color for the value-text
    value_bck_colors=slice_colors,   # color for the blank spaces
    blank_alpha=0.4,                 # alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#F2F2F2", zorder=2, linewidth=1
    ),                               # values to be used when plotting slices
    kwargs_params=dict(
        color="#000000", fontsize=11,
        fontproperties=font_normal.prop, va="center"
    ),                               # values to be used when adding parameter
    kwargs_values=dict(
        color="#000000", fontsize=11,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                                # values to be used when adding parameter-values
)

# add title
fig.text(
    0.515, 0.975, "Liam Kerrigan - UCD AFC", size=16,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

# add subtitle
fig.text(
    0.515, 0.953,
    "Percentile Rank vs Squad | Season 2021-22",
    size=13,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

# add credits
CREDIT_1 = "data: STATSports Apex"
CREDIT_2 = "inspired by: @mckayjohns"

fig.text(
    0.99, 0.02, f"{CREDIT_1}\n{CREDIT_2}", size=9,
    fontproperties=font_italic.prop, color="#000000",
    ha="right"
)

# add text
fig.text(
    0.34, 0.925, "Intensity          Pace                   HML", size=14,
    fontproperties=font_bold.prop, color="#000000"
)

# add rectangles
fig.patches.extend([
    plt.Rectangle(
        (0.31, 0.9225), 0.025, 0.021, fill=True, color="#1a78cf",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.462, 0.9225), 0.025, 0.021, fill=True, color="#ff9300",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.632, 0.9225), 0.025, 0.021, fill=True, color="#d70232",
        transform=fig.transFigure, figure=fig
    ),
])

# add image
ax_image = add_image(
    pl_img, fig, left=0.4478, bottom=0.44, width=0.13, height=0.127
)

ax_image2 = add_image(
    ucd_img, fig, left=0.1, bottom=0.02, width=0.13, height=0.127
)

plt.show()