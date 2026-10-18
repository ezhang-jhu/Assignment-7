import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Map Pin App")

lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0,
                      value=39.2904, step=0.5, format="%.4f")
lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0,
                      value=-76.6122, step=0.5, format="%.4f")

m = folium.Map(location=[lat, lon], zoom_start=6)

folium.Marker(
    [lat, lon],
    tooltip=f"Lat {lat}, Lon {lon}",
    icon=folium.Icon(color="red"),
).add_to(m)

st_folium(m, width=700, height=450)