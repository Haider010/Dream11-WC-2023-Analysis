import pandas as pd
import streamlit as st
import Stats
import sqlpycon as sq
from PIL import Image
import plotly.express as px

conn = sq.sql_py()

# Page title
st.title("WC-2023-Analysis")

# Load and display logo in the sidebar
logo = Image.open("pictures/logo.png")
st.sidebar.image(logo, use_column_width=True)

# Sidebar buttons
dream11_button = st.sidebar.button("Dream 11", use_container_width=True)
stats_button = st.sidebar.button("Stats", use_container_width=True)
about_button = st.sidebar.button("About", use_container_width=True)

def batsman_filter(x,y):
    with st.container(border=True):
        st.subheader('Filters ')
        col11,col12,col13 = st.columns(3)
        col21,col22,col23 = st.columns(3)
        style = col11.selectbox("Batting Style",['Left hand Bat','Right hand Bat'])
        position = col12.slider('Batting Position', x,y)
        matches = col13.slider('Num. of Matches Played',1,13)
        sr = col21.slider('Minimum Strike Rate',1,180)
        avg = col22.slider('Minimum Average',1,100)
        boundary = col23.slider('Minimum Boundary %',1,100)
    df = sq.sql_py.batter_find(conn,style,position,matches,sr,avg,boundary)
    return df
def all_rounder_filter():
    with st.container(border=True):
        st.subheader('Filters ')
        col11, col12, col13, col14 = st.columns(4)
        col21, col22, col23 = st.columns(3)
        position = col11.slider('Batting Position', 4, 9)
        matches_batted = col12.slider('Innings Batted', 1, 13)
        bt_sr = col13.slider('Batting Strike Rate', 1, 180)
        bt_avg = col14.slider('Batting Average', 1, 100)
        matches_bowled = col21.slider('Innings Bowled', 1, 11)
        economy = col22.slider('Economy', 1, 13)
        bw_sr = col23.slider('Bowling Strike Rate', 1, 120)
    df = sq.sql_py.all_rounder_find(conn,position,matches_batted,bt_sr,bt_avg,matches_bowled,economy,bw_sr)
    return df
def bowler_filter():
    with st.container(border=True):
        col11, col12= st.columns(2)
        col21, col22, col23 = st.columns(3)
        st.subheader('Filters ')
        style = col11.selectbox("Bowling Style", ['Slow', 'Fast'])
        avg = col12.slider('Average', 1, 100)
        matches = col21.slider('Innings Bowled', 1, 11)
        economy = col22.slider('Economy', 1, 13)
        sr = col23.slider('Bowling Strike Rate', 1, 120)
    df = sq.sql_py.bowlers_find(conn,style,avg,matches,economy,sr)
    return df
def display_dream11():
    st.subheader('Roles')

    if 'selected_role' not in st.session_state:
        st.session_state.selected_role = "Openers"  # Default role
    if 'dream11_team' not in st.session_state:
        st.session_state.dream11_team = []
    Openers, Anchors, Finisher, All_rounder, Bowler = st.columns(5)

    if Openers.button("Openers", use_container_width=True):
        st.session_state.selected_role = "Openers"
    if Anchors.button("Anchors", use_container_width=True):
        st.session_state.selected_role = "Anchors"
    if Finisher.button("Finishers", use_container_width=True):
        st.session_state.selected_role = "Finishers"
    if All_rounder.button("All Rounders", use_container_width=True):
        st.session_state.selected_role = "All-rounder"
    if Bowler.button("Bowlers", use_container_width=True):
        st.session_state.selected_role = "Bowler"
    df = pd.DataFrame()
    if st.session_state.selected_role == "Openers":
        df = batsman_filter(1, 3)
    elif st.session_state.selected_role == "Anchors":
        df = batsman_filter(3, 6)
    elif st.session_state.selected_role == "Finishers":
        df = batsman_filter(4, 8)
    elif st.session_state.selected_role == "All-rounder":
        df = all_rounder_filter()
    elif st.session_state.selected_role == "Bowler":
        df = bowler_filter()
    with st.container(border=True):
        st.subheader("Available Players")
        st.dataframe(df)
    with st.container(border=True):
        st.subheader("Adding Players to Dream11")
        selected_player = st.selectbox("Select a player to add to Dream11", df['player_name'])
        if st.button("Add Player to Dream11"):
            if len(st.session_state.dream11_team) == 11:
                st.warning('Team is Full', icon="⛔")
            elif selected_player not in st.session_state.dream11_team:
                st.session_state.dream11_team.append(selected_player)
                st.success(f"{selected_player} added to Dream11!")
            else:
                st.warning(f"{selected_player} is already in your Dream11 team.")

    with st.container(border=True):
        st.subheader("Your Dream11 Team")
        updated_team = []
        for player in st.session_state.dream11_team:
            col1, col2 = st.columns([3, 1])
            col1.write(player)
            if col2.button("Double Click To Remove", key=player):
                continue
            updated_team.append(player)
        st.session_state.dream11_team = updated_team
def display_stats():
    with st.container(border=True):
        st.subheader("Players Contribution in Total Team Runs")
        teams = Stats.teams_name()
        team = st.selectbox("Pick a Team",teams)
        df = Stats.runs_contribution(team)
        fig = px.pie(df,values='Runs',names='Batsman_Name')
        st.plotly_chart(fig)
    with st.container(border=True):
        st.subheader("Teams with most Runs")
        top_5_runs = Stats.top_5_runs()
        st.bar_chart(top_5_runs,x='Team_Innings',y='Runs',color='#7a49a5')
    with st.container(border=True):
        st.subheader("Batsman with most Runs")
        top_5_runs = Stats.top_5_bats()
        st.bar_chart(top_5_runs,x='Batsman_Name',y='Runs',color='#7a49a5')
    with st.container(border=True):
        st.subheader("Players Contribution in Total Team Wickets")
        teams = Stats.teams_name()
        team = st.selectbox("Pick a Team:",teams)
        df = Stats.wickets_contribution(team)
        fig = px.pie(df,values='Wickets',names='Bowler_Name',color_discrete_sequence=px.colors.qualitative.T10)
        st.plotly_chart(fig)
    with st.container(border=True):
        st.subheader("Teams with most Wickets")
        top_5_wic = Stats.top_5_wic()
        st.bar_chart(top_5_wic,x='Bowling_Team',y='Wickets',color='#160042')
    with st.container(border=True):
        st.subheader("Bowlers with most Wickets")
        top_5_p_wic = Stats.top_5_p_wic()
        st.bar_chart(top_5_p_wic,x='Bowler_Name',y='Wickets',color='#160042')

if 'page' not in st.session_state:
    st.session_state.page = "Dream 11"

if dream11_button:
    st.session_state.page = "Dream 11"
elif stats_button:
    st.session_state.page = "Stats"
elif about_button:
    st.session_state.page = "About"


if st.session_state.page == "Dream 11":
    display_dream11()
elif st.session_state.page == "Stats":
    display_stats()
elif st.session_state.page == "About":
    st.write("Create Your Dream11 Team Dive into the world of fantasy cricket with our Dream11 team"
             "builder. Here, you can assemble your ultimate fantasy cricket team by selecting your"
             "favorite players.\n")
