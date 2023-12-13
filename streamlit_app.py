# CSCI 5922 Final Project
# Bailey Sauter, Fall 2023

import streamlit as st
import data_processing as dp
from keras.models import load_model
from data_processing import team_list

#---Various required sections for project website---
def introduction_page():
    st.header("NNostradamus Introduction")
    st.image("cover_image.jpg", caption="NCAA Women's Basketball popularity has skyrocketed", use_column_width=True)
    with open('Intro.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("angel-reese-hand-gesture.jpg", caption="Angel Reese Led the LSU Tigers to the 2023 NCAA Championship", use_column_width=True)
    with open('Intro2.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("power5.jpg", caption="Teams from the Power 5 conferences span the country and include the very best teams in collegiate women's basketball", use_column_width=True)
    st.session_state.first_run = False

def live_results(newest_results, selected_team):
    print("SELECTED TEAM INSIDE FUNCTION", selected_team)
    st.session_state.selected_team = selected_team
    st.markdown(newest_results[selected_team])

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
    st.header("Conclusions")
    with open('Conclusion.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("nostradamus.jpg", caption="Nostradamus was renowned for his prophecies, and has shown a knack for basketball as well", use_column_width=True)

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
    predictions_text = ""
    update_button = st.sidebar.button("Call API again (Update Schedule)")

    if 'first_run' not in st.session_state:
        introduction_page()
    elif home_button:
        introduction_page()
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
    elif schedule_button:
        ncaaw_model = load_model('ncaaw_model.h5')
        X_current = dp.get_current_year(use_API=False)
        st.session_state.predictions_text = dp.make_predictions(X_current, ncaaw_model)
        st.header("Live Predictions")
        st.write("Press the update button to call the API again and update the scheduled games")
        st.write("Select a team! Predictions are included for any Power 5 team.")
        options = [team.name for team in team_list]
        selected_team = st.selectbox("Team:", options)
        st.session_state.selected_team = selected_team
        live_results(newest_results=st.session_state.predictions_text, selected_team=st.session_state.selected_team)
    elif update_button:
        print("Update button pressed!!~!!")
        ncaaw_model = load_model('ncaaw_model.h5')
        X_current = dp.get_current_year(use_API=True)
        st.session_state.predictions_text = dp.make_predictions(X_current, ncaaw_model)
        st.header("Live Predictions")
        st.write("Press the update button in the sidebar to call the API again and update the scheduled games")
        st.write("Select a team! Predictions are included for any Power 5 team.")
        options = [team.name for team in team_list]
        selected_team = st.selectbox("Team:", options)
        st.session_state.selected_team = selected_team
        live_results(newest_results=st.session_state.predictions_text, selected_team=st.session_state.selected_team)
    else:
        st.header("Live Predictions")
        st.write("Press the update button in the sidebar to call the API again and update the scheduled games")
        st.write("Select a team! Predictions are included for any Power 5 team.")
        options = [team.name for team in team_list]
        selected_team = st.selectbox("Team:", options)
        st.session_state.selected_team = selected_team
        live_results(newest_results=st.session_state.predictions_text, selected_team=st.session_state.selected_team)
    # print("ST.SELECTION AT END OF MAIN:", st.session_state.selected_team)