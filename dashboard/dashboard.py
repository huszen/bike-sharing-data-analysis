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
    # Pastikan path file sesuai dengan struktur folder kamu
    df = pd.read_csv('dashboard/all_data.csv')
    df['record_date'] = pd.to_datetime(df['record_date'])
    
    # Menambahkan kolom pendukung untuk visualisasi baru
    df['year'] = df['record_date'].dt.year
    df['day_type'] = df['workingday'].map({1: 'Weekday', 0: 'Weekends'})
    
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

date_range = st.sidebar.date_input(
    label='Date Range',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

if len(date_range) == 2:
    start_date, end_date = date_range
    
    # Filter data berdasarkan range tanggal
    main_df = data[(data["record_date"] >= pd.to_datetime(start_date)) & 
                    (data["record_date"] <= pd.to_datetime(end_date))]

    if not main_df.empty:
        st.title('🚲 Bike Rental Dashboard')
        st.markdown("Analyzing bike sharing trends based on day types, seasons, and weather.")

        # --- Top Metrics (KPIs) ---
        col1, col2, col3 = st.columns(3)
        with col1:
            total_rentals = main_df['total_rentals'].sum()
            st.metric('Total Rentals', f"{total_rentals:,}")
        with col2:
            avg_rentals = round(main_df['total_rentals'].mean(), 2)
            st.metric('Avg Daily Rentals', f"{avg_rentals:,}")
        with col3:
            peak_season = main_df['season'].mode()[0]
            st.metric('Top Season', peak_season.capitalize())

        st.divider()

        # --- VISUALISASI 1: Weekdays vs Weekends ---
        st.subheader("📊 Rental Comparison: Weekdays vs Weekends")
        
        # Grouping data
        workingday_rentals = main_df.groupby(['year', 'day_type'])['total_rentals'].sum().unstack()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        workingday_rentals.plot(kind='bar', color=['#ff9999','#66b3ff'], ax=ax)
        
        ax.set_title('Total Bike Rentals: Weekdays vs Weekends', fontsize=12)
        ax.set_xlabel('Year')
        ax.set_ylabel('Total Rentals')
        plt.xticks(rotation=0)

        # Menambahkan label angka di atas bar
        for container in ax.containers:
            ax.bar_label(container, fmt='{:,.0f}', padding=3)
        
        st.pyplot(fig)

        st.divider()

        # --- VISUALISASI 2: Temp vs Rentals per Season ---
        st.subheader("🌡️ Temperature & Seasonality Analysis")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        seasons = main_df['season'].unique()
        colors = {'springer': 'green', 'summer': 'orange', 'fall': 'brown', 'winter': 'blue'}

        for season in seasons:
            subset = main_df[main_df['season'] == season]
            ax.scatter(subset['temp'], subset['total_rentals'], 
                        label=season.capitalize(), 
                        color=colors.get(season, 'gray'), 
                        alpha=0.5)

        ax.set_title('Relationship between Temperature and Rentals per Season', fontsize=12)
        ax.set_xlabel('Temperature (Normalized)')
        ax.set_ylabel('Total Daily Rentals')
        ax.legend(title='Seasons')
        ax.grid(True, linestyle=':', alpha=0.6)
        
        st.pyplot(fig)

        # Footer
        st.caption(f"Copyright © 2026 | BikeShare Analytics Project | Data filtered from {start_date} to {end_date}")
    else:
        st.warning("⚠️ No data for the selected time range.")
else:
    st.info("Please select the start date and end date on the sidebar.")