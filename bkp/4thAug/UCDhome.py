import pandas as pd
import streamlit as st
from PIL import Image

#st.set_page_config(layout="wide")

def app():
    
    
    
    st.markdown(
            f"""
            <style>
            .stApp {{
                background: url("https://www.corkcityfc.ie/home/wp-content/uploads/2019/03/UCD-Bowl-scaled.jpg");
                background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    st.title("")
    col1, col2, col3 = st.columns((1,2,1))
    
    image = Image.open('ucd_logo.png')
    col1.image(image)
    col2.markdown("<h1 style='text-align: center; margin-center: 15px;color:Black;font-family:Arial Black'>VIDA - Data Analysing Tool UCD AFC </h1>", unsafe_allow_html=True)
    #col2.markdown("<style> .css-18c15ts {padding-top: 1rem; margin-top:-10px;} </style>", unsafe_allow_html=True)
    
    col3.write("")
        