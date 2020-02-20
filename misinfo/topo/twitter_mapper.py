import pandas as pd
import kmapper as km
import numpy as np

from sklearn import ensemble, cluster
from sklearn.datasets import fetch_20newsgroups
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import Isomap
from sklearn.preprocessing import MinMaxScaler

print("fuck the system")

# Store the data frame,
df = pd.read_csv("ArsonEmergency_tweets.csv") # store a dataframe to be formatted for mapper
df2 = pd.read_csv("ArsonEmergency_tweets.csv") # store a copy to retain the original information to annotate the diagram


# turn some the numerical features into floats
df['date'] = df['date'].apply(lambda x: float(x[4:].replace("-", "")))
df['time'] = df['time'].apply(lambda x: float(x.replace(":", "")))
df['replies_count'] = df['replies_count'].apply(lambda x: float(x))
df['retweets_count'] = df['retweets_count'].apply(lambda x: float(x))
df['likes_count'] = df['likes_count'].apply(lambda x: float(x))


# split the indexing of features into numerical and categorical
numerical_features = [ 'created_at', 'time', 'date', 'replies_count', 'retweets_count', 'likes_count']
categorical_features = [ 'mentions', 'urls', 'hashtags']

# an array of tweet content strings
X_lang = df['tweet']
print("Tweets = ", X_lang)

mapper = km.KeplerMapper(verbose=2) # initialise kmapper


# project the tweet content strings into a metric space, based on the Tf_idf language distance, and embed in a lower dimensional vector space via SVD and IsoMap
projected_X_lang = mapper.fit_transform(X_lang,
    projection=[TfidfVectorizer(analyzer="char",
                                ngram_range=(1,6),
                                max_df=0.83,
                                min_df=0.05),
                TruncatedSVD(n_components=100,
                             random_state=1729),
                Isomap(n_components=3,
                       n_jobs=-1)],
    scaler=[None, None, MinMaxScaler()])

print("Projected_X_lang = ", projected_X_lang)


# make a lens from the numerical features
created = np.array(df['created_at'])
time = np.array(df['time'])
likes = np.array(df['likes_count'])
replies = np.array(df['replies_count'])
retweets = np.array(df['retweets_count'])

custom_lens = np.c_[created,time] # any combination of the above can be added. if there are n in total, the function maps each tweet into R^n, and splits up the image into n dim cubes

# Generate the abstract mapper graph based on the metric embedding and lens function
G = mapper.map(
    custom_lens,
    projected_X_lang,
    nr_cubes=20,
    remove_duplicate_nodes=True,
    overlap_perc=0.5,
    clusterer=cluster.AgglomerativeClustering(3))

# Visualise the graph using the mapper API, automatically outputs the HTML file 'mapper_visualisation_output.html'
_ = mapper.visualize(
    G,
    color_function=time, # the color_function can be replaced by any numpy array with shape (#data_points,).
    custom_tooltips = df2['tweet'], #
    lens = custom_lens,
    lens_names = ['Created At', 'Time of Day'],
    title="Twitter Misinformation: Time of Day"
)
