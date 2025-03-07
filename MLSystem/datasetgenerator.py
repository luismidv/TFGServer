import pandas as pd
import numpy as np

from  sklearn.preprocessing import OneHotEncoder


def list_creator(list):
    
    new_list =[list[i] for i in np.random.randint(0,len(list), 10000)]
    return new_list

def data_generator():
    name = ['John', 'Michael', 'Derek', 'Nick', 'Lucas', 'Jorge', 'George', 'Miguel', 'Anthony', 'Antonio', 'Mario', 'Marie' , 'Luna', 'Maria', 'Albert', 'Louisa'
        'Loren', 'Josephine']
    surname = ['Bush', 'Smith', 'Jones', 'Williams', 'Brown','Taylor', 'Davies ', 'Evans ', 'Williams', 'Thomas ','Johnson', 'Roberts ', 'Lee ', 'Walker ', 'Wright'
           ,'Robinson ', 'Thompson ', 'White', 'Hughes ', 'Edwards ']
    work_options = ['morning', 'night']
    morning_night = ['morning', 'night']
    studies_level = ['secondary', 'university']
    yes_no_questions = ['Yes', 'No']
    
    
    name_list = list_creator(name)
    surname_list = list_creator(surname)
    email_list = [name_list[i] + surname_list[i] + '@gmail.com' for i in range(len(name_list))]
    age_list = np.random.randint(18,35,10000)
    work_list = list_creator(work_options)
    morn_night_list = list_creator(morning_night)
    studies_list = list_creator(studies_level) 
    pets_list = list_creator(yes_no_questions)
    cooking_list = list_creator(yes_no_questions)
    sport_list = list_creator(yes_no_questions)
    smoking_list = list_creator(yes_no_questions)
    organized_list = list_creator(yes_no_questions)
    id_list = np.arange(1,10001,1)
    users_dataframe = pd.DataFrame(list(zip( name_list, surname_list, age_list, email_list, work_list, morn_night_list, studies_list, 
                                            pets_list, cooking_list, sport_list, smoking_list, organized_list)),
    columns =['Names', 'Surnames','Age', 'Email','Worktimes', 'Schedules', 'Studies level', 'Pets', 'Cooking', 'Sport', 'Smoking', 'Organized'])
    users_dataframe.index = id_list
    users_dataframe.index.name = "id"
    users_dataframe.to_csv('./MLSystem/data/users_dataframe.csv')
    print(users_dataframe)
    return users_dataframe

data_generator()
    





