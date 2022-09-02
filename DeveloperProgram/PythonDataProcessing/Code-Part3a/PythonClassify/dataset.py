import seaborn as sns
import pandas as pd

numeric_field_data_types = ['int', 'float', 'int64', 'float64']
correct_conditions = ['equal', 'lower', 'upper', "==", ">=", "<="]


def get_columns(df):
    """
    Getting the list of column names in the given dataframe
    :param df: the Input DataFrame
    :return: A list of column names as string.
    """
    column_list = df.columns.to_list()
    return column_list


def get_column_data_types(df):
    """
    A list of column datatypes
    :param df: Input dataframe
    :return: A list of column data types as List
    """
    column_types_list = df.dtypes.to_list()
    return column_types_list


def get_records_limit_by_type(df, records_limit, limit_type):
    limit_types = ['top', 'bottom', 'sample']
    if limit_type in limit_types:
        if limit_type == 'top':
            df = df.head(records_limit)
        elif limit_type == 'bottom':
            df = df.tail(records_limit)
        elif limit_type == 'sample':
            df = df.sample(records_limit)
    return df


def validate_field_name(df, field_name):
    all_columns = get_columns(df)
    field_name_validation = False
    if field_name in all_columns:
        field_name_validation = True
    return field_name_validation


def validate_field_type_value(field_value_type):
    field_value_validation = False
    if field_value_type in numeric_field_data_types:
        field_value_validation = True
    return field_value_validation


def validate_conditions(condition):
    field_operator_validation = False
    if condition in correct_conditions:
        field_operator_validation = True
    return field_operator_validation


def get_dataset_by_value(df, field_name, field_value, condition):
    # validate field name
    field_name_validation = validate_field_name(df, field_name)

    # validate field value
    field_value_validation = validate_field_type_value(type(field_value).__name__)

    # validate field type
    field_type_validation = validate_field_type_value(df[field_name].dtypes)

    # validate condition
    field_operator_validation = validate_conditions(condition)

    if field_name_validation and field_value_validation \
            and field_type_validation \
            and field_operator_validation:
        if condition in ['equal', "=="]:
            df = df.loc[df[field_name] == field_value]
        elif condition in ['lower', "<="]:
            df = df.loc[df[field_name] <= field_value]
        elif condition in ['upper', ">="]:
            df = df.loc[df[field_name] >= field_value]

    return df


def get_dataset_by_category(df, field_name, field_values):
    # validate field name
    field_name_validation = validate_field_name(df, field_name)

    # validate field value
    field_value_validation = False
    if len(field_values) > 0:
        # correct_count = 0
        # for each_field in field_values:
        #     field_value_type = type(each_field).__name__
        #     if field_value_type in ['str']:
        #         correct_count = correct_count + 1
        # if correct_count == len(field_values):
        #     field_value_validation = True
        # A single line inline code for the above commented code
        if len([item for item in field_values if type(item).__name__ in ['str']]) == len(field_values):
            field_value_validation = True

    valida_field_data_types = ['category', 'object']
    # validate field type
    field_type_validation = False
    field_type = df[field_name].dtypes
    if field_type in valida_field_data_types:
        field_type_validation = True

    if field_name_validation and field_value_validation \
            and field_type_validation:
        df = df[df[field_name].isin(field_values)]
    return df


def load_dataset_from_sns(ds_name, records_limit, limit_type):
    df = pd.DataFrame()
    if ds_name is not None:
        df = sns.load_dataset(ds_name)

    df = get_records_limit_by_type(df, records_limit, limit_type)

    return df

