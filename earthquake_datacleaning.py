import requests
import pandas as pd
import numpy as np
from datetime import datetime

all_records = []

start_year = datetime.now().year - 5
end_year = datetime.now().year

#GETTING DATA FROM API

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

for year in range(start_year, end_year + 1):

    if year == start_year:
        start_month = datetime.now().month
    else:
        start_month = 1

    if year == end_year:
        end_month = datetime.now().month
    else:
        end_month = 12

    for month in range(start_month, end_month + 1):

        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"

        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": 3
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Failed for {start_date}: {response.text[:200]}")
            continue

        try:
            data = response.json()
        except Exception as e:
            print(f"JSON error for {start_date}: {e}")
            continue

        for f in data["features"]:

            p = f["properties"]
            g = f["geometry"]["coordinates"]

            all_records.append({
                "id": f.get("id"),

                # CONVERT DATETIME FIELDS FOR TIME/UPDATED
                "time": pd.to_datetime(
                    p.get("time"), unit="ms", errors="coerce"
                ),

                "updated": pd.to_datetime(
                    p.get("updated"), unit="ms", errors="coerce"
                ),

                "latitude": g[1] if g else None,
                "longitude": g[0] if g else None,
                "depth_km": g[2] if g else None,

                "mag": p.get("mag"),
                "magType": p.get("magType"),
                "place": p.get("place"),
                "status": p.get("status"),
                "tsunami": p.get("tsunami"),
                "sig": p.get("sig"),
                "net": p.get("net"),
                "nst": p.get("nst"),
                "dmin": p.get("dmin"),
                "rms": p.get("rms"),
                "gap": p.get("gap"),

                #"magError": p.get("magError"),
                #"depthError": p.get("depthError"),
                #"magNst": p.get("magNst"),

                "types": p.get("types"),
                "ids": p.get("ids"),
                "sources": p.get("sources"),
                "type": p.get("type"),

                "code": p.get("code"),       
                "alert": p.get("alert"),
                "felt": p.get("felt"),
                "cdi": p.get("cdi"),
                "mmi": p.get("mmi"),
            })

        print(
            f"{start_date} completed | "
            f"Total records: {len(all_records)}"
        )

# CREATE DataFrame

df = pd.DataFrame(all_records)

print("Original shape:", df.shape)





# Other string fields
text_cols = [
    "magType",
    "status",
    "type",
    "net",
    "sources",
    "types"
]

for col in text_cols:
    df[col] = df[col].str.strip().str.lower()



#  EXTRACT COUNTRY FROM PLACE

df["country"] = (
    df["place"]
    .str.extract(r",\s*([^,]+)$")[0].str.strip().str.lower()
)
df["country"] = df["country"].fillna("unknown")

#  CONVERT NUMERIC FIELDS

numeric_cols = [  "mag","depth_km","nst","dmin","rms","gap","sig","felt","cdi","mmi" ]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# HANDLE MISSING VALUES

df["alert"] = (
    df["alert"].fillna("unknown").str.strip().str.lower()
)

"""
df["magError"] = df["magError"].fillna(0)
df["depthError"] = df["depthError"].fillna(0)
df["magNst"] = df["magNst"].fillna(0)
"""
df["felt"] = df["felt"].fillna(0)


# Fill missing numeric values with median
median_cols = [ "cdi", "mmi","nst","dmin","rms","gap" ]

for col in median_cols:
    df[col] = df[col].fillna(df[col].median())


# DERIVED COLUMNS

# Date-based columns
df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day
df["day_of_week"] = df["time"].dt.day_name()

# Depth classification
df["depth_category"] = np.where(
    df["depth_km"] < 50,
    "shallow",
    "deep"
)

# Strong earthquake
df["strong_earthquake"] = np.where(
    df["mag"] >= 6,
    "strong",
    "not strong"
)

# Destructive earthquake
df["destructive_earthquake"] = np.where(
    df["mag"] >= 7,
    "destructive",
    "not destructive"
)

print(df.isnull().sum())

print(df.head(2))

print(df.shape)
print(df.dtypes)
print(df.isnull().sum())


# Save cleaned data as CSV
df.to_csv("earthquakes_cleaned.csv", index=False)

print("Cleaned data saved successfully!")
