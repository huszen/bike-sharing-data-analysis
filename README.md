# Dicoding Collection Dashboard ✨

## 🌐 Live Demo

The application is deployed and publicly accessible at:

🔗 **[Bike Sharing Data Analysis App](https://huszen-bike-sharing-data-analysis.streamlit.app/)**

## Setup Environment - Anaconda

```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app

```
streamlit run dashboard.py
```

## About This Data

Both day.csv and hour.csv have same column, except in day.csv does not have 'hr' column

| Column Name    | Description                                                                       |
| -------------- | --------------------------------------------------------------------------------- |
| **instant**    | A unique identifier for each record (row).                                        |
| **dteday**     | The date of the record.                                                           |
| **season**     | Season on the recorded day, represented numerically:                              |
|                | - `1` = Spring                                                                    |
|                | - `2` = Summer                                                                    |
|                | - `3` = Fall                                                                      |
|                | - `4` = Winter                                                                    |
| **yr**         | The year of the record:                                                           |
|                | - `0` = 2011                                                                      |
|                | - `1` = 2012                                                                      |
| **mnth**       | The month of the record, ranging from `1` (January) to `12` (December).           |
| **holiday**    | Indicates if the day is a holiday:                                                |
|                | - `1` = Holiday                                                                   |
|                | - `0` = Non-holiday                                                               |
| **weekday**    | Day of the week:                                                                  |
|                | - `0` = Sunday, `1` = Monday, ..., `6` = Saturday                                 |
| **workingday** | Specifies if the day is a working day:                                            |
|                | - `1` = Working day                                                               |
|                | - `0` = Weekend or holiday                                                        |
| **weathersit** | Weather condition on the day, categorized as:                                     |
|                | - `1` = Clear or partly cloudy                                                    |
|                | - `2` = Misty or cloudy                                                           |
|                | - `3` = Light rain or snow                                                        |
|                | - `4` = Heavy rain or snow                                                        |
| **temp**       | Normalized temperature in Celsius (scaled between `0` and `1`).                   |
| **atemp**      | Normalized "feels like" temperature in Celsius (also scaled between `0` and `1`). |
| **hum**        | Normalized humidity level (scaled between `0` and `1`).                           |
| **windspeed**  | Normalized wind speed (scaled between `0` and `1`).                               |
| **casual**     | Count of casual (non-registered) users who rented bikes on that day.              |
| **registered** | Count of registered users who rented bikes on that day.                           |
| **cnt**        | Total number of bike rentals on that day (sum of casual and registered users).    |
