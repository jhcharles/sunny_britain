import streamlit as st
import datetime
import requests
import pandas as pd
import joblib
from PIL import Image
from sunny_britain.data import DataClean

st.markdown("""# Inverter Converter :battery:""")
st.markdown("""Use this tool to convert your solar park inverter data to insights on unavailability likelihood
                \n Please import at least 7 days of data""")

st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Cleaning the imported data
    data_date = DataClean.add_date_features(data)
    data_discard = DataClean.discard_features(data_date)
    clean_data = DataClean.summary_statistics(data_discard)
    X = clean_data[0]
    y = clean_data[1]

    def time(x):
        return x.time()

    data_discard['time']=data_discard['timestamp'].dropna().apply(time)
    grouped = data_discard.groupby(['time']).mean().reset_index()
    all_irradiance = grouped[['Irradiance PoA (W*m^-2) [Inverter 2]']]
    all_irradiance.rename(columns={'Irradiance PoA (W*m^-2) [Inverter 2]': 'Input'}, inplace=True)
    all_current = grouped[['Current Inverter DC (A) [Inverter 2]']]
    all_current.rename(columns={'Current Inverter DC (A) [Inverter 2]': 'Input'},inplace=True)

    #progress bar
    import time

    'Evaluating the uploaded data...'

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        bar.progress(i + 1)
        time.sleep(0.1)

    # Putting the model to work
    model = joblib.load('LightGBM model.joblib')
    y_pred = (model.predict(X))[-7:]

    for i in range(0,7):
        if y_pred[i] == 0:
            st.success(f""":battery: Day {i+1} - **No outage** expected""")
        else:
            st.error(f""":skull_and_crossbones: Day {i+1} - **Outage** expected""")

    ## Anomaly detection
    st.markdown("""## Anomaly monitoring""")
    st.markdown("""Comparing uploaded data with normal behavior""")

    anomaly = pd.read_csv('Current_AC_Test.csv')
    y1 = anomaly['Time']
    X_current = anomaly[['Avg Curr']]
    X_irradiance = (anomaly[['Avg Irr']])

    col1, col2 = st.columns([1, 1])

    data_irr = pd.concat([X_irradiance, all_irradiance], axis=1)
    data_current = pd.concat([X_current, all_current], axis=1)

    col1.subheader('Current')
    col1.line_chart(data_current)

    col2.subheader('Irradiance')
    col2.line_chart(data_irr)

    st.markdown("""## Unavailability forecast""")
    st.markdown("""Applying the Sunny Britain predictive model""")

    ## API joke

    if st.checkbox('Satisfied?'):
        st.write('''Next time just call our API directly!
            ''')
        image = Image.open('API.png')
        st.image(image, caption='', use_column_width=False)
