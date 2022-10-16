import gradio as gr
from whisperui import WhisperModelUI


if __name__ == '__main__':
    my_app = gr.Blocks()
    ui_obj = WhisperModelUI(my_app)
    ui_obj.create_whisper_ui()
    ui_obj.launch_ui()

