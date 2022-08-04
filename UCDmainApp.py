import UCDhome
import UCDApp
import UCDapp2
import UCDapp3
import UCDapp4

import streamlit as st

#st.set_page_config(layout="wide")

PAGES = {
    "Home Page": UCDhome,
    "Data Upload": UCDapp4,
    "Team Analysis": UCDapp3,
    "Player Analysis": UCDapp2,
    "Player Comparision": UCDApp
    
    
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))


page = PAGES[selection]
page.app()