import streamlit as st
import preprocessor
import helper
import overall_analysis
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import country_wise_analysis
import plotly.figure_factory as ff

# Load datasets
df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

# Preprocess data
df = preprocessor.preprocess(df, region_df)

# ---- SIDEBAR ----
st.sidebar.title(" Olympic Data Analysis")
# st.sidebar.markdown("📊 **Explore Olympic data interactively!**")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/2560px-Olympic_rings_without_rims.svg.png", width=200)

choice = st.sidebar.radio(" **Select an Option**", 
                          (" Medal Tally", " Overall Analysis", " Country-wise Analysis", " Athlete-wise Analysis"))

st.sidebar.markdown("---")
st.sidebar.write("⚡ Developed by : **Yatin Kashyap**")

# # ---- MAIN CONTENT ----
# st.title("📊 Olympic Games Analysis Dashboard")

if choice == ' Medal Tally':
    st.title(" Medal Tally Overview")

    country, years = helper.country_year_list(df)
    
    # Apply vertical margins using st.markdown() with CSS
    st.markdown("""
        <style>
            .vertical-margin {
                padding: 10px 0;  /* Adds vertical spacing */
            }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="vertical-margin"></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            selected_year = st.select_slider("📅 Select Year", years)

        with col2:
            selected_country = st.selectbox("🌍 Select Country", country)

        st.markdown('<div class="vertical-margin"></div>', unsafe_allow_html=True)

    # Fetch medal tally
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    if selected_year == "Overall" and selected_country == "Overall":
        st.markdown(f"###  Overall Medal Tally")
    elif selected_year == "Overall" and selected_country!="Overall":
        st.markdown(f"###  Overall Medal Tally for {selected_country}")
    elif selected_year != "Overall" and selected_country == "Overall":
        st.markdown(f"###  Overall Medal Tally for {selected_year}")
    else:
        st.markdown(f"###  Medal Tally for {selected_year} in {selected_country}")

    # Display Results
    if medal_tally.empty:
        st.warning("🚨 No data available for the selected filters.")
    else:
        st.dataframe(medal_tally.style.format({"Gold": "{}", "Silver": "{}", "Bronze": "{}", "Total": "{}🏅"}))

    st.markdown("---")
    st.info("🔍 **Tip:** Select a year & country to filter the medal tally!")
elif choice == " Overall Analysis":
    overall_analysis.overall_analysis(df)
elif choice == " Country-wise Analysis":
    st.title("Country-wise Analysis")
    
    countries=helper.country_year_list(df)[0]
    country_choice=st.sidebar.selectbox("Select Country",countries)
    
    if country_choice=="Overall":
        st.warning("Please select a country to view the analysis.")
    else:
        country_wise_analysis.country_wise_analysis(df,country_choice)
        country_wise_analysis.country_sport_heatmap(df,country_choice)
        country_wise_analysis.most_successful_athlete(df,country_choice)
    
elif choice == " Athlete-wise Analysis":
    st.title("Athlete-wise Analysis")

    # Drop duplicate athlete-region pairs
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Create age data groups
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    # Create the distribution plot
    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        group_labels=['Overall Age', 'Gold Medal', 'Silver Medal', 'Bronze Medal'],
        show_hist=False,
        show_rug=False
    )

    # Customize layout and traces
    fig.update_layout(
        title_text='Age Distribution of Athletes',
        title_x=0.5,
        xaxis_title="Age",
        yaxis_title="Density",
        template="plotly_dark",
        legend_title_text='Medal Type'
    )

    # Optional: Add marker edge (applies to histograms, not KDE)
    # fig.update_traces(marker=dict(line=dict(width=2, color='black')))

    # Show the chart
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🏅 Age Distribution of Gold Medalists by Sport")

    # Filter only gold medal winners with valid age and sport
    gold_df = df[(df['Medal'] == 'Gold') & (df['Age'].notna()) & (df['Sport'].notna())]

    # Select top N sports with most gold medals for clarity (e.g., top 6)
    top_sports = gold_df['Sport'].value_counts().head(6).index.tolist()
    
    # Prepare data and labels
    age_data = []
    sport_labels = []

    for sport in top_sports:
        sport_ages = gold_df[gold_df['Sport'] == sport]['Age']
        if not sport_ages.empty:
            age_data.append(sport_ages)
            sport_labels.append(sport)

    # Plot
    fig = ff.create_distplot(
        age_data,
        group_labels=sport_labels,
        show_hist=False,
        show_rug=False
    )

    fig.update_layout(
        title="Distribution of Ages for Gold Medalists by Sport",
        title_x=0.5,
        xaxis_title="Age",
        yaxis_title="Density",
        template="plotly_dark",
        legend_title_text="Sports"
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Filter data for Gold medalists with weight info
    gold_medalists = df[(df['Medal'] == 'Gold') & (df['Sex'].notna()) & (df['Weight'].notna())]

    # Define weight categories (customize as needed)
    def weight_category(weight):
        if weight < 60:
            return 'Lightweight (<60kg)'
        elif 60 <= weight <= 75:
            return 'Middleweight (60–75kg)'
        else:
            return 'Heavyweight (>75kg)'

    gold_medalists['Weight Category'] = gold_medalists['Weight'].apply(weight_category)

    # Let user select a weight category to view gender split
    selected_category = st.sidebar.selectbox(
        "Select Weight Category",
        gold_medalists['Weight Category'].unique()
    )

    # Filter by selected weight category
    filtered = gold_medalists[gold_medalists['Weight Category'] == selected_category]

    # Count Male vs Female
    gender_counts = filtered['Sex'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    gender_counts['Gender'] = gender_counts['Gender'].map({'M': 'Male', 'F': 'Female'})

    # Plot pie chart
    fig = px.pie(gender_counts,
                names='Gender',
                values='Count',
                title=f"🥇 Gender Distribution in {selected_category}",
                color='Gender',
                color_discrete_map={'Male': 'royalblue', 'Female': 'deeppink'})

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)

    # Display
    st.plotly_chart(fig, use_container_width=True)
    
    selected_sport=st.sidebar.selectbox("Select Sport", df['Sport'].unique())
    st.subheader(f"🏋️‍♂️ Height & Weight Analysis for {selected_sport}")
    helper.height_weight_analysis(df,selected_sport)

    st.markdown("---")
    st.info("🔍 Tip: This overview provides a high-level summary of Olympic history!")