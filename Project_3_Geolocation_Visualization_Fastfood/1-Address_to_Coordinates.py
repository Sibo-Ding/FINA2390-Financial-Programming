# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 22:37:40 2022

@author: Sibo Ding
"""

'''
This code convert addresses to coordinates using Google API.
Import and export .csv file using Pandas.
References:
https://www.natasshaselvaraj.com/a-step-by-step-guide-on-geocoding-in-python/
https://developers.google.com/maps/documentation/geocoding/overview
'''

import pandas as pd
import googlemaps

def add_to_coor(csv_in, csv_out):
    df = pd.read_csv(csv_in)  # Import .csv file

    # Add latitude and longitude of each address into two lists
    list_lat = []
    list_lng = []
    for i in range(len(df)):
        # Select an address in dataframe
        # Convert the address to latitude and longitude using Google API
        # "g": A list containing multi-level dictionaries and lists,
        # with composite geolocation info
        g = gmaps_key.geocode(df['address'][i])
        lat = g[0]['geometry']['location']['lat']
        lng = g[0]['geometry']['location']['lng']
        list_lat.append(lat)
        list_lng.append(lng)
        
    # Add two "lat" and "lng" columns
    df['lat'] = list_lat
    df['lng'] = list_lng
    df.to_csv(csv_out, index=False)  # Export .csv file


if __name__ == '__main__':
    # Obtain Google API key
    gmaps_key = googlemaps.Client(key='Fill your key')
    add_to_coor('sb_address.csv', 'sb_coordinates.csv')
