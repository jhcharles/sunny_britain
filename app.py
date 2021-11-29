import streamlit as st
import datetime
import requests
import pandas as pd

st.markdown("""# Inverter Converter :battery:""")
st.markdown("""Use this tool to convert your solar park inverter data to insights on unavailability likelihood """)

st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)
