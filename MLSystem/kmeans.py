import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from  sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from scipy.spatial.distance import euclidean
import joblib

class k_means_algo():
    


    def data_preparing(self,person):
       
        #DATAFRAME WITH DATA

        
        new_dataframe = pd.DataFrame(columns=person)
        print(new_dataframe.columns)

        original_dataframe = pd.read_csv('./MLSystem/data/users_dataframe.csv')
        print(original_dataframe.columns)

        id = original_dataframe["id"].iloc[-1]
        last_id = id + 1
        
        new_row_data = [last_id, "John", "Doe", 30, "john.doe@example.com", "Morning", "Night", 
                "Bachelor", "Yes", "Yes", "Yes", "No", "Yes"]

        
        new_row_dataframe = pd.DataFrame([new_row_data], columns=person)
        self.result_data = pd.concat([original_dataframe, new_row_dataframe]).set_index("id")
        
        

        
        
        


    def data_checking(self,dataframe):
        for col in dataframe.columns:
            if dataframe[col].isnull().sum() > 0:
                print(f"Missing values in {col} column")
            else:
                print(f"No missing values in column {col}")

    def reshape_playground(self,data):
        print(f"Data shape {data.shape}")
        data[50].reshape(17,1)
        print(data.shape)

    def forward_algorithm(self,dataframe,cluster_spec):
        cluster_spec = dataframe[0]
        kmeans = KMeans(n_clusters=4, random_state=42)
        result = kmeans.fit_predict(dataframe)
        print(result[1])
        print(result)

    def set_specific_cluster(self,dataframe,cluster_spec):
        cluster_spec = dataframe[cluster_spec]
        distances = [euclidean(cluster_spec,point) for point in dataframe]
        print(distances)

    def specific_cluster_kmeans(self):
        id = self.result_data["id"].iloc[-1]
        print(self.result_data)
        cluster_spec = self.result_data[id]
        cluster_spec = cluster_spec.reshape(1,17)
        print(cluster_spec.shape)
        kmeans = KMeans(n_clusters=1, init = cluster_spec, n_init = 1, random_state=42)
        data = kmeans.fit(dataframe)
        joblib.dump(kmeans, 'MLSystem/kmeans_model.pkl')
        

    
my_kmeans = k_means_algo()
person = ["id","Names","Surnames","Age","Email","Worktimes","Schedules","Studies level","Pets","Cooking","Sport","Smoking","Organized"]

my_kmeans.data_preparing(person)

#forward_algorithm(dataframe,50)
#set_specific_cluster(dataframe,50)
#my_kmeans.specific_cluster_kmeans()
