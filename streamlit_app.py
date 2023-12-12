# CSCI 5922 Final Project
# Bailey Sauter, Fall 2023

import streamlit as st
import data_processing as dp
from keras.models import load_model

#---Various required sections for project website---
def introduction_page():
    st.header("Project Introduction (5 paragraphs)")
    st.write("100% non-technical")

def live_results(newest_results):
    st.header("Live Results")
    st.write("Press the update button to call the API again and update the scheduled games")
    st.write(newest_results)

def data_gathering():
    st.header("Data Gathering")
    st.write("Include Gathering and cleaning")

def analysis_page():
    st.header("Analysis")
    st.write("Models/Methods Used")

def results_page():
    st.header("Technical Results")
    st.write("This is the place for technical results")

def about_me():
    st.header("About the Author")
    st.image("bio_image.jpg", caption="Author Bailey Sauter", use_column_width=True)
    st.write("Bailey Sauter is a 2nd-year Ph.D. student in Power Electronics at the University of Colorado Boulder. "
             "He earned his B.S. in Electrical and Computer Engineering at Oregon State University with minors in "
             "Computer Science and Spanish. Past employment "
             "includes the Oregon State Energy Systems Lab (Corvallis, OR), Tektronix (Beaverton, OR) and Imperix "
             "(Sion, Switzerland)."
             "\n\nWhen not working or studying, Bailey can be found running, skiing, or biking.")

def conclusion():
    st.header("Conclusion (5 paragraphs)")
    st.write("100% non-technical")

run_once = False

if __name__ == '__main__':

    # ---Everything below here is website-related---
    home_button = st.sidebar.button("Introduction")
    schedule_button = st.sidebar.button("Scheduled Games + Predictions")
    data_button = st.sidebar.button("Data and Prep")
    analysis_button = st.sidebar.button("Analysis")
    results_button = st.sidebar.button("Technical Results")
    conclusion_button = st.sidebar.button("Conclusions")
    about_button = st.sidebar.button("About the Author")

    if home_button:
        introduction_page()
    elif schedule_button:
        ncaaw_model = load_model('ncaaw_model.h5')
        X_current = dp.get_current_year(use_API=False)
        predictions_text = dp.make_predictions(X_current, ncaaw_model)
        live_results(newest_results=predictions_text)
    elif data_button:
        data_gathering()
    elif analysis_button:
        analysis_page()
    elif results_button:
        results_page()
    elif conclusion_button:
        conclusion()
    elif about_button:
        about_me()
    else:
        introduction_page()

