from datasetmanager import DatasetManager
from datasetselector import DatasetSelector
import gradio as gr
import seaborn as sns
import pandas as pd


def previous_dataset_code():
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
            ds_updated.filter_dataset_by_value('carat', 1, "upper")
            print("Dataset length: {}".format(ds_updated.dataset_length()))
            ds_updated.filter_dataset_by_category('cut', ['Premium'])
            ds_updated.filter_dataset_by_category('color', ['A', 'B', 'C', 'D', 'E'])
            print("Dataset length: {}".format(ds_updated.dataset_length()))
        elif dataset_name == 'iris':
            ds_updated = DatasetManager(dataset_name, ds_manager.dataframe)
            ds_updated.filter_dataset_by_value('sepal length (cm)', 5.5, "upper")
            print("Dataset length: {}".format(ds_updated.dataset_length()))
            ds_updated.filter_dataset_by_value('sepal width (cm)', 3.5, "upper")
            print("Dataset length: {}".format(ds_updated.dataset_length()))
        elif dataset_name == 'planets':
            ds_updated = DatasetManager(dataset_name, ds_manager.dataframe)
            ds_updated.filter_dataset_by_value('mass', 1, "upper")
            print("Dataset length: {}".format(ds_updated.dataset_length()))
            ds_updated.filter_dataset_by_category('method', ['Radial Velocity'])
            ds_updated.filter_dataset_by_category('method', ['Imaging', 20, 'Eclipse Timing Variations',
                                                             'Transit', 'Astrometry'])
            print("Dataset length: {}".format(ds_updated.dataset_length()))

        ds_manager.render_dataset_values("df")


def read_dataset(ds_library, dataset_name, limit_type, records_limit):
    ds_selector = DatasetSelector(ds_library, dataset_name)
    df = ds_selector.get_dataset()
    if not df.empty:
        ds_manager = DatasetManager(dataset_name, df)
        ds_manager.set_dataset_limit(records_limit, limit_type)
        return ds_manager.dataframe

    return pd.DataFrame({"Status": ["Error: Bad dataset name"]})


def gradio_ui_handler(ds_library, ds_name, row_limit_type, row_count):
    df = read_dataset(ds_library.lower(),
                      ds_name,
                      row_limit_type.lower(),
                      row_count)
    return df


if __name__ == '__main__':
    my_app = gr.Interface(
        gradio_ui_handler,
        [
            gr.Dropdown(label="Please select dataset library",
                        value="Seaborn",
                        choices=["Seaborn", "Scikit-learn"]),
            gr.Textbox(label="Enter the dataset name", lines=1),
            gr.Radio(label="Please select the row sampling type",
                     choices=["Top", "Bottom", "Sample"],
                     value="Top"),
            gr.Slider(label="Please select rows in your dataset",
                      minimum=1,
                      maximum=1000,
                      value=5,
                      step=5)
        ],
        "dataframe"
    )

    my_app.launch()
    # print("Let's go")
    # print("gradio Version {}".format(gr.__version__))
