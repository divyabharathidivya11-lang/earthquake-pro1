import pandas as pd
from sqlalchemy import create_engine

username = "root"
password = "DivyaMysql11"
host = "localhost"
database = "earthquake_db"


engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{database}"
)

print("SQLAlchemy engine created successfully!")


#Magnitude & Depth 
#1. Top 10 strongest earthquakes (mag). 
query = """
Select * from earthquakes
order by mag DESC
limit 10
"""

result = pd.read_sql(query, engine)

print(result)

# 2.Top 10 deepest earthquakes (depth_km). 
query1 = """
Select  id,time,place,depth_km,mag,magType
From earthquakes
order by depth_km DESC
limit 10;
"""

result1 = pd.read_sql(query1, engine)

print(result1)

#3. shallow earthquakes < 50 km and mag > 7.5. 
query3 = """
select id, time, place, depth_km, mag
from earthquakes
where depth_category = 'shallow' and mag > 7.5;
"""

result3 = pd.read_sql(query3, engine)

print(result3)

#5. Average magnitude per magnitude type (magType). 
query4=""" 
select magType, AVG(mag) 
from earthquakes
group by magType;
"""
result4=pd.read_sql(query4,engine)

print(result4)

#Time Analysis 
#6. Year with most earthquakes.
query5="""
select year,count(*) as earthquake_count 
from earthquakes
group by year
order by earthquake_count desc
"""

result5=pd.read_sql(query5,engine)

print(result5)

#7. Month with highest number of earthquakes. 
query6=""" 
select month,count(*) AS earthquake_count
from earthquakes
group by month
order by earthquake_count DESC
limit 5;
"""
result6=pd.read_sql(query6,engine)

print(result6)

#8. Day of week with most earthquakes. 
query7=""" 
select  day_of_week,count(*) as earthquake_count
from earthquakes
group by day_of_week
order by earthquake_count desc
limit 5;
"""

result7=pd.read_sql(query7,engine)

print(result7)

#9. Count of earthquakes per hour of day. 

query8="""
select hour(time) as hour,count(*) as earthquake_count
from earthquakes
group by hour
order by earthquake_count desc
limit 5
"""

result8=pd.read_sql(query8,engine)

print(result8)

#10.   Most active reporting network (net). 
query9="""
select net,count(*) as earthuake_count
from earthquakes
group by net
order by earthuake_count desc
"""

result9=pd.read_sql(query9,engine)

print(result9)

#11.  Top 5 places with highest casualties. 
query10="""
select place,SUM(felt) AS casualties
from earthquakes
where felt > 0
group by place
order by casualties desc
limit 5;
"""
result10=pd.read_sql(query10,engine)
print(result10)

#13.  Average economic loss by alert level. 

query11="""
select alert,count(*) AS economic_loss
from earthquakes
Where alert != 'unknown'
group by alert
order by economic_loss DESC;
"""

result11=pd.read_sql(query11,engine)
print(result11)

#Event Type & Quality Metrics 
#14.  Count of reviewed vs automatic earthquakes (status).

query12="""
select status,count(*) as earthquake_count
from earthquakes
group by status
"""
result12=pd.read_sql(query12,engine)

print(result12)

#15.  Count by earthquake type (type). 
query13 = """
select  type,count(*) AS earthquake_count
from earthquakes
group by type
order by earthquake_count DESC;
"""

result13 = pd.read_sql(query13, engine)

print(result13)

#16.  Number of earthquakes by data type (types). 
query14=""" 
select types,count(*) as earthquake_types_count
from earthquakes
group by types
"""

result14=pd.read_sql(query14,engine)

print(result14)


#18.  Events with high station coverage (nst > threshold).
query15=""" 
select id,place, mag,nst
from earthquakes
where nst > 50
order by nst desc;
 """
result15=pd.read_sql(query15,engine)

print(result15)


#print("uniqu",df["tsunami"].unique())
#Tsunamis & Alerts 
#19.  Number of tsunamis triggered per year. 

