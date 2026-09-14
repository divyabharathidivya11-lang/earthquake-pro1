import streamlit as st
import earthquake_sql

# Page title
st.set_page_config(
    page_title="Global Seismic Trends",
    page_icon="\U0001F30D",
    layout="wide"
)

# Query 1
#st.header("1. Top 10 Strongest Earthquakes mag")
#st.dataframe(earthquake_sql.result, use_container_width=True)

# Main title
st.title("\U0001F30D Global Seismic Trends Data-Driven Earthquake Insights")
#st.subheader("Data-Driven Earthquake Insights")
# Sidebar
st.sidebar.title("\U0001F4CA Analysis Categories")

categories = {
    "Magnitude & Depth": {
        "Top 10 strongest earthquakes": "result",
        "Top 10 deepest earthquakes": "result1",
        "Shallow earthquakes below 50 km and magnitude above 7.5": "result3",
        "Average magnitude by magnitude type": "result4"
    },

    "Time Analysis": {
        "Year with most earthquakes": "result5",
        "Month with highest number of earthquakes": "result6",
        "Day of week with most earthquakes": "result7",
        "Earthquake count by hour": "result8"
    },

    "Casualties & Economic Loss": {
        "Top 5 places with highest felt reports": "result10",
        "Earthquake count by alert level": "result11"
    },

    "Event Type & Quality Metrics": {
        "Reviewed vs automatic earthquakes": "result12",
        "Count by earthquake type": "result13",
        "Number of earthquakes by data types": "result14",
        "Events with high station coverage": "result15"
    },

    "Tsunamis & Alerts": {
        "Number of tsunamis per year": "result16",
        "Count of earthquakes by alert level": "result17"
    },

    "Seismic Pattern & Trends Analysis": {
        "Top 5 countries by average magnitude": "result18",
        "Countries with shallow and deep earthquakes in the same month": "result19",
        "Year-over-year earthquake growth rate": "result20",
        "Top 3 seismically active regions": "result21"
    },

    "Depth, Location & Distance-Based Analysis": {
        "Average depth near the equator": "result22",
        "Highest shallow-to-deep earthquake ratio": "result23",
        "Magnitude difference: tsunami vs non-tsunami": "result24",
        "Events with high gap and RMS values": "result25",
        "Regions with the most deep-focus earthquakes": "result26"
    }
}

# First dropdown: category
selected_category = st.sidebar.selectbox(
    "Select analysis category",
    list(categories.keys())
)

# question dropdown: question
selected_question = st.selectbox(
    "Select question",
    list(categories[selected_category].keys())
)

# Get the  result variable name
result_variable = categories[selected_category][selected_question]

# Get the DataFrame from earthquake_sql.py
result_df = getattr(earthquake_sql, result_variable)

# Display the selected question
#st.header(selected_question)

# Display result
st.dataframe(result_df, use_container_width=True)

# Display a chart for selected results
if selected_question == "Year with most earthquakes":
    st.bar_chart(
        result_df.set_index("year")["earthquake_count"]
    )

elif selected_question == "Month with highest number of earthquakes":
    st.bar_chart(
        result_df.set_index("month")["earthquake_count"]
    )

elif selected_question == "Number of tsunamis per year":
    st.bar_chart(
        result_df.set_index("year")["eathquake_count_tunami"]
    )