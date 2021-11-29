import streamlit as st
import datetime
import requests
import pandas as pd
import joblib
from sunny_britain.data import DataClean

st.markdown("""# Inverter Converter :battery:""")
st.markdown("""Use this tool to convert your solar park inverter data to insights on unavailability likelihood """)

st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.markdown("""## Unavailability forecast""")
    #progress bar
    import time

    'Peering deep into the future...'

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        bar.progress(i + 1)
        time.sleep(0.1)

    # Cleaning the imported data
    data_date = DataClean.add_date_features(data)
    data_discard = DataClean.discard_features(data_date)
    clean_data = DataClean.summary_statistics(data_discard)
    X = clean_data[0]
    y = clean_data[1]

    # Putting the model to work
    model = joblib.load('LightGBM model.joblib')
    y_pred = (model.predict(X))[-7:]

    for i in range(0,7):
        if y_pred[i] == 0:
            st.success(f""":battery: Day {i+1} - **No outage** expected""")
        else:
            st.error(f""":skull_and_crossbones: Day {i+1} - **Outage** expected""")
