# Project Summary

This project is a Sales Operations lead scoring pipeline built in Python. I built this project as a learning exercise to familiarize myself with the types of analytical and data questions a Sales team might face. The goal is to simulate how a sales team can move from a raw company list to a ranked set of prioritized leads. 

## Step-by-step solution

### Step 1
Creating the input dataset, a CSV file containing a seed list of Finnish companies. This dataset is synthetic and was generated with the help of ChatGPT. It provides a controlled starting point for the pipeline and avoids scraping or collecting sensitive data.
### Step 2
Enriching the dataset with PRH open data. Each company name is sent to the PRH/YTJ open data API. The API returns official company-level information.
### Step 3
Defining a rule-based lead scoring logic. The score is based on three factors with different weights: Compliance pressure, Business model fit, and company size. I developed this scoring logic with the help of ChatGPT.
### Step 6
Calculating scores for each company and ranking them from highest to lowest score. This ranking can be used for sales prioritization.

## Workflow Structure

seed_companies.csv -> load_clean_data.py -> api_reguest.py -> score_leads.py -> main.py -> scored_companies.csv

**To run the entire pipeline, execute src/main.py. It runs the workflow from start to finish and returns a ranked list of companies.**
