## Sample Gradio Code to Try in pieces ##

```
def step1(value):
    return value
demo = gr.Interface(
    step1,
    "label",
    "label",
).launch()
```

----------------------

```
def step1(value):
    return value
demo = gr.Interface(
    step1,
    "label",
    "text",
).launch()
```

--------------------
```
def step1(value):
    return "Avkash" <========== Change it to value later
demo = gr.Interface(
    step1,
    "text",
    "text",
).launch()
```
---------------------
```
def step1(value):
    return df
demo = gr.Interface(
    step1,
    "label",
    "dataframe",
).launch()
```

------------------
```
def step1(ds_name):
    if ds_name in ["diamonds", "planets", "titanic"]:
      return sns.load_dataset(ds_name)
    return pd.DataFrame({"Status": ["Error: Bad Dataset Name"]})

def collect_gradio_ui_feedback(ds_name):
    return step1(ds_name)

demo = gr.Interface(
    collect_gradio_ui_feedback,
    [
        gr.Textbox(label="Select Dataset", lines=1)
    ],
    "dataframe",
).launch()
```
-------------------
```
def step1(ds_library, ds_name, rows_limit):
    if ds_library == "Seaborn":
      if ds_name in ["diamonds", "planets", "titanic"]:
        df = sns.load_dataset(ds_name)
        if not df.empty:
          df = df.head(rows_limit)
          return df
    elif ds_library == "Scikit-learn":
      if ds_name in ["iris", "digits"]:
        if ds_name == 'iris':
          iris = load_iris()
          dataframe = pd.DataFrame(data=iris.data, columns=iris.feature_names)
          return dataframe
        elif ds_name == "digits":
          digits = load_digits()
          dataframe = pd.DataFrame(data=digits.data, columns=digits.feature_names)
          return dataframe
    return pd.DataFrame({"Status": ["Error: Bad Dataset Name"]})

def collect_gradio_ui_feedback(ds_library, ds_name, rows_limit):
    return step1(ds_library, ds_name, rows_limit)

demo = gr.Interface(
    collect_gradio_ui_feedback,
    [
        gr.Dropdown(["Seaborn", "Scikit-learn"]),
        gr.Textbox(label="Select Dataset", lines=1),
        gr.Slider(1, 1000, value=5),   
    ],
    "dataframe",
).launch()
```
