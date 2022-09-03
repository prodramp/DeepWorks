# Sample Gradio Code with Tabs #

```
def func1(in1, in2):
    return "Hello from Panel 11", "Hello from Panel 12"

def func2(in1):
    return "Hello from Panel 21"

my_app = gr.Blocks()

with my_app:
    gr.Markdown("Data analytics UI Demo")
    with gr.Tabs():
        with gr.TabItem("Dataset Details"):
            with gr.Row():
                with gr.Column():
                    in1 = gr.Label(label="label1")
                    in2 = gr.Label(label="label2")
                with gr.Column():
                    out1 = gr.Label(label="label1")
                    out2 = gr.Label(label="label2")
        panel_1 = gr.Button("Get Info 1")
        with gr.TabItem("Dataset Details"):
            with gr.Row():
                with gr.Column():
                    in1 = gr.Label(label="label1")
                    out1 = gr.Label(label="label1")
        panel_2 = gr.Button("Get Info 2")

    panel_1.click(
        func1,
        [
            in1,
            in2
        ],
        [
            out1,
            out2
        ]
    )
    panel_2.click(
        func1,
        [
            in1,
        ],
        [
            out1,
        ]
    )

```