query16=""" 
select year,count(*) as eathquake_count_tsunami
from earthquakes
where tsunami=1
group by year
order by year
"""
result16=pd.read_sql(query16,engine)

print(result16)


#20.Count earthquakes by alert levels (red, orange, etc.).

query17=""" 
select alert,count(*) as earthquae_alert_count
from earthquakes
group by alert
"""
result17=pd.read_sql(query17,engine)

print(result17)


#Seismic Pattern & Trends Analysis.             
#21.Find the top 5 countries with the highest average magnitude of earthquakes in past 5 years 

#print(df["country"].unique())

query18=""" 
select country,avg(mag) as avg_magnitude
from earthquakes
where country !="unknown"
group by country
order by avg_magnitude desc
limit 5
"""

result18=pd.read_sql(query18,engine)

print(result18)

#print(df["depth_category"].unique())
#22.Find countries that have experienced both shallow and deep earthquakes within the same month. 

query19="""
select country,year,month
from earthquakes
where country != 'unknown'
group by country, year, month
having sum(depth_km < 70) > 0 and sum(depth_km > 300) > 0
limit 10;
"""

result19=pd.read_sql(query19,engine)
print(result19)

#23 Compute the year-over-year growth rate in the total number of earthquakes globally.

query20 = """
SELECT
    year,
    earthquake_count,
    LAG(earthquake_count) OVER (ORDER BY year) AS previous_year_count,
    ROUND(
        (earthquake_count - LAG(earthquake_count) OVER (ORDER BY year))
        / LAG(earthquake_count) OVER (ORDER BY year) * 100,
        2
    ) AS growth_rate
FROM (
    SELECT
        year,
        COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY year
) AS yearly_data
ORDER BY year;
"""

result20 = pd.read_sql(query20, engine)
print(result20)

#24. List the 3 most seismically active regions by combining both frequency and average magnitude. 

query21="""
select country,count(*) as earthquake_count,avg(mag) as avg_magnitude
from earthquakes
where country !="unknown"
group by country
order by earthquake_count desc, avg_magnitude desc
limit 3
"""

result21=pd.read_sql(query21,engine)
print(result21)

#Depth, Location & Distance-Based  Analysis. 
#25. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator. 

query22="""
select country,avg(depth_km) as avg_depth
from earthquakes
where country !="unknown" and latitude between -5 and 5    
group by country
order by avg_depth desc
"""

result22=pd.read_sql(query22,engine)
print(result22)

#26. Identify countries having the highest ratio of shallow to deep earthquakes. 

query23="""
select country, sum(depth_category = 'shallow') as shallow_count,
    sum(depth_category = 'deep') as deep_count,
    sum(depth_category = 'shallow') / sum(depth_category = 'deep') as shallow_to_deep_ratio
from earthquakes
where country != "unknown"
group by country
having sum(depth_category = 'deep') > 0
order by shallow_to_deep_ratio desc
limit 10;
"""

result23=pd.read_sql(query23,engine)
print(result23)

#27. Find the average magnitude difference between earthquakes with tsunami alerts and those without. 

query24=""" 
select avg(case when tsunami = 1 then mag else null end) AS avg_mag_with_tsunami,
       avg(case when tsunami = 0 then mag else null end) AS avg_mag_without,
       round(avg(case when tsunami = 1 then mag else null end) - 
          avg(case when tsunami = 0 then mag else null end), 2) AS avg_mag_difference 
from earthquakes;
"""

result24=pd.read_sql(query24,engine)
print(result24)


#28. Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins). 

query25="""
select id, country, gap, rms, (gap + rms) / 2 AS avg_error_margin
from earthquakes  
where country != "unknown"
order by avg_error_margin desc
limit 20;
"""

result25=pd.read_sql(query25,engine)
print(result25)


#30. Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km). 

query26=""" 
select country, count(*) as deep_earthquake_count
from earthquakes
where depth_km > 300 and country != "unknown"
group by country
order by deep_earthquake_count desc
limit 10;
"""

result26=pd.read_sql(query26,engine)
print(result26) 

