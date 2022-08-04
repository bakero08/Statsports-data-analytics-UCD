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
        
        col1.title("Team Performance Analysis")
        #col2.image(image)
        
        dataframe = pd.read_csv("Comparison.csv")
        dataframe['Session Date']= pd.to_datetime(dataframe['Session Date'])
        match_dates = dataframe['Session Date'].dt.date
        match_dates = match_dates.unique()
        match_dates = np.sort(match_dates, axis=None)
        

        
        def scatterPlot():
            columns_to_keep_scat = ['Player Name', 'Distance Per Min', 'HSR Per Minute (Absolute)','Average Speed', 'Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute']
            scatter_df = dataframe[columns_to_keep_scat]
            
            scatter_df = scatter_df.groupby('Player Name').mean()
            scatter_df = scatter_df.reset_index(0)
            #scatter_df
        
            position = ['FWD', 'MID', 'DEF','MID', 'DEF', 'FWD','FWD', 'DEF','MID', 'DEF','DEF', 'MID', 'MID','FWD', 'FWD', 'DEF','MID', 'DEF', 'DEF','MID']
            scatter_df['position'] = position
            scatter_df = round(scatter_df,2)
            
            plot = px.scatter(scatter_df, x='Total Distance', y='HMLD Per Minute', color='position', size='Distance Per Min', symbol='position', hover_data = ['Player Name'], trendline="ols",trendline_scope="overall")
            plot.update_layout(
                            title_font_family="Times New Roman",
                            title_font_size = 25,
                            title_font_color="darkblue",
                            title_x=0.5,
                            plot_bgcolor="rgb(240,240,240)",
                            title_text='Team Position-wise Distance stats over the season',
                            height=550)
            return plot    
            
    
        def timeSeriesSeason(metric,session):
            
            columns_g = ['Session Title','Player Name','Sprints', 'HML Efforts Maximum Speed','Accelerations','Max Deceleration' ,'High Intensity Bursts Maximum Speed','Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute']
            df_p = dataframe[columns_g]

            df_p = df_p[(df_p['Session Title']==session)]
            
            fig = go.Figure()
            
            if metric == 'Max Acceleration':
            
                    fig.add_shape(type='line',
                                    x0=0,
                                    y0=4.5,
                                    x1=12,
                                    y1=4.5,
                                    #line=dict(color='Red',),
                                    xref='x',
                                    yref='y',
                                    line=dict(
                                    color="red",
                                    width=2,
                                    dash="dashdot",)
                                  )
                    
                    fig.add_shape(type='line',
                                    x0=0,
                                    y0=4.5,
                                    x1=12,
                                    y1=4.5,
                                    #line=dict(color='Red',),
                                    xref='x',
                                    yref='y',
                                    line=dict(
                                    color="red",
                                    width=2,
                                    dash="dashdot",)
                                  )
                                        
            else:
                    fig.add_shape(type='line',
                                    x0=0,
                                    y0=6.5,
                                    x1=12,
                                    y1=6.5,
                                    #line=dict(color='Red',),
                                    xref='x',
                                    yref='y',
                                    line=dict(
                                    color="red",
                                    width=2,
                                    dash="dashdot",)
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
                    marker_color='lemonchiffon',
                    marker_line_color='orange',
                    marker_line_width=1, 
                ))
            fig.update_traces(texttemplate='%{text:.2s}')
                   
            fig.update_layout(
                                        title_font_family="Times New Roman",
                                        title_font_size = 25,
                                        title_font_color="darkblue",
                                        title_x=0.5,
                                        legend_title_text='Stats',
                                        plot_bgcolor="rgb(240,240,240)",
                                        title_text=f'{metric} for the Team with Thresholds',
                                        height=550
            )
            
            
            return fig

        
        def accDecPlot(match):
            columns_to_keep_ad = ['Session Title','Player Name', 'Total Distance','Distance Per Min', 'Accelerations','Decelerations']
            adratio_df = dataframe[columns_to_keep_ad]
            adratio_df = adratio_df[adratio_df['Session Title']==match]
            adratio_df['Acc/Dec'] = adratio_df['Accelerations']/adratio_df['Decelerations']
            adratio_df['Acc/Dec'] = adratio_df['Acc/Dec'].round(2)
            
            plot = px.scatter(adratio_df, x='Total Distance', y='Acc/Dec', color='Player Name', size='Distance Per Min')
            plot.update_layout(
                            title_font_family="Times New Roman",
                            title_font_size = 25,
                            title_font_color="darkblue",
                            title_x=0.5,
                            plot_bgcolor="rgb(240,240,240)",
                            title_text=f'Acceleration - Deceleration Ratio for {match}',
                            height=550)
            return plot
            
        

        def scatterPlotCustom(xaxis,yaxis):
            columns_to_keep_scat = ['Player Name', 'Distance Per Min', 'HSR Per Minute (Absolute)','Average Speed', 'Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute', 'Accelerations','Decelerations','Dynamic Stress Load Zone 6','Impacts Zone 6']
            scatter_df = dataframe[columns_to_keep_scat]
            
            scatter_df = scatter_df.groupby('Player Name').mean()
            scatter_df = scatter_df.reset_index(0)
            #scatter_df
        
            #position = ['MID', 'ATT', 'DEF','ATT', 'MID', 'DEF','ATT', 'MID','MID', 'DEF','ATT', 'MID', 'DEF','ATT', 'MID', 'DEF','ATT', 'MID', 'DEF','DEF']
            #scatter_df['position'] = position
            scatter_df = round(scatter_df,2)
            
            plot = px.scatter(scatter_df, x=xaxis, y=yaxis, color='Player Name', hover_data = ['Player Name'], trendline="ols",trendline_scope="overall")
            plot.update_layout(
                            title_font_family="Times New Roman",
                            title_font_size = 25,
                            title_font_color="darkblue",
                            title_x=0.5,
                            plot_bgcolor="rgb(240,240,240)",
                            title_text='Average stats over the season',
                            showlegend=False,
                            height=550)
            plot.update_traces(marker=dict(size=12))
            return plot    
         
         
        scatterP = scatterPlot()
        st.plotly_chart(scatterP, use_container_width=True)

           
        col3,col4 = st.columns((1,3))
        
        
        session_list = dataframe['Session Title'].sort_values(ascending=True)
        session_list = session_list.unique()
        session = col3.selectbox("Select Session",session_list, index = 0)
        
        metric_list = ['Max Speed','Max Deceleration','Max Acceleration']
        metric_sel = col3.selectbox("Select metric",metric_list, index = 0)
        
        timeSeries_f = timeSeriesSeason(metric_sel,session)
        col4.plotly_chart(timeSeries_f, use_container_width=True)
        
        col5,col6 = st.columns((1,3))
        session_list2 = dataframe['Session Title'].sort_values(ascending=True)
        session_list2 = session_list2.unique()
        session2 = col5.selectbox("Select Session :",session_list2, index = 0)
        adPlot = accDecPlot(session2)
        col6.plotly_chart(adPlot, use_container_width=True)
        

        columns_to_keep_s = ['Distance Per Min', 'HSR Per Minute (Absolute)','Average Speed', 'Max Speed', 'Max Acceleration','Total Distance', 'HMLD Per Minute', 'Accelerations','Decelerations','Dynamic Stress Load Zone 6','Impacts Zone 6']
        scat_df = dataframe[columns_to_keep_s]
        xax = np.sort(scat_df.columns.values)
        yax = np.sort(scat_df.columns.values)[::-1]
        
        col7,col8 = st.columns((1,3))
        
        xaxis_sel = col7.selectbox("Select x-axis",xax, index = 0)
        yaxis_sel = col7.selectbox("Select y-axis",yax, index = 0)
        
        scatterC = scatterPlotCustom(xaxis_sel,yaxis_sel)
        col8.plotly_chart(scatterC, use_container_width=True)
            
