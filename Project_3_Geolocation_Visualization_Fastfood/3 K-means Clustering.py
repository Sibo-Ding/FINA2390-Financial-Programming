# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:09:18 2022

@author: Sibo Ding
"""

'''
This code calculates k-means clustering data using sklearn.
Plots inertia and clustering graphs using mpl.
Import .csv file with coordinates using Pandas.
References:
https://www.w3schools.com/python/python_ml_k-means.asp#:~:text=K%2Dmeans%20is%20an%20unsupervised,the%20variance%20in%20each%20cluster.
https://medium.com/chung-yi/ml%E5%85%A5%E9%96%80-%E4%BA%8C%E5%8D%81%E4%B8%80-knn%E8%88%87k-means%E5%B7%AE%E7%95%B0-7dc6ad0227fc
https://scikit-learn.org/stable/modules/clustering.html#k-means
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html
'''

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def k_means(csv_in, elbow_clusters, plot_clusters):
    df = pd.read_csv(csv_in)  # Import .csv file

    # Convert "lng" and "lat" columns to lists
    x = df['lng'].to_list()
    y = df['lat'].to_list()
    coor = [*zip(x, y)]  # Combine "lng" and "lat" into a tuple

#%% This part generates "elbow" graph, can be omitted to speed up.
    # Inertia: Within-cluster sum-of-squares criterion, 
    # measuring how internally coherent clusters are
    inertias = []
    for i in range(1, elbow_clusters+1):
        # Train K-means model
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(coor)
        # Add the inertia of each cluster number to a list
        inertias.append(kmeans.inertia_)
        
    # Plot the inertia list
    plt.plot(range(1, elbow_clusters+1), inertias, marker='o')
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()
    # Look for the "elbow" (where the inertia becomes more linear)

#%% Train K-means model
    kmeans = KMeans(n_clusters=plot_clusters)
    kmeans.fit(coor)

    # Plot different clusters; "c" means different colors
    # kmeans.lables_: An array of numbers ranging (0, num_clusters - 1),
    # indicating different clusters
    plt.scatter(x, y, c=kmeans.labels_)
    plt.title(f'No. of clusters: {plot_clusters}')
    plt.show()

if __name__ == '__main__':
    k_means('sb_coordinates.csv', 20, 7)
