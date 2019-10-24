import requests
from bs4 import BeautifulSoup
import pandas as pd 
from datetime import datetime 

url = 'http://www.koeri.boun.edu.tr/scripts/lasteq.asp'

r = requests.get(url)
html_doc = r.text

# create a BeautifulSoup object and prettify it
soup = BeautifulSoup(html_doc)
pretty_soup = soup.prettify()

# create txt file 
with open('quakes.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(str(soup.find_all('pre')))

file = open('quakes.txt', 'r')
table = file.readlines()
del table[0:10]
file.close()


# write txt file 

file_out = open('quakes.txt','w')
file_out.writelines(table)
file_out.close()


# convert txt to csv for cleaning
def txt_to_csv(textfile):

	df = pd.read_fwf(textfile, colspecs = 'infer' )
	df.to_csv('quakes_raw.csv')

txt_to_csv('quakes.txt')


# cleaning and export .csv file with timestamp 
def clean_quakes_csv(quakes_raw_csv):

	df = pd.read_csv(quakes_raw_csv, header=0, usecols = range(1,8), skiprows =[1,2,3])
	
	# take every second row (others are NaN)
	df = df.iloc[::2]

	df.rename(columns = {'MD   ML   Mw': 'Magnitude'}, inplace = True)

	df['Magnitude']= df['Magnitude'].str.replace(r'\-.-', '')

	df.to_csv('quakes_cleaned_' + datetime.now().strftime('%y%m%d-%H%M') + '.csv')

clean_quakes_csv('quakes_raw.csv')

