import gradio as gr
from backend import ProcessPrompt

if __name__ == '__main__':
    my_app = gr.Blocks()
    t2i = ProcessPrompt(my_app)
    t2i.create_application_ui()
    t2i.launch_ui()