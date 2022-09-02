import seaborn as sns
from dataset import load_dataset_from_sns, get_columns, get_column_data_types, \
    get_dataset_by_value, get_dataset_by_category


def get_dataset(dataset_name):
    records_limit = 1000
    limit_type = 'sample'
    df = load_dataset_from_sns(dataset_name, records_limit, limit_type)

    if dataset_name == 'diamonds':
        df = get_dataset_by_value(df, 'carat', 2, "upper")
        df = get_dataset_by_category(df, 'cut', ['Premium'])
        df = get_dataset_by_category(df, 'color', ['A', 'B', 'C', 'D', 'E'])
    elif dataset_name == 'planets':
        df = get_dataset_by_value(df, 'mass', 1, "upper")
        # df = get_dataset_by_category(df, 'method', ['Radial Velocity'])
        df = get_dataset_by_category(df, 'method', ['Imaging', 20,
                                                    'Eclipse Timing Variations',
                                                    'Transit',
                                                    'Astrometry'])

    columns = get_columns(df)
    print("Column List: {}".format(columns))
    columns = get_column_data_types(df)
    print("Column Data Types List: {}".format(columns))
    print("Dataframe records: {}".format(len(df)))
    result_type = 'df'
    if result_type == 'df':
        print(df)
    else:
        print(df.to_json(orient='records'))


def process_selected_dataset(dataset_name):
    all_sns_datasets = sns.get_dataset_names()
    if dataset_name in all_sns_datasets:
        get_dataset(dataset_name)


if __name__ == '__main__':
    process_selected_dataset('planets')
    print("Let's go")
