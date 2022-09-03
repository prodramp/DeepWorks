
class DatasetManager(object):
    def __init__(self, ds_name=None, dataframe=None):
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

    def validate_field_name(self, field_name):
        if field_name in self.get_columns():
            return True
        return False

    def validate_field_type_value(self, field_value_type):
        if field_value_type in self.numeric_field_data_types:
            return True
        return False

    def validate_conditions(self, condition):
        if condition in self.correct_conditions:
            return True
        return False

    def validate_columns_as_string(self, field_values):
        if len(field_values) > 0:
            if len([item for item in field_values
                    if type(item).__name__ in self.valid_category_field_types]) \
                    == len(field_values):
                return True
        return False

    def validate_field_type_exist(self, field_name):
        field_type = self.dataframe[field_name].dtypes
        if field_type in self.valid_field_data_types:
            return True
        return False

    def filter_dataset_by_value(self, field_name, field_value, condition):
        if self.validate_field_name(field_name) \
                and self.validate_field_type_value(type(field_value).__name__) \
                and self.validate_field_type_value(self.dataframe[field_name].dtypes) \
                and self.validate_conditions(condition):
            if condition in ['equal', "=="]:
                self.dataframe = self.dataframe.loc[self.dataframe[field_name] == field_value]
            elif condition in ['lower', "<="]:
                self.dataframe = self.dataframe.loc[self.dataframe[field_name] <= field_value]
            elif condition in ['upper', ">="]:
                self.dataframe = self.dataframe.loc[self.dataframe[field_name] >= field_value]

    def filter_dataset_by_category(self, field_name, field_values):
        if self.validate_field_name(field_name) \
                and self.validate_columns_as_string(field_values) \
                and self.validate_field_type_exist(field_name):
            self.dataframe = self.dataframe[self.dataframe[field_name].isin(field_values)]

    # New function
    def get_selected_field_data_type(self, field_name):
        if self.validate_field_name(field_name):
            return self.dataframe[field_name].dtypes

    def render_dataset_values(self, result_type):
        if result_type == 'df':
            print(self.dataframe)
        elif result_type == 'json':
            print(self.dataframe.to_json(orient='records'))
