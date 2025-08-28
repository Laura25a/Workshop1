#%% Imports
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# connect to etl db
conn = sqlite3.connect("../data/candidatesdw.db")
cursor = conn.cursor()

#%% Hires by Technology
query = """
   SELECT t.Technology, COUNT(*) AS total_hires
   FROM scores_fact_table f
   JOIN technology_table t ON f.id_technology = t.id_technology
   WHERE f.hired = 1
   GROUP BY t.Technology
   ORDER BY total_hires DESC;
"""
df_tec = pd.read_sql_query(query, conn)
print("Hires by technology ------")
print(df_tec)

#%% Visualization: Hires by technology bar chart

technologies = df_tec['Technology']
hires = df_tec['total_hires']

plt.figure(figsize=(10,8))
plt.barh(technologies, hires, color='skyblue') 
plt.xlabel("Total Hires")
plt.ylabel("Technology")
plt.title("Hires by Technology")
plt.tight_layout()
plt.show()


#%%GET Hires by year

query = """
    SELECT d.year, COUNT(*) AS total_hires
    FROM scores_fact_table f
    JOIN date_table d ON f.date_id = d.date_id
    WHERE hired = 1
    GROUP BY year
    ORDER BY d.year ASC;
"""
df_year = pd.read_sql_query(query, conn)
print("Hires by year")
print(df_year)

#%%Visualization: Hires by year line chart

years = df_year['year']
hires_year = df_year['total_hires']

plt.plot(years, hires_year, marker='o', linestyle='-', color='b')  # sin x= y y=
plt.xlabel("Years")
plt.ylabel("Hires by year")
plt.title("Hires by Year Line Chart")
plt.grid(True)
plt.show()


# %%GET Hires by seniority
query = """
   SELECT s.Seniority, COUNT(*) AS total_hires
   FROM scores_fact_table f
   JOIN seniority_table s ON f.id_seniority = s.id_seniority
   WHERE f.hired = 1
   GROUP BY s.Seniority
   ORDER BY total_hires DESC;
"""
df_seniority = pd.read_sql_query(query, conn)
print("Hires by seniority----------")
print(df_seniority)

#%%Visualization: Hires by seniority bar chart

labels = df_seniority['Seniority']
sizes = df_seniority['total_hires']

plt.figure(figsize=(10,6))
bars = plt.bar(labels, sizes, color='skyblue')
plt.bar_label(bars)
plt.xlabel("Total Hires")
plt.ylabel("Seniority")
plt.title("Hires by Seniority")
plt.tight_layout()
plt.show()

#%%Hires by country over years

query = """
   SELECT
  c.Country, d.year,
  COUNT(*) AS total_hires
FROM scores_fact_table f 
JOIN country_table c ON f.id_country = c.id_country
JOIN date_table d ON f.date_id = d.date_id
WHERE f.hired = 1
AND c.Country IN ('United States of America', 'Brazil','Colombia','Ecuador')
GROUP BY c.Country, d.year
ORDER BY d.year ASC;
"""
df_country_by_years = pd.read_sql_query(query, conn)
print("Hires by over years -------")
print(df_country_by_years)

#%%Visualization: Hires by country over years stacked bar chart

for country in df_country_by_years['Country'].unique():
    subset = df_country_by_years[df_country_by_years['Country'] == country]
    plt.plot(subset['year'], subset['total_hires'], marker='o', label=country)

plt.xlabel("Year")
plt.ylabel("Total Hires")
plt.title("Hires by Country Over Years")
plt.legend()
plt.grid(True)
plt.show()
# %% Hires by YOE range

query = """
   SELECT 
   CASE 
        WHEN YOE < 2 THEN '0-1'
        WHEN YOE BETWEEN 2 AND 5 THEN '2-5'
        WHEN YOE BETWEEN 6 AND 10 THEN '6-10'
        WHEN YOE BETWEEN 11 AND 20 THEN '11-20'
        WHEN YOE BETWEEN 21 AND 30 THEN '21-30'
        WHEN YOE BETWEEN 31 AND 40 THEN '31-40'
   END AS yoe_range,
   COUNT(*) AS total_hires
   FROM scores_fact_table
   WHERE hired = 1
   GROUP BY yoe_range
   ORDER BY total_hires DESC;"""
   
df_YOE= pd.read_sql_query(query, conn)
print("Hires by YOE range -------")
print(df_YOE)

#%%Visualization: Hires by YOE range bar chart

plt.figure(figsize=(10,6))
plt.bar(df_YOE['yoe_range'], df_YOE['total_hires'], color='blue')
plt.xlabel('Years of Experience Range')
plt.ylabel('Total Hires')
plt.title('Hires by Years of Experience Range')
plt.show()


#%% Not Hires by Technology
query = """
   SELECT t.Technology, COUNT(*) AS total_not_hires
   FROM scores_fact_table f
   JOIN technology_table t ON f.id_technology = t.id_technology
   WHERE f.hired = 0
   GROUP BY t.Technology
   ORDER BY total_not_hires DESC;
"""
df_not_tec = pd.read_sql_query(query, conn)
print("Not Hires by technology ------")
print(df_not_tec)


#%% Visualization: not Hires by technology bar chart

technologies = df_not_tec['Technology']
not_hires = df_not_tec['total_not_hires']

plt.figure(figsize=(10,8))
plt.barh(technologies, not_hires, color='skyblue') 
plt.xlabel("Total not Hires")
plt.ylabel("Technology")
plt.title("Not Hires by Technology")
plt.tight_layout()
plt.show()

