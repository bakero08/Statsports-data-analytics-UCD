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
        
        st.info('The Application is under development, hence only limited functionalities are available!')
        col1, col2 = st.columns((2,1))
        
        col1.title("Player Season Performance")
        #col2.image(image)
        
        dataframe = pd.read_csv("Comparison.csv")
        dataframe['Session Date']= pd.to_datetime(dataframe['Session Date'])
        match_dates = dataframe['Session Date'].dt.date
        match_dates = match_dates.unique()
        match_dates = np.sort(match_dates, axis=None)
        
            
        def comboChart(p1):
            
            columns_com = ['Session Title','Player Name','Sprints', 'Distance Per Min','Accelerations','Max Deceleration' ,'HSR Per Minute (Absolute)', 'Average Speed','Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute']
            combo_df = dataframe[columns_com]

            combo_df = combo_df[(combo_df['Player Name']==p1)]

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=combo_df['Session Title'],
                    y=combo_df['Max Acceleration'],
                    name="Max Accel"
                ))
            
            fig.add_trace(
                go.Scatter(
                    x=combo_df['Session Title'],
                    y=combo_df['Max Speed'],
                    name="Max Speed"
                ))
            
            fig.add_trace(
                go.Scatter(
                    x=combo_df['Session Title'],
                    y=combo_df['Max Deceleration'],
                    name="Max Decel"
                ))
            fig.add_trace(
                go.Bar(
                    x=combo_df['Session Title'],
                    y=combo_df['Sprints'],
                    name="Number of Sprints",
                    text = combo_df['Sprints'],
                    textposition='outside',
                    textfont=dict(
                    size=13,
                    color='black'),
                    #marker_color=combo_df['Sprints'],
                    marker_color='#ce93d8', 
                    marker_line_color='#4a148c',
                    marker_line_width=2, 
                    opacity=0.7
                ))
            fig.update_traces(texttemplate='%{text:.2s}')
            fig.update_layout(
                            title_font_family="Times New Roman",
                            title_font_size = 25,
                            title_font_color="darkblue",
                            title_x=0.5,
                            legend_title_text='Stats',
                            plot_bgcolor="rgb(240,240,240)",
                            title_text='Pace Stats over the Season',
                            height=550)
            
            return fig
            
        def timeSeriesSeason(metric,session):
            
            columns_g = ['Session Title','Player Name','Sprints', 'HML Efforts Maximum Speed','Accelerations','Max Deceleration' ,'High Intensity Bursts Maximum Speed','Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute']
            df_p = dataframe[columns_g]

            df_p = df_p[(df_p['Session Title']==session)]
            
            fig = go.Figure()

            fig.add_shape(type='line',
                            x0=0,
                            y0=6.5,
                            x1=11,
                            y1=6.5,
                            line=dict(color='Red',),
                            xref='x',
                            yref='y'
            )
            fig.add_trace(
                go.Bar(
                    x=df_p['Player Name'],
                    y=df_p[metric],
                    #name="Number of Sprints",
                    text = df_p[metric],
                    textposition='outside',
                    textfont=dict(
                    size=13,
                    color='#1f77b4'),      
                    #marker_color=["#f3e5f5", '#e1bee7', '#ce93d8', '#ba68c8','#ab47bc',
                     #           '#9c27b0','#8e24aa','#7b1fa2','#6a1b9a','#4a148c','#3c0a99'],
                    #marker_line_color='rgb(17, 69, 126)',
                    #marker_line_width=1, 
                ))
            fig.update_traces(texttemplate='%{text:.2s}')
            #fig.update_layout(legend_title_text='Stats',
            #                title_text='Pace Stats over the Season')
            
            fig.update_layout(
                                        title_font_family="Times New Roman",
                                        title_font_size = 25,
                                        title_font_color="darkblue",
                                        title_x=0.5,
                                        legend_title_text='Stats',
                                        plot_bgcolor="rgb(240,240,240)",
                                        title_text=f' Time Series Stats over the Season for {metric}',
                                        height=550
            )
            
            
            return fig

        players_list = dataframe['Player Name'].sort_values(ascending=True)
        players_list = players_list.unique()
        
        
        
        session_list = dataframe['Session Title'].sort_values(ascending=True)
        session_list = session_list.unique()
        session = st.selectbox("Select Session",session_list, index = 0)
            
        
        player1 = st.selectbox("Select Player",players_list, index = 0)
        combo_c = comboChart(player1)
            
        st.plotly_chart(combo_c, use_container_width=True)
            
        metric_list = ['Max Speed','Max Deceleration']
        metric_sel = st.selectbox("Select metric",metric_list, index = 0)
        timeSeries_f = timeSeriesSeason(metric_sel,session)
        st.plotly_chart(timeSeries_f, use_container_width=True)
        