import os
import numpy as np 			        
import pandas as pd 			    
import random
import matplotlib.pyplot as plt
from sklearn import datasets


class Function():
    def __init__(self, file_name='iris.csv'):
        self.directory_name='datacademy_demo'
        self.file_name = file_name
        self.data = datasets.load_iris()
        self.working_dir = os.path.join(os.getcwd().lower().split(self.directory_name)[0], self.directory_name, "Modules", "M4_ML", "src")
        self.answer_dir = os.path.join(os.getcwd().lower().split(self.directory_name)[0], self.directory_name, "Modules", "M4_ML")

        self.imputed_outlier_index = 72

        self.iris = self.data_modification()
        self.preprocessed_dataframe = None
        self.supervised_dataframe = None
        self.created_pipeline = None


    def data_modification(self) -> pd.DataFrame:
        """
        Create and modify a version of the Iris dataset suitable for the learning task.

        Returns:
            pd.DataFrame: Modified Iris dataset for learning tasks.
        """
        # Transform to Pandas DataFrame
        iris = pd.DataFrame(data=self.data.data, columns=self.data.feature_names)
        
        # Create NaN values (missing values) in petal width
        none_values = [random.randint(0, 149) for _ in range(5)]
        iris.loc[none_values, 'petal length (cm)'] = None

        # Add additional column for categorical features
        iris['state'] = np.random.choice(['wet', 'dry'], iris.shape[0])

        # Transform one column its measure unit
        iris = iris.rename(columns={'sepal width (cm)':'sepal width (mm)'})
        iris['sepal width (mm)'] = iris['sepal width (mm)'].apply(lambda x: x*10)

        # Add outlier to the DataFrame
        index_val = self.imputed_outlier_index
        value = iris.loc[index_val, 'sepal length (cm)']
        new_value = float(str(value).split('.')[0] + '0.' + str(value).split('.')[-1])
        iris.loc[index_val, 'sepal length (cm)'] = new_value

        return iris


    def remove_0_in_outlier(self, outlier_value:float) -> None:
        """
        Adjusts the outlier value by removing the 0 that is inserted by accident.

        Args:
            outlier_value (float): Value of the outlier to be removed.
        """
        # Verwijder de 0 in de outlier value en update the DataFrame
        location_outlr = self.iris[self.iris['sepal length (cm)'] == outlier_value].index[0]

        # get index of first occurrence of '0'
        id = str(outlier_value).index('0')

        # remove the first occurrence of '0'
        new_value = float(str(outlier_value)[:id] + str(outlier_value)[id+1:])

        # Append the new value to the DataFrame
        self.iris.loc[self.imputed_outlier_index, 'sepal length (cm)'] = new_value


    def prepare_supervised_learning(self) -> None:
        """
        Remove the added column created during clustering and add a target column containing all labels belonging to the Iris data.
        """
        # Copy the dataset used for unsupervised learning onto a class variable for later use.
        self.unsupervised_dataset = self.iris.copy(deep=True)

        # Recreate dataset and add the target column.
        self.iris = self.data_modification()
        self.iris['target'] = self.data.target.tolist()


    def get_unsupervised_dataset(self) -> pd.DataFrame:
        """
        Return the saved unsupervised dataset that is saved when preparing the supervised learning set.

        Returns:
            pd.DataFrame: Preprocessed Pandas DataFrame containing the data used for unsupervised learning.
        """
        return self.unsupervised_dataset


    def execute_function(self, answer, exercise:str=None, save_output:bool=True) -> str:
        if not isinstance(answer, pd.DataFrame):
            answers_df = pd.DataFrame(data={
                "answer": [answer]})
        else:
            answers_df = answer
        
        if save_output:
            if not os.path.exists(os.path.join(self.answer_dir, "answers")):
                os.mkdir(os.path.join(self.answer_dir, "answers"))
            if exercise is None:
                return "Please provide the exercise name in the function if you want to save the outputs."
            answers_df.to_csv(os.path.join(self.answer_dir, "answers", f"{exercise}.csv"), sep=";", index=False)
        
        return "Answer successfully submitted!"


    def save_preprocessed_dataframe(self, preprocessed_df:pd.DataFrame) -> str:
        self.preprocessed_dataframe = preprocessed_df
    
        return "Successfully saved the preprocessed DataFrame."


    def save_supervised_dataframe(self, supervised_df:pd.DataFrame) -> str:
        self.supervised_dataframe = supervised_df
        
        return "Successfully saved the supervised DataFrame."

    def save_pipeline_for_later_evaluation(self, pipeline, df:pd.DataFrame):
        self.created_pipeline = pipeline

        return "Successfully saved your created pipeline."
