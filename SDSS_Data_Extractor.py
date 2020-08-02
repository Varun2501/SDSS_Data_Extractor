import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from astropy.coordinates import SkyCoord
from astroquery.sdss import SDSS
import astropy.units as u

def get_value(objid, specobjid, req_par):

    #This function finds the value of the req_par that you entered and finds ist corresponding value

    response = requests.get('http://skyserver.sdss.org/dr16/en/tools/explore/DisplayResults.aspx?name=stellarMassFSPSGranEarlyDust&id=%s&spec=%s'%(objid, specobjid))
    soup = BeautifulSoup(response.text, features='html5lib')

    tables = soup.find_all('table')
    tabs_data = []

    for table in tables:
            
        tab_data = [[cell.text for cell in row.find_all(["td",{'class':['t']}])] for row in table.find_all("tr")]
        tabs_data.append(tab_data)

    tab_len = len(tabs_data)
    tab_id = tab_len-1
    par_name = str(req_par)

    for i in range(len(tabs_data[tab_id])):
        if tabs_data[tab_id][i][0] == par_name:
            print(tabs_data[tab_id][i][1])
            return tabs_data[tab_id][i][1]

    return 0

def load_data(catalog=None):

    #Load in your catalog here and pass the object index/number, ra, dec in the same order
    #The object index is to keep track of the order of the objects
    #An example is given below

    if catalog is None:
        df = pd.read_csv('Catalog.csv')
        print(df.head())
        return (df['Index'], df['RA'], df['DEC'])


def save_data(index, ra, dec, req_par):

    output_file = 'Result.dat'

    #This function takes in coordinates and finds their SDSS objid and specobjid
    #The objid and specobjid is needed to find the required parameters
    #The required parameter is then extracted and saved on to a dat file

    for i in range(len(index)):
        
        c = SkyCoord(ra=ra[i], dec=dec[i], unit=(u.deg, u.deg), frame='icrs')
        result_SDSS=None
        try:
            result_SDSS = SDSS.query_region(c, spectro=True, radius='3s')
        
        except:
            print('Failed to query SDSS - ',i)
        if result_SDSS is None:
            print(i)

        if result_SDSS is not None:

            objid = str(result_SDSS['objid'][0])   # Find SDSS objid
            specobjid = str(result_SDSS['specobjid'][0]) # Find SDSS specobjid

            par_value = get_value(objid, specobjid, req_par) # Calls the webscrapping function to extract the value of the required parameter

            f = open(output_file,"a")
            f.write('%d %f %f %f\n'%(index[i], ra[i], dec[i], par_value))
            f.close()
            print('%d %f %f %f'%(index[i], ra[i], dec[i], par_value))

    return None

'''Make sure that you have added the source catalog properly
This program will run for FSPS GranEarlyDust but if you want for other ports just change the name of the port in Line 11
Enter name of the required parameter you want to find Eg: age, mass, ssfr etc.'''

print('Enter parameter name: ')
req_par = input()

index, ra, dec = load_data()
save_data(index, ra, dec, req_par)