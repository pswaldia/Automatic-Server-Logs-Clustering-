
import pandas as pd
import numpy as np
import re
import os
import pickle
import sys


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.feature_extraction.text import TfidfVectorizer

from cluster_utils import get_options, read_object, save_object , save_txt
from cluster_utils import clear_log, load_log
from cluster_utils import create_log_tag,create_sub_files,create_view,create_view_test

from collections import Counter
from collections import defaultdict


def tfidf_feature(documents, maxx, minn,documents_test):

    vectorizer = CountVectorizer(max_df=maxx, min_df=minn)
    transformer = TfidfTransformer()
    tf = vectorizer.fit_transform(documents)
    tf_test=vectorizer.transform(documents_test)
    tfidf_vectors_test = transformer.fit_transform(tf_test)
    tfidf_vectors = transformer.fit_transform(tf)
    words = vectorizer.get_feature_names()  # Get all the words in the word bag model
    weight = tfidf_vectors.toarray()
    save_txt("words", words)
    print("preprocessing finished......")

    #printing the shape of tfidf_vectors feature vector for test and train
    print(tfidf_vectors.shape,tfidf_vectors_test.shape)

    return tfidf_vectors,tfidf_vectors_test


#Calculate the distance between two vectors

def distance(a, b):
    sum = 0
    for i, j in zip(a, b):
        sum += (abs(i - j) ** 2)

    return sum ** 0.5

from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

def kmeans_cluster(data,data_test,n_clusters):
    kmeans = KMeans(init="k-means++", n_clusters=n_clusters,
                    n_jobs=-1, random_state=0).fit(data)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    
    labels_test=kmeans.predict(data_test)
    return labels,labels_test

def k_elbow(data,k_min,k_max,locate_elbow=True):
    model = KMeans(init="k-means++",n_jobs=-1)
    visualizer = KElbowVisualizer(model, k=(k_min,k_max), locate_elbow=True)
    visualizer.fit(data)        # Fit the data to the visualizer
    visualizer.poof()        # Draw/show/poof the data



def main():

    # data = load_log(filename)
    # kmeans_cluster(data)
    if not os.path.exists("{}_{}_cache".format(filename, clusters)):
        os.mkdir("{}_{}_cache".format(filename, clusters))
    
    filename_test='logs/private_test_set.txt'   #the filename of the test set on which prediction is to be done.
    
    documents = load_log(filename,chars)
    documents_test=load_log(filename_test,chars)
    

    tfidf_vectors,tfidf_vectors_test = tfidf_feature(documents,maxx, minn,documents_test)
    labels,labels_test = kmeans_cluster(tfidf_vectors,tfidf_vectors_test,clusters)

    # Instantiate the clustering model and visualizer to find the optimal number of clusters.
    data=tfidf_vectors    #train data
    k_elbow(data,2,20,locate_elbow=True)

    database, labels_info = create_log_tag(labels, filename)
    database_test,labels_info_test=create_log_tag(labels_test,filename_test)
    
    create_view(labels_info, database)
    create_view_test(labels_info_test, database_test)


if __name__ == '__main__':

    option_dict = get_options()
    filename = option_dict['filename']
    clusters = option_dict['clusters']
    maxx = option_dict['max']
    minn = option_dict['min']
    chars = option_dict['chars']

    main()
