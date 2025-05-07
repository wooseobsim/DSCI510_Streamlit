import streamlit as st
import pandas as pd
import plotly.express as px

# Load the integrated dataset
@st.cache_data
def load_data():
    return pd.read_csv("final_dataset_language_sentiment_national.csv")

df = load_data()

# Sidebar filter
st.sidebar.title("Language and State Filters")
states = st.sidebar.multiselect("Select State(s):", sorted(df["State"].dropna().unique()))
languages = st.sidebar.multiselect("Select Language(s):", sorted(df["Language"].dropna().unique()))

# Filtered dataset
filtered_df = df.copy()
if states:
    filtered_df = filtered_df[filtered_df["State"].isin(states)]
if languages:
    filtered_df = filtered_df[filtered_df["Language"].isin(languages)]

st.title("🗺️ Multilingual Trends Across U.S. States")

st.markdown("This dashboard presents insights from U.S. Census data, Reddit discussions, and web localization demand, focused on languages spoken across American states.")

# Top bar charts
st.subheader("Top Languages by ACS Speakers")
acs_chart = filtered_df.groupby("Language")["ACS_Speakers"].sum().nlargest(10).reset_index()
fig_acs = px.bar(acs_chart, x="Language", y="ACS_Speakers", title="Top 10 Languages by ACS Speakers")
st.plotly_chart(fig_acs)

st.subheader("Top Languages by Reddit Mentions")
reddit_chart = filtered_df.groupby("Language")["Reddit_Mentions"].sum().nlargest(10).reset_index()
fig_reddit = px.bar(reddit_chart, x="Language", y="Reddit_Mentions", title="Top 10 Languages Mentioned on Reddit")
st.plotly_chart(fig_reddit)

st.subheader("Average Sentiment by Language (Reddit)")
sentiment_chart = filtered_df.groupby("Language")["Avg_Sentiment"].mean().sort_values(ascending=False).head(10).reset_index()
fig_sentiment = px.bar(sentiment_chart, x="Language", y="Avg_Sentiment", title="Most Positive Languages by Sentiment")
st.plotly_chart(fig_sentiment)

# State-wise Language Table
st.subheader("Detailed Table of Selected Data")
st.dataframe(filtered_df.sort_values(by=["State", "Language"]))


# Interactive Map with Clickable States
st.subheader("🌍 Interactive Map: Top 5 Languages by State")

# Create a choropleth map of total language speakers by state
state_summary = df.groupby("State").agg(
    Total_Speakers=("ACS_Speakers", "sum")
).reset_index()




# Fill NaN values and format the State column
df['LEP_Speakers'].fillna(0, inplace=True)
df['ACS_Speakers'].fillna(0, inplace=True)
df['Reddit_Mentions'].fillna(0, inplace=True)
df['Avg_Sentiment'].fillna(0, inplace=True)
df['State'] = df['State'].str.title()

# Aggregate data to get total speakers per state for map visualization
state_totals = df.groupby('State').agg(Total_Speakers=('ACS_Speakers', 'sum')).reset_index()

st.title("Total Language Speakers by State")

# Interactive map
fig = px.choropleth(state_totals,
                    locations="State",
                    locationmode="USA-states",
                    color="Total_Speakers",
                    hover_name="State",
                    scope="usa",
                    color_continuous_scale="Blues",
                    title="Total Language Speakers by State")

st.plotly_chart(fig)

# User can click on a state to view top 5 languages
selected_state = st.selectbox("Select a State to view top 5 languages:", state_totals['State'].unique())

if selected_state:
    top_languages = df[df['State'] == selected_state].nlargest(5, 'ACS_Speakers')
    st.write(f"Top 5 languages in {selected_state}:")
    st.write(top_languages[['Language', 'ACS_Speakers']])