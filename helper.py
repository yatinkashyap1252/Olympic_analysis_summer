import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Medal','Games','Year','City','Sport','Event'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['Total']=medal_tally['Total'].astype('int')
    
    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    
    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    
    return country,years

def fetch_medal_tally(df, year, country):
    # Drop duplicate medals to count only unique wins
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Medal', 'Games', 'Year', 'City', 'Sport', 'Event'])
    
    flag = 0
    temp_df = medal_df  # ✅ Set default value to avoid UnboundLocalError

    if year == "Overall" and country == "Overall":
        temp_df = medal_df  # ✅ Already set, but kept for clarity
    
    elif year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    
    elif year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df['Year'] == year]
    
    elif year != "Overall" and country != "Overall":  # ✅ Fixed condition
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    # Group data based on the flag condition
    if temp_df.empty:
        return pd.DataFrame(columns=['Gold', 'Silver', 'Bronze', 'Total'])  # ✅ Return empty DataFrame if no data
    
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Bronze', 'Silver']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Bronze', 'Silver']].sort_values('Gold', ascending=False).reset_index()

    # Add total medals column
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # Convert to integers for cleaner display
    for col in ['Gold', 'Silver', 'Bronze', 'Total']:
        x[col] = x[col].astype(int)

    return x

def data_over_time(df,col,y_label):
    nation_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nation_over_time.rename(columns={'count':y_label,'Year':'Edition'},inplace=True)
    return nation_over_time

def height_weight_analysis(df, sport):
    # Drop duplicates to get unique athletes
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    
    # Fill missing medal values
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    
    # Filter by selected sport
    temp_df = athlete_df[athlete_df['Sport'] == sport]
    
    # Create figure
    # Create figure with custom background
    fig = plt.figure(figsize=(12, 8), facecolor='#1e1e1e')  # dark gray background

    # Plot
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', palette='Set2', alpha=0.7)

    # Update axes background color
    ax.set_facecolor('#2a2a2a')  # slightly lighter gray
    ax.figure.set_facecolor('#1e1e1e')  # match the figure background

    # Update label colors
    ax.set_title(f"Height vs Weight of Athletes in {sport}", fontsize=16, color='white')
    ax.set_xlabel("Weight (kg)", color='white')
    ax.set_ylabel("Height (cm)", color='white')
    ax.tick_params(colors='white')  # tick color
    ax.legend(title='Medal', facecolor='#2a2a2a', edgecolor='white', labelcolor='white', title_fontsize='13', fontsize='11')

    # Grid
    ax.grid(True, color='gray', alpha=0.3)

    # Show in Streamlit
    st.pyplot(fig)

