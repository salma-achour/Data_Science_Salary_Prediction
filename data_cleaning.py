# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:19:15 2020

@author: salma
"""

import pandas as pd

df = pd.read_csv("glassdoor_jobs.csv")

# Remove missing salary data
df = df[df["Salary Estimate"] != "-1"]

# Salary parsing

## Removing the ( (Glassdoor est.)) expression
salary = df["Salary Estimate"].apply(lambda x: x.split("(")[0])

## Removing the "K" symbol and the "$" symbol
salary_kd = salary.apply(lambda x: x.replace("K","").replace("$",""))

## Making the per hour a seperate feature
df["per_hour"] = df["Salary Estimate"].apply(lambda x: 1 if "per hour" in x.lower() else 0)

## Making the Employer provided a seperate feature
df["employer_provided"] = df["Salary Estimate"].apply(lambda x: 1 if "employer provided salary:" in x.lower() else 0)

## Removing per hour and employer provided from salary_kd
min_hr = salary_kd.apply(lambda x: x.lower().replace("per hour", "").replace("employer provided salary:", ""))


## Retriving the min salary
df["min_salary"]= min_hr.apply(lambda x: int(x.split("-")[0]))

## Retrieving the max salary
df["max_salary"]= min_hr.apply(lambda x: int(x.split("-")[1]))

## Calculating average salary
df["avg_salary"] = (df["min_salary"] + df["max_salary"])/2


# company name text only
df["company_text"] = df.apply(lambda x: x["Company Name"] if x['Rating'] <0 else x["Company Name"][:-3], axis =1)


# seperate  state and city
df["job_state"] = df["Location"].apply(lambda x: x.split(",")[1])

# Removing los angelos from states
df['job_state']= df.job_state.apply(lambda x: x.strip() if x.strip().lower() != 'los angeles' else 'CA')

# Is the job position in the Hedquarters?
df["hq_job_same_state"]  = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

# convert founded to age
df["company_age"] = df.Founded.apply(lambda x: x if x<1 else 2020 - x)

# Parsing job description (looking for some data science tools and skills)

skills = ["python", "r studio", "excel","spark", "machine learning", "deep learning" , "matlab", "big data", "business intelligence", "mongo"]

for i in skills:
    df[i] = df["Job Description"].apply(lambda x: 1 if i in x.lower() else 0)
    
# Dropping extra index column
del df["Unnamed: 0"]

# useful functions
def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'
    
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'



# Job title and seniority 
df['job_simp'] = df['Job Title'].apply(title_simplifier)
df['seniority'] = df['Job Title'].apply(seniority)

#  Competitor count
df['num_comp'] = df['Competitors'].apply(lambda x: len(x.split(',')) if x != '-1' else 0)

# hourly wage to annual 
df['min_salary'] = df.apply(lambda x: x.min_salary*2 if x.per_hour ==1 else x.min_salary, axis =1)
df['max_salary'] = df.apply(lambda x: x.max_salary*2 if x.per_hour ==1 else x.max_salary, axis =1)

# remove "\n" from job title
df['company_text'] = df.company_text.apply(lambda x: x.replace('\n', ''))


# Export dataframe to csv file
df_out = df.to_csv("df_salary-clean.csv", index=False)