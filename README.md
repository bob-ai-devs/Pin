# 📍 Nearby Pincode Comparator

A Streamlit-based application for comparing nearby Indian pincodes using two different geographic reference datasets:

* 📌 **Area-Based Centroids**
* 🏤 **Post Office Locations**

The application calculates the nearest pincode, identifies pincodes within **5 km, 10 km, and 20 km**, displays directional information, and provides interactive maps for both geographic approaches.

---

# 🚀 Features

## 📌 Pincode Search

Enter a valid Indian pincode to analyze its surrounding geographic area.

The application retrieves:

* District
* State
* Latitude
* Longitude
* Nearest pincode
* Nearby pincodes
* Distance from the input pincode
* Direction from the input pincode

---

## 📊 Dual Geographic Comparison

The application performs the same analysis using two independent location datasets.

### 1. Area-Based Centroids

Uses:

```text
pincode_centroids_sorted.csv
```

This dataset represents pincodes using geographic area centroid coordinates.

### 2. Post Office Locations

Uses:

```text
cleaned_pincode_lat_long.csv
```

This dataset represents pincodes using post-office geographic coordinates.

The two approaches can therefore produce different nearest pincodes and nearby-pincode lists.

---

# 📏 Distance Analysis

The application uses the **Haversine formula** to calculate the geographical distance between two latitude/longitude coordinates.

Distances are calculated in kilometres.

The application identifies pincodes in the following ranges:

| Radius | Description                      |
| ------ | -------------------------------- |
| 5 km   | Pincodes within 5 km             |
| 10 km  | Pincodes between 5 km and 10 km  |
| 20 km  | Pincodes between 10 km and 20 km |
| 50 km  | Pincodes between 20 km and 50 km |

The nearest pincode is also identified independently.

---

# 🧭 Direction Analysis

For each nearby pincode, the application calculates its approximate geographical direction relative to the input pincode.

Possible directions include:

* North
* South
* East
* West
* North-East
* North-West
* South-East
* South-West
* Same

The direction is determined by comparing the latitude and longitude of the two locations.

---

# 🗺️ Interactive Maps

The application generates interactive **Folium** maps for both datasets.

Two maps are displayed:

### 📌 Area-Based Centroid Map

Shows nearby pincodes based on area centroid coordinates.

### 🏤 Post Office Location Map

Shows nearby pincodes based on post-office coordinates.

The maps use marker clustering to keep the visualization manageable when multiple pincodes are located close to each other.

---

# 🗺️ Map Marker Legend

Different marker colours represent different categories.

| Marker    | Meaning                  |
| --------- | ------------------------ |
| 🔴 Red    | Input / Original Pincode |
| 🟠 Orange | Nearest Pincode          |
| 🟢 Green  | Within 5 km              |
| 🔵 Blue   | Within 10 km             |
| 🟣 Purple | Within 20 km             |
| ⚫ Black   | Within 50 km             |

Each marker provides the pincode and corresponding district/state information.

---

# 🔍 Radius Comparison

The application compares the results from the two geographic datasets.

For each radius:

* 5 km
* 10 km
* 20 km
* 50 km

the application identifies pincodes that appear in one dataset but not the other.

Example:

| Pincode | Area | Post-office |
| ------- | ---- | ----------- |
| 400001  | ✅    | ❌           |
| 400002  | ❌    | ✅           |
| 400003  | ✅    | ✅           |

This helps identify differences between **area-centroid-based** and **post-office-based** proximity calculations.

---

# 📂 Input Data

The application expects the following CSV files in the same directory as the Streamlit application.

```text
original_pin.csv
pincode_centroids_sorted.csv
cleaned_pincode_lat_long.csv
```

## 1. `original_pin.csv`

Contains pincode administrative information.

Important columns:

```text
pincode
district
statename
```

Example:

```text
pincode,district,statename
400001,Mumbai,Maharashtra
```

The `pincode` column is loaded as a string to preserve leading zeroes.

---

## 2. `pincode_centroids_sorted.csv`

Contains geographic centroid information for pincodes.

Required columns:

```text
Pincode
Latitude
Longitude
```

Example:

```text
Pincode,Latitude,Longitude
400001,18.9388,72.8354
```

---

## 3. `cleaned_pincode_lat_long.csv`

Contains geographic coordinates corresponding to post-office locations.

Required columns:

```text
Pincode
Latitude
Longitude
```

Example:

```text
Pincode,Latitude,Longitude
400001,18.9388,72.8354
```

---

# 📁 Recommended Project Structure

```text
nearby-pincode-comparator/
│
├── app.py
├── requirements.txt
├── README.md
│
├── original_pin.csv
├── pincode_centroids_sorted.csv
└── cleaned_pincode_lat_long.csv
```

---

# 🛠️ Installation

## 1. Clone or download the project

Place all application files and CSV datasets in the same directory.

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

The application uses:

| Package            | Purpose                            |
| ------------------ | ---------------------------------- |
| `streamlit`        | Web application interface          |
| `pandas`           | CSV loading and data processing    |
| `numpy`            | Numeric calculations               |
| `folium`           | Interactive maps                   |
| `streamlit-folium` | Embedding Folium maps in Streamlit |

