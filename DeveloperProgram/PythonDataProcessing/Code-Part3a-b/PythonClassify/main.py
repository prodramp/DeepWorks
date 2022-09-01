from datasetmanager import DatasetManager
from datasetselector import DatasetSelector


if __name__ == '__main__':
    dataset_name = 'planets'
    ds_selector = DatasetSelector("sns", dataset_name)
    df = ds_selector.get_dataset()

    if not df.empty:
        records_limit = 1000
        limit_type = 'sample'
        ds_manager = DatasetManager(dataset_name, df)
        ds_manager.set_dataset_limit(records_limit, limit_type)

        print("Dataset length: {}".format(ds_manager.dataset_length()))

        ds_shape = ds_manager.dataset_shape()
        if len(ds_shape) == 2:
            print("Dataset Rows: {}  Columns: {}".format(ds_shape[0], ds_shape[1]))

        print("Dataset Columns: {}".format(ds_manager.get_columns()))

        print("Dataset Column Types: {}".format(ds_manager.get_column_data_types()))

        if dataset_name == 'diamonds':
            ds_updated = DatasetManager(dataset_name, ds_manager.dataframe)
            print("Dataset length: {}".format(ds_updated.dataset_length()))
        elif dataset_name == 'iris':
            ds_updated = DatasetManager(dataset_name, ds_manager.dataframe)
            print("Dataset length: {}".format(ds_updated.dataset_length()))
        elif dataset_name == 'planets':
            ds_updated = DatasetManager(dataset_name, ds_manager.dataframe)
            print("Dataset length: {}".format(ds_updated.dataset_length()))

        ds_manager.render_dataset_values("df")

    print("Let's go")
