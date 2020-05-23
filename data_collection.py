# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:57:33 2020

@author: salma
"""

import Glassdoor_scraper as gs 
import pandas as pd 

path = "C:/Users/salma/Downloads/Chromedriver/chromedriver"

df = gs.get_jobs('data scientist',1000, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index = False)