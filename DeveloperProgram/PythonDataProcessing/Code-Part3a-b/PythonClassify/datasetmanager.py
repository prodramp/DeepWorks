
class DatasetManager(object):
    def __init__(self, ds_name, dataframe):
        self.name = "Dataset Manager Class"
        self.description = "This class manage all the dataset specific functions"
        self.ds_name = ds_name
        self.dataframe = dataframe
        self.limit_types = ['top', 'bottom', 'sample']
        self.numeric_field_data_types = ['int', 'float', 'int64', 'float64']
        self.correct_conditions = ['equal', 'lower', 'upper', "==", ">=", "<="]
        self.valid_category_field_types = ['str']
        self.valid_field_data_types = ['category', 'object']

    def set_dataset_limit(self, ds_limit, ds_limit_type):
        if ds_limit_type not in self.limit_types:
            return False
        if ds_limit_type == 'top':
            self.dataframe = self.dataframe.head(ds_limit)
        elif ds_limit_type == 'bottom':
            self.dataframe = self.dataframe.tail(ds_limit)
        elif ds_limit_type == 'sample':
            if ds_limit < self.dataset_length():
                self.dataframe = self.dataframe.sample(ds_limit)
            else:
                self.dataframe = self.dataframe.sample()

    def dataset_length(self):
        return len(self.dataframe)

    def dataset_shape(self):
        return self.dataframe.shape

    def get_columns(self):
        """
        Getting the list of column names in the given dataframe
        :param df: the Input DataFrame
        :return: A list of column names as string.
        """
        column_list = self.dataframe.columns.to_list()
        return column_list

    def get_column_data_types(self):
        """
        A list of column datatypes
        :param df: Input dataframe
        :return: A list of column data types as List
        """
        column_types_list = self.dataframe.dtypes.to_list()
        return column_types_list

    # todo: Added next
    # filter dataset by value
    # filter dataset by category

    def render_dataset_values(self, result_type):
        if result_type == 'df':
            print(self.dataframe)
        elif result_type == 'json':
            print(self.dataframe.to_json(orient='records'))
