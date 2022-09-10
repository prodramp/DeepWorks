import gradio as gr
from imageprocessui import ImageProcessUI


if __name__ == '__main__':
    my_app = gr.Blocks()
    img_ui = ImageProcessUI(my_app)
    img_ui.create_application_ui()
    img_ui.launch_ui()


