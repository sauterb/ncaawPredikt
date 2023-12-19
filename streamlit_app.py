# CSCI 5922 Final Project
# Bailey Sauter, Fall 2023

import streamlit as st
import data_processing as dp
from keras.models import load_model
from data_processing import team_list

#---Various required sections for project website---
def introduction_page():
    st.header("Meet :rainbow[NNostradamus]!")
    st.image("cover_image.jpg", caption="NCAA Women's Basketball popularity has skyrocketed", use_column_width=True)
    with open('Intro.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("angel-reese-hand-gesture.jpg", caption="Angel Reese led the LSU Tigers to the 2023 NCAA Championship", use_column_width=True)
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
    st.header("Data Gathering and Cleaning")
    with open('DataPrep.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("data_lifecycle.jpg",
             caption="The flowchart depicts how data goes from the original format to being used by the model",
             use_column_width=True)

def analysis_page():
    st.header("Models + Methods")
    with open('Analysis.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("lstm.png",
             caption="A simplified version of a single timestep in an LSTM network",
             use_column_width=True)
    with open('Analysis2.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("model_summary.png",
             caption="Keras model summary of LSTM",
             use_column_width=True)

def results_page():
    st.header("Technical Results")
    with open('Results.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("model_loss_graph.jpeg",
             caption="Loss vs. Accuracy of NNostradamus over training epochs",
             use_column_width=True)
    with open('Results2.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("raw_predictions.png",
             caption="Raw outcome of the model predicting the likelihood an array of teams will win their games",
             use_column_width=True)

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
    with open('Conclusion2.txt', 'r') as file:
        content = file.read()
    st.markdown(content)
    st.image("trophy.jpg", caption="", use_column_width=True)
run_once = False

if __name__ == '__main__':

    # ---This is rerun on any website event---
    home_button = st.sidebar.button("Introduction")
    schedule_button = st.sidebar.button("Scheduled Games + Predictions")
    data_button = st.sidebar.button("Data Preparation")
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
        print("Update button pressed!")
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
