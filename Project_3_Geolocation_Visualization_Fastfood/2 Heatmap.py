# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 23:00:50 2022

@author: Sibo Ding
"""

'''
This code plots heatmap based on coordinates using Google API.
Import .csv file using Pandas; export .html file.
References:
https://www.storybench.org/how-to-build-a-heatmap-in-python/
https://jupyter-gmaps.readthedocs.io/en/latest/tutorial.html
https://jupyter-gmaps.readthedocs.io/en/latest/export.html
'''

import pandas as pd
import gmaps
from ipywidgets.embed import embed_minimal_html  # To export .html

def heatmap(csv_in, html_out):
    df = pd.read_csv(csv_in)  # Import .csv file
    locations = df[['lat', 'lng']]  # Filter "lat" and "lng" columns

    fig = gmaps.figure()  # Create an empty Google map figure
    heatmap_layer = gmaps.heatmap_layer(locations)  # Create a heatmap layer
    heatmap_layer.opacity = 0.75  # Adjust the opacity of heat
    fig.add_layer(heatmap_layer)  # Add heatmap layer

    embed_minimal_html(html_out, views=[fig])  # Export .html file


if __name__ == '__main__':
    # Obtain Google API key
    gmaps.configure(api_key='Fill your key')
    heatmap('sb_coordinates.csv', 'sb_heatmap.html')
