## Project Description

In this project, an ETL process was performed. Data was loaded into a data warehouse, and KPIs and visualizations were generated from them.
This was done to analyze relevant indicators regarding the hiring process of several candidates.

## Repository Structure

C:
│ .gitignore
│ README.md
│
├───data
│ candidates.csv
│ candidatesdw.db
│
├───pics
│ star_diagram.png
│
└───src
etl.py # Code containing extraction, transformation, and loading
query.py # Code with SQL queries and visualizations