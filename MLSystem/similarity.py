import numpy as np
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def data_preparing():
    original_dataframe = pd.read_csv('./data/users_dataframe.csv')
    columns = ['Age', 'Worktimes', 'Schedules', 'Studies level', 'Pets', 'Cooking', 'Sport', 'Smoking', 'Organized']
    dataframe = original_dataframe[columns]
    return dataframe, original_dataframe

def data_checking(dataframe):
    for col in dataframe.columns:
        if dataframe[col].isnull().sum() > 0:
            print(f"Missing values in {col} column")
        else:
            print(f"No missing values in column {col}")

def encoder_matrix(dataframe, min_range, max_range):
    encoder = OneHotEncoder(sparse_output = False)
    data_encoded = encoder.fit_transform(dataframe)
    encoded_feature_names = encoder.get_feature_names_out()

    matriz_s = np.dot(data_encoded, data_encoded.T)
    
    min_original = np.min(matriz_s)
    max_original = np.max(matriz_s)
    matriz_reescalada = ((matriz_s-min_original) / (max_original - min_original))*(max_range - min_range) + min_range

    new_similarity_matrix = pd.DataFrame(matriz_reescalada, index = dataframe.index, columns = dataframe.index)
    return new_similarity_matrix

