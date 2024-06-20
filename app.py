import datetime
import haversine
from haversine import Unit
from sklearn.linear_model import LinearRegression
import pickle
import streamlit as st
with open('my_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)


st.title("Cab Fare Prediction Model")

col1, col2 = st.columns(2)

with col1:
    pickup_latitude = st.number_input(
        "Pickup Latitude", min_value=40.48, max_value=40.91)
    submit_button = st.button("Enter Pickup Latitude")
with col2:
    pickup_longitude = st.number_input(
        "Pickup Longitude", min_value=-74.02, max_value=-73.77)
    submit_button = st.button("Enter Pickup Longitude")


col3, col4 = st.columns(2)
with col3:
    dropoff_latitude = st.number_input(
        "Dropoff Latitude", max_value=40.91, min_value=40.49)
    submit_button = st.button("Enter Dropoff Latitude")

with col4:
    dropoff_longitude = st.number_input(
        "Dropoff Longitude", min_value=-74.03, max_value=-73.77)
    submit_button = st.button("Enter Dropoff Longitude")

passenger_count = st.number_input(
    "Number of Passengers", min_value=0, max_value=6)
submit_button = st.button("Enter Number of Passengers")


if (st.button('\nPredict Fare')):
    pickup_coords = (pickup_latitude, pickup_longitude)
    dropoff_coords = (dropoff_latitude, dropoff_longitude)
    haversine_distance = haversine.haversine(
        pickup_coords, dropoff_coords, unit=Unit.KILOMETERS)

    now = datetime.datetime.now()

    year = now.year
    month = now.month
    week_number, _, day_of_week = now.isocalendar()
    week_number = week_number
    year, week_number, _ = now.isocalendar()
    day_of_year = now.timetuple().tm_yday
    day_of_month = now.day
    day_of_week = day_of_week
    hour = now.hour
    minute = now.minute
    second = now.second
    year = year-2000

    data = [pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count,
            haversine_distance, year, month, week_number, day_of_year, day_of_month, day_of_week, hour, minute, second]
    fare = loaded_model.predict([data])
    st.text(f"Fare Estimate: {fare[0][0].round(2)} $")

image_paths = [r'PLOTS/Pickup Plot of Pickup Latitude vs Pickup Longitude.png',
               r'PLOTS/Dropoff Plot of Dropoff Latitude vs Dropoff Longitude.png',
               r'PLOTS/Distribution of Pickup(Green) & Dropoff(Blue) Coordinates on New York Map.png',
               r'PLOTS/Fare Amount Distribution.png',
               r'PLOTS/Haversine Distance Count Distribution.png',
               r'PLOTS/Passenger Count Frequency.png',
               r'PLOTS/Fare Variation with Passengers in the Cab.png',
               r'PLOTS/Correlation Heatmap.png',
               r'PLOTS/Fare Variation over the Years.png',
               r'PLOTS/Fare Variation over the Months of the Year.png',
               r'PLOTS/Fare Variation over the Days of the Month.png',
               r'PLOTS/Number of Rides over the Hours of the Day.png',
               r'PLOTS/Fare Variation over Hours of the Day.png',
               r'PLOTS/Mean Fare Amount Variation over different Timeframes.png',
               r'PLOTS/Haversine Distance variation over different TimeFrames.png',
               r'PLOTS/Fare per Km Variation over different Timeframes.png',
               r'PLOTS/Fare Variation with Haversine Distance.png',
               r'PLOTS/Average Fare Price variation with Number of Passengers.png']

image_texts = [
    "Pickup Plot of Pickup Latitude vs Pickup Longitude",
    "Dropoff Plot of Dropoff Latitude vs Dropoff Longitude",
    "Distribution of Pickup(Green) & Dropoff(Blue) Coordinates on New York Map",
    "Fare Amount Distribution",
    "Haversine Distance Count Distribution",
    "Passenger Count Frequency",
    "Fare Variation with Passengers in the Cab",
    "Correlation Heatmap",
    "Fare Variation over the Years",
    "Fare Variation over the Months of the Year",
    "Fare Variation over the Days of the Month",
    "Number of Rides over the Hours of the Day",
    "Fare Variation over Hours of the Day",
    "Mean Fare Amount Variation over different Timeframes",
    "Haversine Distance variation over different TimeFrames",
    "Fare per Km Variation over different Timeframes",
    "Fare Variation with Haversine Distance",
    "Average Fare Price variation with Number of Passengers"
]


if 'image_visibility' not in st.session_state:
    st.session_state['image_visibility'] = [False] * 18


def toggle_image_visibility(index):
    # Update only the clicked image's visibility
    image_visibility = st.session_state['image_visibility']
    image_visibility[index] = not image_visibility[index]
    # Update session state
    st.session_state['image_visibility'] = image_visibility
    st.experimental_rerun()


st.title("Meaningful Observations expressed via Graphs")

pdf_download_link = "https://drive.google.com/file/d/1ZWLHgk2oXHoCS0rPXTWcd0nF2awMprJ0/view?usp=drive_link"
st.link_button("Download PDF of the Analysis", pdf_download_link)

style = "<style>.row-widget.stButton {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)

for i, image_path in enumerate(image_paths):
    with st.container():

        if st.session_state['image_visibility'][i]:
            show_hide_text = f"Hide Plot {i+1}"
        else:
            show_hide_text = f"Show Plot {i+1}"

        if st.session_state['image_visibility'][i]:
            st.image(image_path, caption=image_texts[i])

        show_hide_button = st.button(show_hide_text, key=i)

        if show_hide_button:
            toggle_image_visibility(i)


st.write('<div style="text-align: center; font-size: 12px;">Made with ❤️ by HRG</div>',
         unsafe_allow_html=True)
