import UCDApp
import UCDapp2
import UCDapp3
import UCDhome

import streamlit as st

#st.set_page_config(layout="wide")

PAGES = {
    "Home Page": UCDhome,
    "Player Comparision": UCDApp,
    "Player Stats": UCDapp2,
    "Seasonal Stats": UCDapp3
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))


page = PAGES[selection]
page.app()