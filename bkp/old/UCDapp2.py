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
        
        col1.title("Individual Player Performance")
        #col2.image(image)
        
        dataframe = pd.read_csv("Comparison.csv")
        dataframe['Session Date']= pd.to_datetime(dataframe['Session Date'])
        match_dates = dataframe['Session Date'].dt.date
        match_dates = match_dates.unique()
        match_dates = np.sort(match_dates, axis=None)
        
        columns_pizza =['Session Title','Player Name','Distance Per Min', 'HSR Per Minute (Absolute)','Number Of High Intensity Bursts', 'High Intensity Bursts Total Distance', 'High Intensity Bursts Maximum Speed','Max Speed', 'Average Speed','Sprints','Max Acceleration','Max Deceleration', 'HMLD Per Minute', 'HML Distance', 'HML Efforts Total Distance', 'HML Efforts','HML Efforts Maximum Speed']
        
        pizza_df = dataframe[columns_pizza]
        players_list = pizza_df['Player Name'].sort_values(ascending=True)
        players_list = players_list.unique()
        session_list = pizza_df['Session Title'].sort_values(ascending=True)
        session_list = session_list.unique()

        def pizzaChart(p1):
        
            
            #font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
            #               "Roboto-Regular.ttf?raw=true"))
            #font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
             #                       "Roboto-Italic.ttf?raw=true"))
            #font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
              #                      "Roboto-Medium.ttf?raw=true"))
            pl_img = Image.open(f"Facepack/{p1}.png")
            ucd_img = Image.open("ucd_logo.png")
            
            
            
            pizza_df_player = pizza_df[(pizza_df['Player Name']==p1)]
        
            pizza_value_df=[]
            pizza_value_df = pizza_df_player.drop(['Session Title','Player Name'], axis=1 )
            
            pizza_values = pizza_value_df.mean()
            #ra = ra.to_list()
            
            np_array = np.array(pizza_values)
            np_round = np.around(np_array, 2)
            
            pizza_values = list(np_round)
            
            params = [ 'Distance Per Min', 'HSR Per Minute (Absolute)','Number Of High Intensity Bursts','High Intensity Bursts Total Distance','High Intensity Bursts Maximum Speed','Max Speed', 'Average Speed','Sprints','Max Acceleration','Max Deceleration','HMLD Per Minute', 'HML Distance', 'HML Efforts Total Distance','HML Efforts','HML Efforts Maximum Speed' ]
            
            # calculating the percentile values with scipy stats. Since we have raw values

            pvalues = []
            for x in range(len(params)):   
                pvalues.append(math.floor(stats.percentileofscore(pizza_df[params[x]],pizza_values[x])))
                
                
            
            # parameter list
            params_new = [ 'Distance p/Min','HSR p/Min','Number of HIB','HIB Distance', 'HIB Max Speed','Max Speed', 'Avg Speed','Number of Sprints','Max Accel','Max Decel','HMLD p/Min','HML Distance', 'HML Efforts Distance','HML Efforts','HML Efforts Max Speed']
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
                    #fontproperties=font_normal.prop, 
                    va="center"
                ),                               # values to be used when adding parameter
                kwargs_values=dict(
                    color="#000000", 
                fontsize=11,
               #     fontproperties=font_normal.prop, 
               zorder=3,
                    bbox=dict(
                        edgecolor="#000000", facecolor="cornflowerblue",
                        boxstyle="round,pad=0.2", lw=1
                    )
                )                                # values to be used when adding parameter-values
            )
            
            # add title
            fig.text(
                0.515, 0.975, f"{p1} - UCD AFC", size=16,
                ha="center", 
                #fontproperties=font_bold.prop, 
                color="#000000"
            )
            
            # add subtitle
            fig.text(
                0.515, 0.953,
                "Percentile Rank vs Squad | Season 2021-22",
                size=13,
                ha="center", 
                #fontproperties=font_bold.prop,
                color="#000000"
            )
            
            # add credits
            CREDIT_1 = "data: STATSports Apex"
            CREDIT_2 = "inspired by: @mckayjohns"
            
            fig.text(
                0.99, 0.02, f"{CREDIT_1}\n{CREDIT_2}", size=9,
                #fontproperties=font_italic.prop,
                color="#000000",
                ha="right"
            )
            
            # add text
            fig.text(
                0.34, 0.925, "Intensity          Pace                   HML", size=14,
                #fontproperties=font_bold.prop,
                color="#000000"
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
                pl_img, fig, left=0.4478, bottom=0.433, width=0.13, height=0.127
            )
            
            ax_image2 = add_image(
                ucd_img, fig, left=0.1, bottom=0.02, width=0.13, height=0.127
            )
            
            #plt.title("Pizza Chart  ", fontsize=20, fontfamily='serif', color = 'Green')
            return fig
            
        def gauges(p1,s1):
            columns_g = ['Session Title','Player Name', 'Max Speed','Total Distance', 'HML Distance']
            player_guage_df = dataframe[columns_g]
            player_guage_df = player_guage_df[(player_guage_df['Player Name']==p1)]
            
            player_guage_df = player_guage_df[(player_guage_df['Session Title']==s1)].reset_index()
            player_guage_df = player_guage_df.drop(['index'],axis=1)
            #player_guage_df
            
            max_sp = player_guage_df.iloc[0]['Max Speed']
            t_dis = player_guage_df.iloc[0]['Total Distance']
            hml_dis = player_guage_df.iloc[0]['HML Distance']
            
            fig_d = go.Figure(go.Indicator(
                domain = {'x': [0, 1], 'y': [0, 1]},
                value = t_dis,
                mode = "gauge+number+delta",
                title = {'text': "Total Distance"},
                delta = {'reference': 10000},
                gauge = {'axis': {'range': [None, 15000]},
                        'steps' : [
                            {'range': [0, 8000], 'color': "lightgray"},
                            {'range': [8000, 10000], 'color': "gray"}],
                        'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 14000}}))
            fig_d.update_layout(
            autosize=False,
            width=500,
            height=400)
            
            #fig_s.show()
            
            fig_hd = go.Figure(go.Indicator(
                domain = {'x': [0, 1], 'y': [0, 1]},
                value = hml_dis,
                mode = "gauge+number+delta",
                title = {'text': "HML Distance"},
                delta = {'reference': 2500},
                gauge = {'axis': {'range': [None, 4000]},
                        'bar': {'color': "crimson"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps' : [
                            {'range': [0, 1500], 'color': "beige"},
                            {'range': [1500, 2500], 'color': "palegoldenrod"}],
                        'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 3500}}))
            fig_hd.update_layout(
            autosize=False,
            width=500,
            height=400)
            #fig_d.show()
            
            
            fig_s = go.Figure(go.Indicator(
                domain = {'x': [0, 1], 'y': [0, 1]},
                value = max_sp,
                mode = "gauge+number+delta",
                title = {'text': "Max Speed"},
                delta = {'reference': 8.5},
                gauge = {'axis': {'range': [None, 10]},
                        'bar': {'color': "red"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps' : [
                            {'range': [0, 6], 'color': "yellow"},
                            {'range': [6, 8.5], 'color': "orange"}],
                        'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 8.5}}))
            
            #fig.update_layout( font = {'color': "darkblue", 'family': "Arial"})
            fig_s.update_layout(
            autosize=False,
            width=500,
            height=400)
            #fig_hd.show()
            return fig_s,fig_d,fig_hd
            
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
                            y0=7.5,
                            x1=11,
                            y1=7.5,
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


        
        with st.sidebar:
            st.title('Player Performance Analysis')
            #st.sidebar.markdown('''##### Player's performance over the season''')
            player1 = st.selectbox("Select Player",players_list, index = 0)
            session = st.selectbox("Select Session",session_list, index = 0)
            selected_date = st.sidebar.select_slider('Select the match date range', match_dates, value=[min(match_dates),max(match_dates)])
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
            
            submitButton = st.button("Submit")
            #st.subheader('Key Metrics')
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
        if submitButton:
            pchart = pizzaChart(player1)
            gauge_s, gauge_d, gauge_hd = gauges(player1,session)
            combo_c = comboChart(player1)
            
            player_img = Image.open(f"Facepack/{player1}.png")
            
            col1.markdown("_________________")
            col1.markdown('**Date of birth/Age:**   \n **Citizenship:**   \n**Height:**   \n **Position:**   \n **Joined:**   \n **Contract expires:**   \n**Date of last contract extension:** ')
            
            col2.image(player_img)
            st.markdown("_________________")            
            col3,col4,col5 = st.columns(3)
            
            col3.plotly_chart( gauge_s, use_container_width=True)
            col4.plotly_chart( gauge_d, use_container_width=True)
            col5.plotly_chart(gauge_hd, use_container_width=True)
            col6,col7 = st.columns(2)
            
            col6.pyplot(pchart) 
            col7.plotly_chart(combo_c, use_container_width=True)
            st.plotly_chart(combo_c, use_container_width=True)
            
            metric_list = ['Max Speed']
            metric_sel = st.selectbox("Select metric",metric_list, index = 0)
            timeSeries_f = timeSeriesSeason(metric_sel,session)
            st.plotly_chart(timeSeries_f, use_container_width=True)
        