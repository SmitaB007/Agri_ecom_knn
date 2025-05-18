from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
import os
from django.conf import settings
import pandas as pd
from .models import UserPurchase
from sklearn.neighbors import NearestNeighbors
import numpy as np




def checksum():
   purchases = UserPurchase.objects.all().values('user_id','product_id')

   df = pd.DataFrame(list(purchases))
   df = df.drop_duplicates(subset=['user_id', 'product_id'])
   df['interaction'] = 1
   user_product_matrix = df.pivot(index='user_id', columns='product_id', values='interaction').fillna(0).astype(int)
   print(user_product_matrix)

   user_product_matrix = user_product_matrix.to_numpy()

   knn = NearestNeighbors(n_neighbors=3,metric='cosine')
   knn.fit(user_product_matrix)
   return user_product_matrix,knn,df

def get_recommendation(user_id):
    user_product_matrix,knn,df =checksum()
    user_ids = df['user_id'].unique()  
    user_id_to_index = {user_id: idx for idx, user_id in enumerate(user_ids)}
    print(user_id_to_index)
    matrix_index = user_id_to_index[user_id]
    distances,indices = knn.kneighbors(user_product_matrix[matrix_index].reshape(1,-1))
    print(distances)
    print(indices)
    similar_user_ids = indices.flatten()


    recommended_products = []
    for s in similar_user_ids:
        s_purchases = user_product_matrix[s]
        bought_products = np.where(s_purchases == 1)[0]
        recommended_products.extend(bought_products)
    
    # user_purchase = user_product_matrix[matrix_index]
    # print(user_purchase)
    # already_bought_products = np.where(user_purchase == 1)[0]
    # recommended_products = list(set(recommended_products)-set(already_bought_products))
    print(list(recommended_products))
      
    return recommended_products
