import streamlit as st
import pandas as pd
import numpy as np
import math
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

NAVY = "#0B3D59"
NAVY_DEEP = "#082C41"
TEAL = "#1C7293"
AMBER = "#E8871E"
GREEN = "#2E9E63"
RED = "#D64545"
INK = "#1B2430"
MUTED = "#5B6B79"
OFFWHITE = "#F7F9FA"

CUSTOM_CSS = f"""
<style>
    .stApp {{
        background-color: {OFFWHITE};
    }}
    .hero-banner {{
        background: {NAVY};
        background-image: radial-gradient(circle at 85% -10%, {TEAL}55, transparent 55%);
        padding: 1.8rem 2.2rem;
        border-radius: 14px;
        margin-bottom: 1.4rem;
    }}
    .hero-title {{
        color: white;
        font-size: 2.0rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }}
    .hero-sub {{
        color: #CADCFC;
        font-size: 1.0rem;
    }}
    .kicker {{
        color: {AMBER};
        letter-spacing: 2px;
        font-weight: 700;
        font-size: 0.78rem;
        text-transform: uppercase;
    }}
    .poc-card {{
        background: white;
        border: 1px solid #E3E8EC;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
    }}
    .badge {{
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.82rem;
        color: white;
    }}
    .escalate-banner {{
        background: {RED};
        color: white;
        padding: 1rem 1.3rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 1rem;
    }}
    .ok-banner {{
        background: {GREEN};
        color: white;
        padding: 0.7rem 1.3rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }}
    .footer-note {{
        color: {MUTED};
        font-size: 0.78rem;
        margin-top: 2rem;
    }}
    div[data-testid="stMetricValue"] {{
        color: {NAVY};
    }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "trail" not in st.session_state:
    st.session_state.trail = []

if "pin" not in st.session_state:
    st.session_state.pin = None

full_df = pd.read_csv("original_pin.csv", dtype={"pincode": str}, low_memory=False)
full_df['pincode'] = full_df['pincode'].astype(str)

area_df = pd.read_csv("pincode_centroids_sorted.csv", dtype={"Pincode": str}, low_memory=False)
area_df['Pincode'] = area_df['Pincode'].astype(str)

po_df = pd.read_csv("cleaned_pincode_lat_long.csv", dtype={"Pincode": str}, low_memory=False)
po_df['Pincode'] = po_df['Pincode'].astype(str)

def show_pin_details(pin: str):
    global full_df
    try:
        # Filter for the requested pin
        pin_info = full_df[full_df['pincode'] == pin].iloc[0]
        district = str(pin_info['district'])
        state = str(pin_info['statename'])
        # print(district, state)
        if district == "nan":
            district = "Unknown District"
        if state == "nan":
            state = "Unknown State"

        # Display with title casing
        # st.success(f"District: {district.title()}")
        # st.success(f"State: {state.title()}")
        return (f"({district.title()}, {state.title()})")
        
    except Exception as e:
        return (f"(Unknown District), Unknown State)")
    
def show_pin_dist(ref: str, pin: str, flag):
    global area_df, po_df
    full_df = pd.DataFrame()
    if flag:
        full_df = po_df.copy()
    else:
        full_df = area_df.copy()
    try:
        # Filter for the requested pin
        ref_info = full_df[full_df['Pincode'] == ref].iloc[0]
        ref_lat = np.float64(ref_info['Latitude'])
        ref_long = np.float64(ref_info['Longitude'])

        pin_info = full_df[full_df['Pincode'] == pin].iloc[0]
        pin_lat = np.float64(pin_info['Latitude'])
        pin_long = np.float64(pin_info['Longitude'])

        # st.success(ref_lat, ref_long, pin_lat, pin_long)

        return haversine_distance(ref_lat, ref_long, pin_lat, pin_long)

    except Exception as e:
        return 0

def show_pin_dir(ref: str, pin: str, flag):
    global area_df, po_df
    full_df = pd.DataFrame()
    if flag:
        full_df = po_df.copy()
    else:
        full_df = area_df.copy()
    try:
        # Filter for the requested pin
        ref_info = full_df[full_df['Pincode'] == ref].iloc[0]
        ref_lat = np.float64(ref_info['Latitude'])
        ref_long = np.float64(ref_info['Longitude'])

        pin_info = full_df[full_df['Pincode'] == pin].iloc[0]
        pin_lat = np.float64(pin_info['Latitude'])
        pin_long = np.float64(pin_info['Longitude'])

        # st.success(ref_lat, ref_long, pin_lat, pin_long)

        if (ref_lat > pin_lat) and (ref_long > pin_long):
            return "South-West"
        elif (ref_lat > pin_lat) and (ref_long < pin_long):
            return "South-East"
        elif (ref_lat < pin_lat) and (ref_long > pin_long):
            return "North-West"
        elif (ref_lat < pin_lat) and (ref_long < pin_long):
            return "North-East"
        elif (ref_lat > pin_lat) and (ref_long == pin_long):
            return "South"
        elif (ref_lat == pin_lat) and (ref_long < pin_long):
            return "East"
        elif (ref_lat < pin_lat) and (ref_long == pin_long):
            return "North"
        elif (ref_lat == pin_lat) and (ref_long > pin_long):
            return "West"
        else: 
            return "Same"

    except Exception as e:
        return 0


# === Haversine Distance Function ===
def haversine_distance(lat1, lon1, lat2, lon2, earth_radius=6371):
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius * c


# === Sort Pincodes by Distance ===
def sort_pins(pin: str, pin_list, flag):
    global area_df, po_df
    if pin_list == []:
        return pin_list
    dist = []
    full_df = po_df
    if flag:
        full_df = area_df
    ref_info = full_df[full_df['Pincode'] == pin].iloc[0]
    ref_lat = np.float64(ref_info['Latitude'])
    ref_long = np.float64(ref_info['Longitude'])
    for i in pin_list:
        pin_info = full_df[full_df['Pincode'] == i].iloc[0]
        pin_lat = np.float64(pin_info['Latitude'])
        pin_long = np.float64(pin_info['Longitude'])
        dist.append(float(haversine_distance(ref_lat, ref_long, pin_lat, pin_long)))
    
    # Pair the lists and sort by elements of list1
    combined = list(zip(dist, pin_list))
    sorted_combined = sorted(combined)

    # Unzip the sorted pairs back into two lists
    dist, pin_list = zip(*sorted_combined)

    return pin_list


# === Distance Calculation Logic ===
def process_dataset(pin, df, flag):
    df['Pincode'] = df['Pincode'].astype(str)
    if pin not in df['Pincode'].values:
        return None, None, None, [], [], [], []
    lat = df.loc[df['Pincode'] == pin, 'Latitude'].values[0]
    lon = df.loc[df['Pincode'] == pin, 'Longitude'].values[0]
    min_dist = np.inf
    min_pin = None
    within_5km, within_10km, within_20km, within_50km = [], [], [], []
    for _, row in df.iterrows():
        current_pin = row['Pincode']
        if current_pin == pin:
            continue
        dist = haversine_distance(lat, lon, row['Latitude'], row['Longitude'])
        if dist < min_dist:
            min_dist = dist
            min_pin = current_pin
        if dist <= 5:
            within_5km.append(current_pin)
        elif dist <= 10:
            within_10km.append(current_pin)
        elif dist <= 20:
            within_20km.append(current_pin)
        elif dist <= 50:
            within_50km.append(current_pin)
    within_5km_sorted = sorted(set(within_5km))
    within_10km_sorted = sorted(set(within_10km))
    within_20km_sorted = sorted(set(within_20km))
    within_50km_sorted = sorted(set(within_50km))

    within_5km_sorted = sort_pins(pin, within_5km_sorted, flag)
    within_10km_sorted = sort_pins(pin, within_10km_sorted, flag)
    within_20km_sorted = sort_pins(pin, within_20km_sorted, flag)
    within_50km_sorted = sort_pins(pin, within_50km_sorted, flag)
    
    return min_pin, min_dist, lat, within_5km_sorted, within_10km_sorted, within_20km_sorted, within_50km_sorted


# === Map creation helper ===
def create_pincode_map(pin, df, nearest_pin, within_5km, within_10km, within_20km):
    lat = df.loc[df['Pincode'] == pin, 'Latitude'].values[0]
    lon = df.loc[df['Pincode'] == pin, 'Longitude'].values[0]
    m = folium.Map(location=[lat, lon], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)
    
    for _, row in df.iterrows():
        pincode = row['Pincode']
        plat = row['Latitude']
        plon = row['Longitude']
        if pincode == pin:
            color = 'red'
            tooltip = f"Original Pincode: {pincode} {show_pin_details(pincode)}"
            icon = 'home'
        elif pincode == nearest_pin:
            color = 'orange'
            tooltip = f"Nearest Pincode: {pincode} {show_pin_details(pincode)}"
            icon = 'star'
        elif pincode in within_5km:
            color = 'green'
            tooltip = f"Within 5 km: {pincode} {show_pin_details(pincode)}"
            icon = 'circle'
        elif pincode in within_10km:
            color = 'blue'
            tooltip = f"Within 10 km: {pincode} {show_pin_details(pincode)}"
            icon = 'circle'
        elif pincode in within_20km:
            color = 'purple'
            tooltip = f"Within 20 km: {pincode} {show_pin_details(pincode)}"
            icon = 'circle'
        elif pincode in within_50km:
            color = 'black'
            tooltip = f"Within 50 km: {pincode} {show_pin_details(pincode)}"
            icon = 'circle'
        else:
            continue  # skip others to keep map clean
        
        folium.Marker(
            location=[plat, plon],
            popup=tooltip,
            tooltip=tooltip,
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(marker_cluster)
    return m




# === Streamlit UI ===
st.set_page_config(page_title="Nearby Pincode Comparator", layout="wide", page_icon="📍")
# st.title("📍 Nearby Pincode Comparator")
# st.markdown("Compare nearby pincodes based on 📌 **Area Centroids** vs 🏤 **Post Office Locations**.")

st.markdown(
    f"""
    <div class="hero-banner">
        <div class="kicker">Pin Code \u00b7 Area Analysis</div>
        <div class="hero-title">📍 Nearby Pincode Comparator</div>
        <div class="hero-sub">Compare nearby pincodes based on 📌 **Area Centroids** vs 🏤 **Post Office Locations**.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "last_pin" not in st.session_state:
    st.session_state.last_pin = None

