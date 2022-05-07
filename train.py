
from re import S
from flask import Flask , jsonify

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.decomposition import TruncatedSVD

# Dataset link: https://www.kaggle.com/datasets/skillsmuggler/amazon-ratings#https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews

df = pd.read_csv(r"C:\Users\kinyah\Downloads\ratings_Beauty.csv" , low_memory=False)
#dtype={'user_id': int}

dfcopy = df.copy()
print(dfcopy.head())

print(dfcopy.shape)

#droping timestamp column
dfcopy.drop(['Timestamp'], axis=1,inplace=True)

print(dfcopy.Rating.max().T)

dfcopy.head()

dfcopy.Rating.value_counts()

with sns.axes_style('white'):
    g = sns.catplot("Rating", data=dfcopy, aspect=2.0,kind='count')
    g.set_ylabels("Total number of ratings")

print("Total data ")
print("="*50)
print("\nTotal no of ratings :",dfcopy.shape[0])
print("Total No of Users   :", len(np.unique(dfcopy.UserId)))
print("Total No of products  :", len(np.unique(dfcopy.ProductId)))


no_of_rating_per_product = dfcopy.groupby(by='ProductId')['Rating'].count().sort_values(ascending=False)
no_of_rating_per_product.head() 

average_rating = pd.DataFrame(dfcopy.groupby('ProductId')['Rating'].mean())
average_rating['ratingCount'] = pd.DataFrame(dfcopy.groupby('ProductId')['Rating'].count())
average_rating.sort_values('ratingCount', ascending=False).head()

ratings = dfcopy.head(10000)
print(ratings.shape)

ratings_utility_matrix = ratings.pivot_table(values='Rating', index='UserId', columns='ProductId', fill_value=0)
ratings_utility_matrix.head()



X = ratings_utility_matrix.T
print(X.head())

#making a copy of the data 
X1 = X

SVD = TruncatedSVD(n_components=10)
decomposed_matrix = SVD.fit_transform(X)
decomposed_matrix.shape

correlation_matrix = np.corrcoef(decomposed_matrix)
correlation_matrix.shape
#pcking a random index
i = X.index[40]

print("the product = ", i)

product_names = list(X.index)
product_ID = product_names.index(i)
print(product_ID)


correlation_product_ID = correlation_matrix[product_ID]
correlation_product_ID.shape


recommended_products = list(X.index[correlation_product_ID > 0.90])

# Removes the item already bought by the customer
recommended_products.remove(i) 

predictions = recommended_products[0:10]

app = Flask(__name__)

@app.route("/preds")
def preds():
    return { "predictions" : predictions } 


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(host='0.0.0.0', port=port)

