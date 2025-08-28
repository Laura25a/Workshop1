import pandas as pd
import sqlite3

#Extract

# Load CSV
df = pd.read_csv("data/candidates.csv", sep=";", low_memory=False)



# Make sure numeric fields have no NaN
numeric_cols = ["YOE","Code Challenge Score","Technical Interview Score"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    

#Transform


def transform(data):
    #Apply the “HIRED” rule.
    data["hired"] = ((data["Code Challenge Score"] >= 7) & (data["Technical Interview Score"] >= 7)).astype(int)
    return data

df = transform(df)

#interviewed table

interviewed_table = df[["First Name", "Last Name", "Email"]].copy()
interviewed_table = interviewed_table.reset_index(drop=True)
interviewed_table["id_interviewed"] = interviewed_table.index + 1

#country table

country_table = df[["Country"]].drop_duplicates()
country_table["id_country"] = country_table.index + 1

#seniority table

seniority_table = df[["Seniority"]].drop_duplicates()
seniority_table["id_seniority"] = seniority_table.index + 1

#technology table

technology_table = df[["Technology"]].drop_duplicates()
technology_table["id_technology"] = technology_table.index + 1

#date table

df["Application Date"] = pd.to_datetime(df["Application Date"], dayfirst=True) #true = DD/MM/YYYY
date_table = df[["Application Date"]].drop_duplicates()
date_table = pd.DataFrame({
    "full_date": df["Application Date"].drop_duplicates()
}).reset_index(drop=True)

date_table["date_id"] = date_table.index + 1
date_table["day"] = date_table["full_date"].dt.day
date_table["month"] = date_table["full_date"].dt.month
date_table["year"] = date_table["full_date"].dt.year


#ref
df = df.merge(interviewed_table, on=["First Name", "Last Name", "Email"])
df = df.merge(country_table, on="Country")
df = df.merge(seniority_table, on="Seniority")
df = df.merge(technology_table, on="Technology")
df = df.merge(date_table, left_on="Application Date", right_on="full_date")

#score table

df["id_scores"] = df.index + 1
score_table = df[["id_scores","Code Challenge Score", "Technical Interview Score", "hired","id_seniority","id_interviewed","id_country","date_id","YOE","id_technology"]].drop_duplicates()


#Load

#Insert the transformed data into a DW

conn = sqlite3.connect("data/candidatesdw.db")

# Load data into sqlite
interviewed_table.to_sql("interviewed_table", conn, if_exists="replace", index=False)
country_table.to_sql("country_table", conn, if_exists="replace", index=False)
seniority_table.to_sql("seniority_table", conn, if_exists="replace", index=False)
technology_table.to_sql("technology_table", conn, if_exists="replace", index=False)
date_table.to_sql("date_table", conn, if_exists="replace", index=False)
score_table.to_sql("scores_fact_table", conn, if_exists="replace", index=False)

# Close connection
conn.close()

print("ETL complete")

