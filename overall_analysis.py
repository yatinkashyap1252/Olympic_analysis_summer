import streamlit as st
import helper
import plotly.express as px
import matplotlib.pylab as plt
import seaborn as sns

def overall_analysis(df):
    # Calculate key statistics
    edition = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    
    # print(f"Edition: {edition}, Cities: {cities}, Sports: {sports}, Events: {events}, Athletes: {athletes}, Nations: {nations}")

    # Page Title
    st.title(" Overall Olympic Analysis")
    # st.markdown("###  **Olympic Games Overview**")

    # Custom CSS for Card Styling
    st.markdown("""
        <style>
            .card {
                background-color: #ffffff4d;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
                font-size: 15px;
                margin: 10px;
            }
            .metric {
                font-size: 44px;
                color: #fff;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create a Card Layout using st.columns()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card"> Editions <br> <span class="metric">{}</span></div>'.format(edition), unsafe_allow_html=True)
        st.markdown('<div class="card"> Sports <br> <span class="metric">{}</span></div>'.format(sports), unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card"> Cities <br> <span class="metric">{}</span></div>'.format(cities), unsafe_allow_html=True)
        st.markdown('<div class="card"> Events <br> <span class="metric">{}</span></div>'.format(events), unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card"> Athletes <br> <span class="metric">{}</span></div>'.format(athletes), unsafe_allow_html=True)
        st.markdown('<div class="card"> Nations <br> <span class="metric">{}</span></div>'.format(nations), unsafe_allow_html=True)
        
    nation_over_time=helper.data_over_time(df,'region','No of Countries')
    st.markdown("""
        <style>
            .vertical-margin {
                padding: 10px 0;  /* Adds vertical spacing */
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="vertical-margin"></div>', unsafe_allow_html=True)
    st.header("Number of Participating Nations Over Time")
    fig = px.line(nation_over_time, x="Edition", y="No of Countries")
    st.plotly_chart(fig)
    
    event_over_time=helper.data_over_time(df,'Event', 'No of Countries')
    st.markdown("""
        <style>
            .vertical-margin {
                padding: 10px 0;  /* Adds vertical spacing */
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="vertical-margin"></div>', unsafe_allow_html=True)
    st.header("Number of Events Over Time")
    fig = px.line(event_over_time, x="Edition", y="No of Countries")
    st.plotly_chart(fig)

    sport_over_time=helper.data_over_time(df,'Sport', 'No of Countries')
    st.markdown("""
        <style>
            .vertical-margin {
                padding: 10px 0;  /* Adds vertical spacing */
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="vertical-margin"></div>', unsafe_allow_html=True)
    st.header("Number of Sports Over Time")
    fig = px.line(sport_over_time, x="Edition", y="No of Countries")
    st.plotly_chart(fig)
    
    athlete_over_time=helper.data_over_time(df,'Name', 'No of Athletes')
    st.markdown("""
        <style>
            .vertical-margin {
                padding: 10px 0;  /* Adds vertical spacing */
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="vertical-margin"></div>', unsafe_allow_html=True)
    st.header("Number of Athletes Over Time")
    fig = px.line(athlete_over_time, x="Edition", y="No of Athletes")
    st.plotly_chart(fig)
    
    st.header("Most Successful Countries Over Time")

    country_medals = df.dropna(subset=['Medal']).groupby(['Year', 'region'])['Medal'].count().reset_index()
    fig = px.choropleth(country_medals, locations="region", locationmode="country names", 
                        color="Medal", hover_name="region", animation_frame="Year",
                        title="Country Medal Distribution Over Time",
                        color_continuous_scale=px.colors.sequential.Plasma)

    st.plotly_chart(fig)
    
    st.header("👨‍👩‍👧‍👦 Gender Participation Over Time")

    # Create gender participation dataset
    gender_over_time = df.groupby(['Year', 'Sex'])['Name'].count().reset_index()
    gender_over_time.rename(columns={'Name': 'Count'}, inplace=True)

    # Default Graph (Both Male & Female)
    fig_both = px.line(gender_over_time, x="Year", y="Count", color="Sex", 
                    markers=True, title="Male vs Female Participation Over the Years",
                    color_discrete_map={'M': 'blue', 'F': 'red'})

    # st.plotly_chart(fig_both, key="both_graph")  # Assigning a unique key

    # ------------------------------
    # User Selection for More Graphs
    # ------------------------------
    st.markdown("### Customize the Graph")
    gender_option = st.radio(
        "📌 **Select a Visualization**",
        ["📈 Male Participation", "📉 Female Participation", "📊 Both (Male & Female)", "🌍 Choropleth Map"],
        index=2  # Default to 'Both'
    )

    # ------------------------------
    # 1️⃣ Male Participation Only (Line Graph)
    # ------------------------------
    if gender_option == "📈 Male Participation":
        male_data = gender_over_time[gender_over_time["Sex"] == "M"]
        fig_male = px.line(male_data, x="Year", y="Count", markers=True,
                        title="📈 Male Participation Over the Years",
                        line_shape="linear", color_discrete_sequence=['blue'])
        st.plotly_chart(fig_male, key="male_graph")  # Assigning a unique key

    # ------------------------------
    # 2️⃣ Female Participation Only (Line Graph)
    # ------------------------------
    elif gender_option == "📉 Female Participation":
        female_data = gender_over_time[gender_over_time["Sex"] == "F"]
        fig_female = px.line(female_data, x="Year", y="Count", markers=True,
                            title="📉 Female Participation Over the Years",
                            line_shape="linear", color_discrete_sequence=['red'])
        st.plotly_chart(fig_female, key="female_graph")  # Assigning a unique key

    # ------------------------------
    # 3️⃣ Both Male & Female (Default)
    # ------------------------------
    elif gender_option == "📊 Both (Male & Female)":
        st.plotly_chart(fig_both, key="both_graph_again")  # Assigning a different key

    # ------------------------------
    # 4️⃣ Choropleth Map (Geographical Distribution of Gender Participation)
    # ------------------------------
    elif gender_option == "🌍 Choropleth Map":
        st.header("🌍 Global Gender Participation Over Time")

        # Prepare Data for Choropleth
        gender_map_data = df.groupby(['Year', 'region', 'Sex'])['Name'].count().reset_index()
        gender_map_data.rename(columns={'Name': 'Count'}, inplace=True)

        # Plot Choropleth Map
        fig_choropleth = px.choropleth(
            gender_map_data, locations="region", locationmode="country names",
            color="Count", hover_name="region", animation_frame="Year",
            facet_col="Sex", title="🌍 Global Male & Female Participation Over Time",
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_choropleth, key="choropleth_map")  # Assigning a unique key
        
    st.header("Sport-wise Athlete Participation")

    sport_count = df.groupby('Sport')['Name'].nunique().reset_index()
    sport_count = sport_count.sort_values('Name', ascending=False).head(10)  # Top 10 sports

    fig = px.bar(sport_count, x='Name', y='Sport', orientation='h', 
                title="Top 10 Sports with Most Athletes", 
                labels={'Name': 'Number of Athletes', 'Sport': 'Sport'},
                color='Name', color_continuous_scale='Bluered')

    st.plotly_chart(fig)    
    
    st.header("Top Medal-Winning Athletes")

    # Prepare Data
    top_athletes = df[df['Medal'].notna()].groupby(['Name', 'Sport', 'region'])['Medal'].count().reset_index()
    top_athletes = top_athletes.sort_values('Medal', ascending=False).head(10)

    # Display Table
    # st.dataframe(top_athletes.style.format({'Medal': '{}🏅'}))

    # Bar Graph Visualization
    st.subheader("Top 10 Athletes with the Most Medals")

    fig = px.bar(
        top_athletes, x="Medal", y="Name", color="Sport",
        orientation='h',  # Horizontal Bar Chart
        text="Medal", 
        labels={"Medal": "Total Medals", "Name": "Athlete"},
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    # Improve layout
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))  # Sort by medal count

    st.plotly_chart(fig, use_container_width=True)  # Display chart
    
    st.title("No of Events over time(Every Sport):")
    
    x=df.drop_duplicates(['Year','Sport','Event'])
    
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)