import pandas as pd
from sqlalchemy import create_engine

username = "root"
password = "DivyaMysql11"
host = "localhost"
database = "earthquake_db"
# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{database}"
)
print("Engine created successfully!")

# Read cleaned data
df = pd.read_csv("earthquakes_cleaned.csv")

print("Cleaned data loaded successfully!")
print("Shape:", df.shape)


#  CREATE TABLE AND INSERT DATA 
df.to_sql( "earthquakes", con=engine,
           if_exists="replace", index=False )
print("Earthquake data inserted into MySQL successfully!")