import UCDApp
import UCDapp2
import UCDhome

import streamlit as st

#st.set_page_config(layout="wide")

PAGES = {
    "Home Page": UCDhome,
    "Player Comparision": UCDApp,
    "Player Stats": UCDapp2
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))


page = PAGES[selection]
page.app()