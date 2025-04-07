import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def country_wise_analysis(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Year','NOC','Games','Team','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    fig=px.line(final_df,x='Year',y='Medal')
    st.header(f"{country} Medal Tally Over the Years")
    st.plotly_chart(fig,use_container_width=True)
    
def country_sport_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Year', 'NOC', 'Games', 'Team', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]

    # Pivot the data
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    # Create the figure
    fig, ax = plt.subplots(figsize=(20, 20))
    fig.patch.set_alpha(0)
    heatmap=sns.heatmap(pt, annot=True, fmt=".0f", cmap="magma", linewidths=0.5, ax=ax)
    
    ax.tick_params(axis='x', rotation=45,colors='white')
    ax.tick_params(axis='y', rotation=0,colors='white')
    ax.set_xlabel('Year', fontsize=14, color='white')
    ax.set_ylabel('Sport', fontsize=14, color='white')
    
    # Get the colorbar object
    colorbar = heatmap.collections[0].colorbar

    # Change tick label color
    colorbar.ax.yaxis.set_tick_params(color='white')
    for label in colorbar.ax.get_yticklabels():
        label.set_color('white')  # You can change 'red' to any color

    # Display in Streamlit
    st.header(f"{country} Medal Tally in Different Sports")
    st.pyplot(fig)

def most_successful_athlete(df,country):
    temp_df = df.dropna(subset=['Medal'])
    new_df = temp_df[temp_df['region'] == country]
    
    # Group by athlete and count medals
    most_successful = new_df.groupby('Name').count()['Medal'].reset_index()
    most_successful = most_successful.sort_values(by='Medal', ascending=False).head(10)

    # Create the figure
    fig, ax = plt.subplots(figsize=(20, 10))
    fig.patch.set_alpha(0)
    sns.barplot(data=most_successful, x='Medal', y='Name', palette='magma')
    
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=14, rotation=0, color='white')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=20, rotation=0, color='white')
    ax.set_xlabel('Number of Medals', fontsize=14, color='white')
    ax.set_ylabel('Athlete Name', fontsize=14, color='white')
    
    # Display in Streamlit
    st.header(f"Most Successful Athletes from {country}")
    st.pyplot(fig)
    
    # Filter data for the selected country and drop missing medals
    country_df = df[(df['region'] == country) & (df['Medal'].notna())]

    # Check if any medals exist for the selected country
    if country_df.empty:
        st.warning(f"❌ No medal data found for **{country}**.")
    else:
        # Count medal types
        medal_counts = country_df['Medal'].value_counts().reset_index()
        medal_counts.columns = ['Medal Type', 'Count']

        # Plot pie chart
        fig_pie = px.pie(medal_counts, 
                        names='Medal Type', 
                        values='Count', 
                        title=f'🏅 Medal Distribution for {country}',
                        color='Medal Type',
                        color_discrete_map={'Gold':'gold', 'Silver':'silver', 'Bronze':'#cd7f32'})

        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(title_x=0.5)

        st.plotly_chart(fig_pie, use_container_width=True)
