import pandas as pd
def teams_name():
    df = pd.read_csv("datasets/batting_summary.csv")
    return list(df['Team_Innings'].unique())
def runs_contribution(team):
    df = pd.read_csv("datasets/batting_summary.csv")
    df = df.groupby(['Team_Innings','Batsman_Name'],as_index=False).agg({'Team_Innings':'first','Runs':'sum'})
    df = df[df['Team_Innings'] == '{}'.format(team)].drop('Team_Innings',axis=1).reset_index(drop=True)
    return df
def top_5_runs():
    df = pd.read_csv("datasets/batting_summary.csv")
    temp_df = pd.DataFrame(df.groupby('Team_Innings',as_index=False)['Runs'].sum())
    temp_df.sort_values('Runs',ascending=False,inplace=True)
    return temp_df.head()
def top_5_bats():
    df = pd.read_csv("datasets/batting_summary.csv")
    temp_df = pd.DataFrame(df.groupby('Batsman_Name',as_index=False)['Runs'].sum())
    temp_df.sort_values('Runs',ascending=False,inplace=True)
    return temp_df.head()
def wickets_contribution(team):
    df = pd.read_csv("datasets/bowling_summary.csv")
    df = df.groupby(['Bowling_Team','Bowler_Name'],as_index=False).agg({'Bowling_Team':'first','Wickets':'sum'})
    df = df[df['Bowling_Team'] == '{}'.format(team)].drop('Bowling_Team',axis=1).reset_index(drop=True)
    return df
def top_5_wic():
    df = pd.read_csv("datasets/bowling_summary.csv")
    temp_df = pd.DataFrame(df.groupby('Bowling_Team',as_index=False)['Wickets'].sum())
    temp_df.sort_values('Wickets',ascending=False,inplace=True)
    return temp_df.head()
def top_5_p_wic():
    df = pd.read_csv("datasets/bowling_summary.csv")
    temp_df = pd.DataFrame(df.groupby('Bowler_Name',as_index=False)['Wickets'].sum())
    temp_df.sort_values('Wickets',ascending=False,inplace=True)
    return temp_df.head()