# Input field
st.session_state.pin = st.text_input("🔢 Enter a valid Indian Pincode:")

# Run check only when pin changes
if st.session_state.pin != st.session_state.last_pin:
    if st.session_state.pin != "": # ignore empty input
        if st.session_state.pin not in st.session_state.trail:
            st.session_state.trail.append(st.session_state.pin)
            # st.session_state.trail = sorted(st.session_state.trail)
        else:
            st.toast("The Pin Already Exists Within Trail.")
    else:
        st.session_state.trail = []

    # Update last_pin so this block won't run again until pin changes
    st.session_state.last_pin = st.session_state.pin


if st.session_state.pin:
    pin = st.session_state.pin
    org_pin = pin
    df_centroids = pd.read_csv("pincode_centroids_sorted.csv")
    df_cleaned = pd.read_csv("cleaned_pincode_lat_long.csv")
    full_df = pd.read_csv("original_pin.csv", dtype={"pincode": str}, low_memory=False)

    progress = st.progress(0)
    progress.progress(30)
    area_nearest, area_dist, area_lat, area_5km, area_10km, area_20km, area_50km = process_dataset(pin, df_centroids, True)
    progress.progress(60)
    po_nearest, po_dist, po_lat, po_5km, po_10km, po_20km, po_50km = process_dataset(pin, df_cleaned, False)
    progress.progress(100)

    if area_nearest is None or po_nearest is None:
        st.error("❌ Pincode not found in either of the datasets. Please enter valid pincode.")
        st.session_state.trail.remove(pin)
        st.warning(f"Trail: {' → '.join(st.session_state.trail)}")
    else:
        st.warning(f"Trail: {' → '.join(st.session_state.trail)}")
        st.success("✅ Data processed successfully!")
        full_df['pincode'] = full_df['pincode'].astype(str)

        pin_info = full_df[full_df['pincode'] == pin].iloc[0]
        district = pin_info['district']
        state = pin_info['statename']
        st.success(f"District: {district.title()}")
        st.success(f"State: {state.title()}")
        # st.toast(show_pin_details(pin))

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 Area-Based (Centroids)")
            st.metric("Nearest Pincode", f"{area_nearest} {show_pin_details(area_nearest)}", f"{area_dist:.2f} km {show_pin_dir(org_pin, area_nearest, False)}")
            st.markdown("**Pincodes within 5 km:**")
            df_5km_area = pd.DataFrame({
                "Pincode": [f"{pin} {show_pin_details(pin)}   \u2191 {show_pin_dist(org_pin, pin, False):.2f} km {show_pin_dir(org_pin, pin, False)}" for pin in area_5km]
            })
            df_5km_area.index = df_5km_area.index + 1
            st.dataframe(df_5km_area, use_container_width=True)

            st.markdown("**Pincodes within 10 km:**")
            df_10km_area = pd.DataFrame({
                "Pincode": [f"{pin} {show_pin_details(pin)}   \u2191 {show_pin_dist(org_pin, pin, False):.2f} km {show_pin_dir(org_pin, pin, False)}" for pin in area_10km]
            })
            df_10km_area.index = df_10km_area.index + 1
            st.dataframe(df_10km_area, use_container_width=True)

            st.markdown("**Pincodes within 20 km:**")
            df_20km_area = pd.DataFrame({
                "Pincode": [f"{pin} {show_pin_details(pin)}   \u2191 {show_pin_dist(org_pin, pin, False):.2f} km {show_pin_dir(org_pin, pin, False)}" for pin in area_20km]
            })
            df_20km_area.index = df_20km_area.index + 1
            st.dataframe(df_20km_area, use_container_width=True)

            st.markdown("**Pincodes within 50 km:**")
            df_50km_area = pd.DataFrame({
                "Pincode": [f"{pin} {show_pin_details(pin)}   \u2191 {show_pin_dist(org_pin, pin, False):.2f} km {show_pin_dir(org_pin, pin, False)}" for pin in area_50km]
            })
            df_50km_area.index = df_50km_area.index + 1
            st.dataframe(df_50km_area, use_container_width=True)

        with col2:
            st.subheader("🏤 Post-Office-Based")
            st.metric("Nearest Pincode", f"{po_nearest} {show_pin_details(po_nearest)}", f"{po_dist:.2f} km {show_pin_dir(org_pin, area_nearest, False)}")
            st.markdown("**Pincodes within 5 km:**")
            df_5km_po = pd.DataFrame({
                "Pincode": [f"{pin} {show_pin_details(pin)}   \u2191 {show_pin_dist(org_pin, pin, True):.2f} km {show_pin_dir(org_pin, pin, True)}" for pin in po_5km]
            })
            df_5km_po.index = df_5km_po.index + 1
            st.dataframe(df_5km_po, use_container_width=True)

            st.markdown("**Pincodes within 10 km:**")
            df_10km_po = pd.DataFrame({
                "Pincode": [f"{pin} {show_pin_details(pin)}   \u2191 {show_pin_dist(org_pin, pin, True):.2f} km {show_pin_dir(org_pin, pin, True)}" for pin in po_10km]
            })
            df_10km_po.index = df_10km_po.index + 1
            st.dataframe(df_10km_po, use_container_width=True)

            st.markdown("**Pincodes within 20 km:**")
            df_20km_po = pd.DataFrame({
                "Pincode": [f"{pin} {show_pin_details(pin)}   \u2191 {show_pin_dist(org_pin, pin, True):.2f} km {show_pin_dir(org_pin, pin, True)}" for pin in po_20km]
            })
            df_20km_po.index = df_20km_po.index + 1
            st.dataframe(df_20km_po, use_container_width=True)

            st.markdown("**Pincodes within 50 km:**")
            df_50km_po = pd.DataFrame({
                "Pincode": [f"{pin} {show_pin_details(pin)}   \u2191 {show_pin_dist(org_pin, pin, True):.2f} km {show_pin_dir(org_pin, pin, True)}" for pin in po_50km]
            })
            df_50km_po.index = df_50km_po.index + 1
            st.dataframe(df_50km_po, use_container_width=True)
            

        # Map display for Area-Based centroids
        st.subheader("🗺️ Map of Input Pincode Area (Area-Based Centroids)")
        m_area = create_pincode_map(pin, df_centroids, area_nearest, area_5km, area_10km, area_20km, area_50km)
        col_left, col_center, col_right = st.columns([1, 3, 1])
        with col_center:
            st_folium(m_area, width=1280, height=500)

        # Map display for Post Office locations
        st.subheader("🗺️ Map of Input Pincode Area (Post Office Locations)")
        m_po = create_pincode_map(pin, df_cleaned, po_nearest, po_5km, po_10km, po_20km, po_50km)
        col_left, col_center, col_right = st.columns([1, 3, 1])
        with col_center:
            st_folium(m_po, width=1280, height=500)

        # === Comparison Section ===
        def show_comparison(title, list1, list2, label1, label2):
            diff1 = sorted(set(list1) - set(list2))
            diff2 = sorted(set(list2) - set(list1))
            combined = sorted(set(diff1 + diff2))

            status = []
            for p in combined:
                in1 = "✅" if p in list1 else "❌"
                in2 = "✅" if p in list2 else "❌"
                status.append((f"{p} {show_pin_details(p)}", in1, in2))

            df_diff = pd.DataFrame(status, columns=["Pincode", label1, label2])
            df_diff.index = df_diff.index + 1
            st.markdown(f"### 🔍 {title}")
            st.dataframe(df_diff, use_container_width=True)

        st.markdown("---")
        show_comparison("5 km Radius Differences", area_5km, po_5km, "Area", "Post-office")
        st.markdown("---")
        show_comparison("10 km Radius Differences", area_10km, po_10km, "Area", "Post-office")
        st.markdown("---")
        show_comparison("20 km Radius Differences", area_20km, po_20km, "Area", "Post-office")
        st.markdown("---")
        show_comparison("50 km Radius Differences", area_50km, po_50km, "Area", "Post-office")
