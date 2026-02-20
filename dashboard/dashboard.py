import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(
    page_title="Bike Rental Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Data Loading & Preprocessing
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/all_data.csv')
    df['record_date'] = pd.to_datetime(df['record_date'])
    df['weather_status'] = df['weather_status'].replace({
        1: 'Clear/Partly Cloudy',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Ice Pallets'
    })
    return df

data = load_data()

# Sidebar Navigation & Filters
st.sidebar.header("Dashboard Filter")
min_date = data["record_date"].min()
max_date = data["record_date"].max()

# Handle the date range selection properly
date_range = st.sidebar.date_input(
    label='Date Range',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Only proceed if the user has selected both a start and end date
if len(date_range) == 2:
    start_date, end_date = date_range
    
    # Filter the data
    main_df = data[(data["record_date"] >= pd.to_datetime(start_date)) & 
                    (data["record_date"] <= pd.to_datetime(end_date))]

    if not main_df.empty:
        # Main Dashboard Header
        st.title('🚲 Bike Rental Dashboard')
        st.markdown("Analyzing bike sharing trends across different weather conditions and seasons.")

        # Top Metrics (KPIs)
        col1, col2, col3 = st.columns(3)
        with col1:
            total_rentals = main_df['total_rentals'].sum()
            st.metric('Total Rentals', f"{total_rentals:,}")

        with col2:
            avg_rentals = round(main_df['total_rentals'].mean(), 2)
            st.metric('Avg Daily Rentals', avg_rentals)

        with col3:
            peak_weather = main_df['weather_status'].mode()[0]
            st.metric('Most Frequent Weather', peak_weather)

        st.divider()

        # Visualizations Section
        row1_col1, row1_col2 = st.columns([2, 1])

        with row1_col1:
            st.subheader("📈 Monthly Rental Trends")
            # Use 'ME' instead of 'M' to avoid FutureWarning
            monthly_rentals = main_df.resample(rule='ME', on='record_date').sum(numeric_only=True)
            
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(monthly_rentals.index, monthly_rentals['total_rentals'], marker='o', linewidth=2, color='#3970F1')
            ax.set_title("Total Bike Rentals per Month", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig)

        with row1_col2:
            st.subheader("🏖️ Holiday Impact")
            holiday_comparison = main_df.groupby('holiday')['total_rentals'].sum()
            
            # Dynamic Labels for Pie Chart
            # Map the index values (0, 1) to readable names
            label_map = {0: 'Working Day', 1: 'Holiday'}
            current_labels = [label_map[i] for i in holiday_comparison.index]
            
            fig, ax = plt.subplots(figsize=(6, 6))
            colors = ['#8fd9b6', '#ff9999']
            ax.pie(holiday_comparison, labels=current_labels, autopct='%1.1f%%', 
                startangle=90, colors=colors[:len(current_labels)], wedgeprops={'edgecolor': 'white'})
            st.pyplot(fig)

        st.divider()

        # Weather & Temperature Analysis
        st.subheader("🌦️ Weather & Temperature Relationship")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.scatterplot(
            data=main_df, 
            x='temp', 
            y='total_rentals', 
            hue='weather_status', 
            palette='viridis', 
            alpha=0.7,
            ax=ax
        )
        ax.set_title('Rentals vs Temperature by Weather Condition', fontsize=12)
        ax.set_xlabel('Normalized Temperature')
        ax.set_ylabel('Total Bike Rentals')
        st.pyplot(fig)

        # Footer
        st.caption("Copyright © 2026 | BikeShare Analytics Project")
    else:
        st.warning("⚠️ No data for the selected time range.")
else:
    # This shows while the user is still picking their second date
    st.info("Please select the start date and end date on the sidebar.")