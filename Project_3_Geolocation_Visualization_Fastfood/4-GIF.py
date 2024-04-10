# -*- coding: utf-8 -*-
"""
Created on Sat Nov  21 11:26:34 2022

@author: Sibo Ding
"""

'''
This code generates animated scatter plots using mpl.animation.
Calculates k-means clustering data using sklearn.
Import .csv file with coordinates using Pandas.
References:
https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot
https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
https://eli.thegreenplace.net/2016/drawing-animated-gifs-with-matplotlib/
https://stackoverflow.com/questions/68960005/saving-an-animated-matplotlib-graph-as-a-gif-file-results-in-a-different-looking
'''

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Combine "lng" list and "lat" list into a tuple
df = pd.read_csv('sb_coordinates.csv')
x = df['lng'].to_list()
y = df['lat'].to_list()
coor = [*zip(x, y)]

# Create a figure with one subplot
fig, ax = plt.subplots()
# Create the initial scatter plot (2 clusters)
# Train K-means model
kmeans = KMeans(n_clusters=2)
kmeans.fit(coor)
scat = plt.scatter(x, y, c=kmeans.labels_, s=10)  # "s": size

# Calculate color data
max_clusters = 15
color_data = np.array([])
for cluster in range(2, max_clusters+1):
    # Train K-means model
    kmeans = KMeans(n_clusters=cluster)
    kmeans.fit(coor)
    # Append kmeans labels of each cluster number to "color_data" array
    # /cluster: Convert data to range [0,1)
    color_data = np.append(color_data, kmeans.labels_ / cluster)
# Reshape: No. of clusters * No. of coordinates
color_data = color_data.reshape(max_clusters-1, len(coor))


# Update scatter plots after the initial plot
def update_plot(i, data, scat):
    scat.set_array(data[i])  # Update colors
    ax.set_title(f'No of clusters: {i+2}')  # Update title
    return scat


# mpl animation
ani = FuncAnimation(fig, update_plot, frames=range(max_clusters-1), 
                    fargs=(color_data, scat))
# Export .gif file; dpi: dots per inch; fps: frames per second
ani.save('sb_gif.gif', dpi=300, writer=PillowWriter(fps=0.5))
