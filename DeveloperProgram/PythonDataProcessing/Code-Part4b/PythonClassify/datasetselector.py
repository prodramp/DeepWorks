import seaborn as sns
import pandas as pd
from sklearn.datasets import load_iris, load_digits, load_diabetes, load_wine, load_breast_cancer


class DatasetSelector(object):
    def __init__(self, ds_library, ds_name):
        self.name = "Dataset Selector"
        self.description = "This class load the dataset from a python library"
        self.ds_libraries = ['sns', 'seaborn', 'scikit-learn', 'sklearn'] # 'pandas',
        self.scikit_learn_datasets = ['iris', 'digits', 'wine', 'diabetes', 'breast_cancer',
                                      "breast-cancer", "breast cancer"]
        self.ds_name = ds_name
        self.ds_library = ds_library

    def get_dataset(self):
        dataframe = pd.DataFrame()
        if self.ds_library in self.ds_libraries:
            if self.validate_dataset_in_libraries():
                if self.ds_library in ['sns', 'seaborn']:
                    # load data set from seaborn library
                    dataframe = self.load_dataset_from_seaborn()
                elif self.ds_library in ['scikit-learn', 'sklearn']:
                    # load data set from seaborn library
                    if self.ds_name in self.scikit_learn_datasets:
                        dataframe = self.load_dataset_from_scikit_learn()
        return dataframe

    def validate_dataset_in_libraries(self):
        if self.ds_library in ['sns', 'seaborn']:
            if self.ds_name in sns.get_dataset_names():
                return True
        elif self.ds_library in ['scikit-learn', 'sklearn']:
            if self.ds_name in self.scikit_learn_datasets:
                return True
        return False

    def load_dataset_from_seaborn(self):
        dataframe = pd.DataFrame()
        try:
            dataframe = sns.load_dataset(self.ds_name)
        except:
            print("Error: Unable to load the dataset {}".format(self.ds_name))
        return dataframe

    def load_dataset_from_scikit_learn(self):
        dataframe = pd.DataFrame()
        try:
            if self.ds_name == 'iris':
                iris = load_iris()
                dataframe = pd.DataFrame(data=iris.data, columns=iris.feature_names)
            elif self.ds_name == 'wine':
                wine = load_wine()
                dataframe = pd.DataFrame(data=wine.data, columns=wine.feature_names)
            elif self.ds_name == 'digits':
                digits = load_digits()
                dataframe = pd.DataFrame(data=digits.data, columns=digits.feature_names)
            elif self.ds_name == 'diabetes':
                diabetes = load_diabetes()
                dataframe = pd.DataFrame(data=diabetes.data, columns=diabetes.feature_names)
            elif self.ds_name in ["breast_cancer", "breast-cancer", "breast cancer"]:
                breast_cancer = load_breast_cancer()
                dataframe = pd.DataFrame(data=breast_cancer.data, columns=breast_cancer.feature_names)
        except:
            print("Error: Unable to load the dataset {}".format(self.ds_name))
        return dataframe
