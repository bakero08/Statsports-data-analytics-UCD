import glob
import os
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math, time
import base64
from statsbombpy import sb
from PIL import Image
from fpdf import FPDF
from mplsoccer import PyPizza, add_image, FontManager
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from tempfile import NamedTemporaryFile
from soccerplots.radar_chart import Radar
from PIL import Image
from scipy import stats
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
#from urllib.request import urlopen



def app():

        
        image = Image.open('Player_img.jpg')
        
        col1, col2 = st.columns(2)
        
        col1.title(" Players Comparison Analysis ")     
        col2.image(image)
        
        dataframe = pd.read_csv("Comparison.csv")
        
        ##RADAR CHART
        
        columns_to_keep = ['Session Title','Player Name', 'Distance Per Min', 'HSR Per Minute (Absolute)', 'Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute']
        radar_df = dataframe[columns_to_keep]
        
        players_list = radar_df['Player Name'].sort_values(ascending=True)
        players_list = players_list.unique()
        session_list = radar_df['Session Title'].sort_values(ascending=True)
        session_list = session_list.unique()

        def radarChart(p1,p2):
        
            df = radar_df[(radar_df['Player Name']==p1) | (radar_df['Player Name']==p2)]
            df = df[(df['Session Title']==session)].reset_index()
            df = df.drop(['index','Session Title'],axis=1)
            
            if p1==p2:
                st.error("Identical players selected! Please select two different players for comparison")
                
            elif len(df) <2: 
                st.error("One or both players didn't play the match! Please select different player or different session")    
            else:
            
                #get parameters
                params = list(df.columns)
                params = params[1:]
                a_values = []
                b_values = []
                
                for x in range(len(df['Player Name'])):
                    if df['Player Name'][x] == p1:
                        a_values = df.iloc[x].values.tolist()
                    if df['Player Name'][x] == p2:
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
                    title_name=p1,
                    title_color = 'red',
                    subtitle_name = 'UCD AFC',
                    subtitle_color = 'red',
                    title_name_2=p2,
                    title_color_2 = 'blue',
                    subtitle_name_2 = 'UCD AFC',
                    subtitle_color_2 = 'blue',
                    title_fontsize = 15,
                    subtitle_fontsize=10
                )
                
                endnote = '@viz created by vida\ndata via STATSports Apex'
                
                ### PLOTTING RADAR CHART
                radar = Radar(label_fontsize=12, range_fontsize=8)
                
                fig,ax = radar.plot_radar(ranges=range_radar,params=params,values=values,
                                        radar_color=['red','blue'],
                                        alphas=[.6,.6],title=title,endnote=endnote,
                                        compare=True)
                plt.title("Radar Chart  ", fontsize=20, fontfamily='serif', color = 'Green')
                
                col3,col4 = st.columns(2)
                col3.pyplot(fig) 
                col4.markdown('  \n  \n  \n  \n')
                #col4.plotly_chart(plot, use_container_width=True, sharing="streamlit")  
                df_T = df
                df_T = df_T.set_index('Player Name')
                df_T  = df_T.transpose()
                col4.dataframe(df_T)                
                
        def comboChartCom(p1,s1):
        
            columns_com = ['Session Title','Player Name','Sprints', 'HML Efforts Maximum Speed','Accelerations','Max Deceleration' ,'High Intensity Bursts Maximum Speed','Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute']
            combo_df_p = dataframe[columns_com]
            
            combo_df_p = combo_df_p[(combo_df_p['Session Title']==s1)]
            
            combo_df_pl1 = combo_df_p[(combo_df_p['Player Name']==p1)]
            
            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=combo_df_pl1['Session Title'],
                    y=combo_df_pl1['Sprints'],
                    name="Number of Sprints",
                    text = combo_df_pl1['Sprints'],
                    textposition='outside',
                    textfont=dict(
                    size=13)       
                ))
            
            fig.add_trace(
                go.Bar(
                    x=combo_df_pl1['Session Title'],
                    y=combo_df_pl1['Max Speed'],
                    name="Max Speed",
                    text = combo_df_pl1['Max Speed'],
                    textposition='outside',
                    textfont=dict(
                    size=13)
                ))
            
            fig.add_trace(
                go.Bar(
                    x=combo_df_pl1['Session Title'],
                    y=combo_df_pl1['Max Acceleration'],
                    name="Max Accel",
                    text = combo_df_pl1['Max Acceleration'],
                    textposition='outside',
                    textfont=dict(
                    size=13)
                ))
            
            fig.add_trace(
                go.Bar(
                    x=combo_df_pl1['Session Title'],
                    y=combo_df_pl1['Max Deceleration'],
                    name="Max Decel",
                    text = combo_df_pl1['Max Deceleration'],
                    textposition='outside',
                    textfont=dict(
                    size=13)
                ))
            
            fig.add_trace(
                go.Bar(
                    x=combo_df_pl1['Session Title'],
                    y=combo_df_pl1['High Intensity Bursts Maximum Speed'],
                    name="HIB Max Speed",
                    text = combo_df_pl1['High Intensity Bursts Maximum Speed'],
                    textposition='outside',
                    textfont=dict(
                    size=13)
                ))
            fig.add_trace(
                go.Bar(
                    x=combo_df_pl1['Session Title'],
                    y=combo_df_pl1['HML Efforts Maximum Speed'],
                    name="HML Efforts Max Speed",
                    text = combo_df_pl1['HML Efforts Maximum Speed'],
                    textposition='outside',
                    textfont=dict(
                    size=13)
                ))
            #fig.update_traces(texttemplate='%{text:.2s}')
            fig.update_layout(
                            title_font_family="Times New Roman",
                            title_font_size = 20,
                            title_font_color="darkblue",
                            title_x=0.5,
                            legend_title_text='Stats',
                            plot_bgcolor="rgb(240,240,240)",
                            title_text=f'{p1} Pace Stats',
                            height=550)
                            #width = 700)
            
            return fig
        
        def scatterPlot():
            columns_to_keep_scat = ['Player Name', 'Distance Per Min', 'HSR Per Minute (Absolute)','Average Speed', 'Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute']
            scatter_df = dataframe[columns_to_keep_scat]
            
            scatter_df = scatter_df.groupby('Player Name').mean()
            scatter_df = scatter_df.reset_index(0)
            #scatter_df
        
            position = ['MID', 'ATT', 'DEF','ATT', 'MID', 'DEF','ATT', 'MID','MID', 'DEF','ATT', 'MID', 'DEF','ATT', 'MID', 'DEF','ATT', 'MID', 'DEF','DEF']
            scatter_df['position'] = position
            scatter_df = round(scatter_df,2)
            
            plot = px.scatter(scatter_df, x='Total Distance', y='HMLD Per Minute', color='position', size='Distance Per Min', symbol='position', hover_data = ['Player Name'])
            plot.update_layout(
                            title_font_family="Times New Roman",
                            title_font_size = 20,
                            title_font_color="darkblue",
                            title_x=0.5,
                            plot_bgcolor="rgb(240,240,240)",
                            title_text='Position-wise over the season Distance stat',
                            height=550)
            return plot    

        
        with st.sidebar:
            st.title('Players Performance Analysis')
            st.sidebar.markdown('''##### Compare two player's performance over the season''')
            player1 = st.selectbox("Select Player 1",players_list, index = 0)
            player2 = st.selectbox("Select Player 2",players_list, index = 1)
            session = st.selectbox("Select Session",session_list, index = 0)
            
            st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color: #ffffff;
                
            }
            div.stButton > button:hover {
                background-color: #ffffff;
                color:ff0000;
                }
            </style>""", unsafe_allow_html=True)
                       
            submitButton = st.button("Compare")
            
            st.subheader('Key Metrics')
            st.sidebar.markdown("""
            | Metric | Description |
            | --- | ---- |
            | Distance Per Min | Distance covered per min |
            | HMLD Per Minute |High Metabolic Load |
            | Max Speed |Maximum speed attained during the game|
            | HSR Per Min | describe this |
            | Total Distance |Distance covered during the session |
            | Max Acceleration |Maximum acceleration attained during the game |
            """
            )
        scatterP = scatterPlot()
        st.plotly_chart(scatterP, use_container_width=True)
            
            
        if submitButton:
            radarChart(player1,player2)
            comboChartP1 = comboChartCom(player1,session)
            comboChartP2 =comboChartCom(player2,session)
            col5,col6 = st.columns(2)
            col5.plotly_chart(comboChartP1, use_container_width=True)
            col6.plotly_chart(comboChartP2, use_container_width=True)
            
            