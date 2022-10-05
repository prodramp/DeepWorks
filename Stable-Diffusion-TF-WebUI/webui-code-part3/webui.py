import gradio as gr
from backend import ProcessPrompt


if __name__ == '__main__':
    sd_ui_obj = gr.Blocks()
    sd_class_obj = ProcessPrompt(sd_ui_obj)
    sd_class_obj.generate_ui()
    sd_class_obj.launch_ui()
