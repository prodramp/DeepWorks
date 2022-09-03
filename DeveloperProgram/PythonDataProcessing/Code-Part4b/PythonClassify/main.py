from datasetmanager import DatasetManager
from datasetselector import DatasetSelector
import gradio as gr
import seaborn as sns
import pandas as pd

ds_manager = DatasetManager()


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
        global ds_manager
        ds_manager = DatasetManager(dataset_name, df)
        ds_manager.set_dataset_limit(records_limit, limit_type)
        df_info = ["Dataset length: {}".format(ds_manager.dataset_length())]
        ds_shape = ds_manager.dataset_shape()
        if len(ds_shape) == 2:
            df_info.append("Dataset Rows: {}  Columns: {}".format(ds_shape[0], ds_shape[1]))
        df_info.append("Dataset Columns: {}".format(ds_manager.get_columns()))
        df_info.append("Dataset Column Types: {}".format(ds_manager.get_column_data_types()))

        return df_info, ds_manager.dataframe

    return "Error in Dataset info", \
           pd.DataFrame({"Status": ["Error: Bad dataset name"]})


def gradio_ui_handler(ds_library, ds_name, row_limit_type, row_count):
    df_info, df = read_dataset(ds_library.lower(),
                      ds_name,
                      row_limit_type.lower(),
                      row_count)
    if type(df_info) == list and len(df_info) > 0:
        df_info = ",".join(df_info)
    return df_info, df


def get_filtered_dataset(filter_field, value_type, filter_value, numeric_filter_method):
    if value_type in ['Int', 'int']:
        filter_value = int(filter_value)
    elif value_type in ['float', 'Float']:
        filter_value = float(filter_value)
    ds_updated = DatasetManager(ds_manager.ds_name, ds_manager.dataframe)

    selected_field_datatype = ds_updated.dataframe[filter_field].dtype
    if selected_field_datatype is not None:
        if selected_field_datatype in ['str', 'object', 'category']:
            if type(filter_value) != list:
                filter_value = filter_value.split(",")
            ds_updated.filter_dataset_by_category(filter_field, filter_value)
            return ds_updated.dataframe
        else:
            ds_updated.filter_dataset_by_value(filter_field, filter_value, numeric_filter_method.lower())
            return ds_updated.dataframe

    return pd.DataFrame({"Status": ["Error: Data Filter Error"]})


def panel1_func(in1, in2):
    return "[x" + in1 + "y" + in2 + "]"


def get_filter_fields(input_1):
    all_field = ds_manager.get_columns()
    return gr.Dropdown.update(choices=all_field)


if __name__ == '__main__':

    my_app = gr.Blocks()
    with my_app:
        gr.Markdown("Data Analytics UI Demo")
        with gr.Tabs():
            with gr.TabItem("Dataset Details"):
                with gr.Row():
                    with gr.Column():
                        ds_lib = gr.Dropdown(label="Please select dataset library",
                                    value="Seaborn",
                                    choices=["Seaborn", "Scikit-learn"])
                        ds_name = gr.Textbox(label="Enter the dataset name", lines=1)
                        ds_sample_type = gr.Radio(label="Please select the row sampling type",
                                 choices=["Top", "Bottom", "Sample"],
                                 value="Top")
                        ds_row_count = gr.Slider(label="Please select rows in your dataset",
                                  minimum=1,
                                  maximum=1000,
                                  value=5,
                                  step=5)
                    with gr.Column():
                        output1_info = gr.Label(label="Dataset Info")
                        output2_df = gr.DataFrame()
                panel1_btn = gr.Button("Get Dataset Info")
            with gr.TabItem("Dataset Filter Details"):
                with gr.Row():
                    with gr.Column():
                        filter_label = gr.Label(label="Info",
                                                value="Please click Get Dataset "
                                                      "Fields button to fill the select field dropdown.")
                        filter_fields = gr.Dropdown(label="Select Field",
                                                    choices=[])
                        filter_value_type = gr.Radio(label="Filter Value Type",
                                                     value="Str",
                                                     choices=['Int', 'Str', 'Float'])
                        filter_value = gr.Textbox(label="Enter Filter Value")
                        numeric_filter_method = gr.Radio(label="Please select for numeric filter",
                                                     value="Upper",
                                                     choices=['Upper', 'Lower', 'Equal'])
                        filter_result = gr.DataFrame()
                panel2_btn1 = gr.Button("Get Dataset Fields")
                panel2_btn2 = gr.Button("Get Filtered Dataset")
        panel1_btn.click(
            gradio_ui_handler,
            [
                ds_lib,
                ds_name,
                ds_sample_type,
                ds_row_count
            ],
            [
                output1_info,
                output2_df
            ]
        )
        panel2_btn1.click(
            get_filter_fields,
            [
                filter_label
            ],
            [
                filter_fields
            ]
        )
        panel2_btn2.click(
            get_filtered_dataset,
            [
                filter_fields,
                filter_value_type,
                filter_value,
                numeric_filter_method
            ],
            [
                filter_result
            ]
        )
    my_app.launch()
