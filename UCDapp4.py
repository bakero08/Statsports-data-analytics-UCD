import pandas as pd
import streamlit as st
from PIL import Image


def app():
    
    st.write("Upload Comparison File")
    data_file_comp = st.file_uploader("Upload csv File1:",type=["csv"])
            
    if data_file_comp is not None:
        file_details = {"filename":data_file_comp.name, "filetype":data_file_comp.type,
                        "filesize":data_file_comp.size}
    
        st.write(file_details)
        df_comp = pd.read_csv(data_file_comp)
        st.dataframe(df_comp.head(2))
        
    st.write("Upload Effort File")
    Effort_data_file = st.file_uploader("Upload csv File2:",type=["csv"])
            
    if Effort_data_file is not None:
        file_details1 = {"filename":Effort_data_file.name, "filetype":Effort_data_file.type,
                        "filesize":Effort_data_file.size}
    
        st.write(file_details1)
        df_effort = pd.read_csv(Effort_data_file)
        st.dataframe(df_effort.head(2))
        
    st.write("Upload HIA File")
    HIA_data_file = st.file_uploader("Upload csv File3:",type=["csv"])
            
    if HIA_data_file is not None:
        file_details2 = {"filename":HIA_data_file.name, "filetype":HIA_data_file.type,
                        "filesize":HIA_data_file.size}
    
        st.write(file_details2)
        df_HIA = pd.read_csv(HIA_data_file)
        st.dataframe(df_HIA.head(2))
        