Python's built-in `math` module is used for the Haversine calculation and does not need to be installed separately.

---

# ▶️ Running the Application

Run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL, normally similar to:

```text
http://localhost:8501
```

Open the URL in a web browser.

---

# 🔄 Application Workflow

The application follows this workflow:

```text
Enter Pincode
      │
      ▼
Validate Pincode
      │
      ▼
Load Area Centroid Data
      │
      ├──► Find Nearest Pincode
      ├──► Find 5 km Pincodes
      ├──► Find 10 km Pincodes
      ├──► Find 20 km Pincodes
      └──► Find 50 km Pincodes
      │
      ▼
Load Post Office Data
      │
      ├──► Find Nearest Pincode
      ├──► Find 5 km Pincodes
      ├──► Find 10 km Pincodes
      ├──► Find 20 km Pincodes
      └──► Find 50 km Pincodes
      │
      ▼
Calculate Directions
      │
      ▼
Display Tables
      │
      ▼
Display Interactive Maps
      │
      ▼
Compare Area vs Post-Office Results
```

---

# 📐 Haversine Distance

The application calculates the great-circle distance between two geographic coordinates.

The general formula is:

```text
a = sin²(Δlat / 2)
    + cos(lat1) × cos(lat2) × sin²(Δlon / 2)

c = 2 × atan2(√a, √(1-a))

distance = R × c
```

where:

```text
R = 6371 km
```

The result represents the approximate geographical distance between the two coordinates.

---

# 🔎 Nearest Pincode Calculation

For the selected pincode, the application:

1. Retrieves its latitude and longitude.
2. Iterates through the available pincodes.
3. Calculates the Haversine distance.
4. Excludes the input pincode itself.
5. Tracks the minimum distance.
6. Returns the corresponding nearest pincode.

The process is performed independently for:

* Area centroid coordinates
* Post-office coordinates

---

# 📋 Output

After entering a valid pincode, the application displays:

## Input Pincode Information

```text
District
State
```

## Area-Based Results

```text
Nearest Pincode
Distance
Direction

Pincodes within 5 km
Pincodes within 10 km
Pincodes within 20 km
Pincodes within 50 km
```

## Post-Office-Based Results

```text
Nearest Pincode
Distance
Direction

Pincodes within 5 km
Pincodes within 10 km
Pincodes within 20 km
Pincodes within 50 km
```

---

# 📊 Comparison Analysis

The application compares the two geographic approaches at each radius.

### 5 km

```text
Area-Based vs Post-Office-Based
```

### 10 km

```text
Area-Based vs Post-Office-Based
```

### 20 km

```text
Area-Based vs Post-Office-Based
```

A check mark indicates that a pincode exists in the corresponding result set, while a cross indicates that it does not.

---

# ⚠️ Data Requirements

The application assumes that:

* Pincodes are represented as strings.
* `Pincode` values are consistent across datasets.
* Latitude values are numeric.
* Longitude values are numeric.
* Required CSV files are available in the application directory.
* Coordinate values represent valid geographic locations.

Pincodes are explicitly converted to strings to prevent issues with leading zeroes.

---

# 🛡️ Error Handling

The application handles several common situations, including:

* Invalid or missing pincodes
* Missing geographic records
* Missing district/state information
* Missing coordinate matches

If the requested pincode cannot be found in the required datasets, the application displays an error message.

---

# 🎯 Use Cases

This application can be used for:

* 📍 Pincode proximity analysis
* 🏤 Post-office location analysis
* 🗺️ Geographic service-area analysis
* 🏦 Banking branch/service coverage analysis
* 🚚 Delivery and logistics analysis
* 📊 Comparing geographic datasets
* 🔎 Identifying differences between centroid and physical-location data
* 📌 Regional service planning

---

# 🏦 Potential Banking Applications

For a banking use case, pincode-level geographic analysis can support:

* Branch proximity analysis
* ATM/service-point coverage
* Customer geographic segmentation
* Banking service accessibility analysis
* Branch catchment-area analysis
* Location-based service planning
* Rural and semi-urban coverage analysis
* Comparison of administrative areas versus physical service locations

---

# 💻 Technology Stack

```text
Python
│
├── Streamlit
├── Pandas
├── NumPy
├── Folium
├── Streamlit-Folium
└── Haversine Geographic Distance Calculation
```

---

# 📜 License

This project is intended for internal/proof-of-concept use unless a separate license is provided.

The geographic datasets used by the application should be used in accordance with their respective data-source terms and licensing requirements.

---

# 👨‍💻 Application Summary

**Nearby Pincode Comparator** provides a side-by-side geographic analysis of Indian pincodes using two different coordinate representations.

It combines:

```text
Pincode Data
      +
Geographic Coordinates
      +
Haversine Distance
      +
Directional Analysis
      +
Interactive Maps
      +
Dataset Comparison
```

to provide a consolidated view of nearby pincode relationships.
