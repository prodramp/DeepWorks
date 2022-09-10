import gradio as gr
import numpy as np
from PIL import Image

image_global = np.zeros([10,10,3], dtype=np.uint8)


def process_source_image(image_source):
    image_out = image_source
    global image_global
    image_global = image_source
    img_info = []
    if image_source is not None:
        if len(image_source.shape) == 3:
            img_info.append({"Height: ": image_source.shape[0]})
            img_info.append({"Width: ": image_source.shape[1]})
            img_info.append({"Channels: ": image_source.shape[2]})
        if len(image_source.shape) == 2:
            img_info.append({"Height: ": image_source.shape[0]})
            img_info.append({"Width: ": image_source.shape[1]})
    return str(img_info), image_out


def image_resizer(img_height, img_width):
    image_out = Image.fromarray(image_global)
    image_out = image_out.resize((img_width, img_height))
    return image_out


def image_convert_grayscale():
    image_out = Image.fromarray(image_global)
    image_out = image_out.convert('L')
    return image_out


def image_process_alpha_channel(alpha_value):
    image_out = Image.fromarray(image_global)
    image_out.putalpha(alpha_value)
    return image_out


def image_process_scratchpad(scratch_img):
    global image_global
    image_global = scratch_img
    image_out = Image.fromarray(scratch_img)
    return image_out


def show_3_channels():
    img_red = img_green = img_blue = image_global
    if len(image_global.shape) == 3 and image_global.shape[2] == 3:
        red_img = np.zeros(image_global.shape)
        red_channel = image_global[:, :, 0]
        red_img[:, :, 0] = red_channel

        green_img = np.zeros(image_global.shape)
        green_channel = image_global[:, :, 1]
        green_img[:, :, 1] = green_channel

        blue_img = np.zeros(image_global.shape)
        blue_channel = image_global[:, :, 2]
        blue_img[:, :, 2] = blue_channel

        img_red = Image.fromarray(red_img.astype(np.uint8))
        img_green = Image.fromarray(green_img.astype(np.uint8))
        img_blue = Image.fromarray(blue_img.astype(np.uint8))

    return img_red, img_green, img_blue,


class ImageProcessUI(object):
    def __init__(self, ui_obj):
        self.name = "Image Processor UI"
        self.description = "This class is designed to build UI for our application"
        self.ui_obj = ui_obj

    def create_application_ui(self):
        with self.ui_obj:
            gr.Markdown("Image Processing Application UI with Gradio")
            with gr.Tabs():
                with gr.TabItem("Select your image"):
                    with gr.Row():
                        with gr.Column():
                            img_source = gr.Image(label="Please select source Image")
                            source_image_loader = gr.Button("Load above Image")
                        with gr.Column():
                            output_label = gr.Label(label="Image Info")
                            img_output = gr.Image(label="Image Output")
                with gr.TabItem("Resize your Image"):
                    with gr.Row():
                        with gr.Column():
                            resize_label = gr.Label(label="Select your image height and width")
                            image_height = gr.Slider(10, 1000, label="Image Height", value=100)
                            image_width = gr.Slider(10, 1000, label="Image Width", value=100)
                            image_resize_btn = gr.Button("Resize Image")
                        with gr.Column():
                            img_resize_output = gr.Image(label="Resized Image Output")
                with gr.TabItem("Image as Grayscale"):
                    with gr.Row():
                        with gr.Column():
                            resize_label = gr.Label(label="Source image as GrayScale",
                                                    value="GRAYSCALE IMAGE")
                            img_gray_output = gr.Image(label="Grayscale Image Output")
                            image_grayscale_btn = gr.Button("Grayscale Your Image")
                with gr.TabItem("Image with Red, Green and Blue Channels"):
                    with gr.Row():
                        with gr.Column():
                            rgb_label = gr.Label(label="Source image with 3 channels",
                                                    value="RED, GREEN and BLUE IMAGE CHANNELS")
                    with gr.Row():
                        with gr.Column():
                            rgb_red_label = gr.Label(label="", value="RED CHANNELS")
                            img_red_output = gr.Image(label="Image as Red Channel")
                        with gr.Column():
                            rgb_green_label = gr.Label(label="", value="GREEN CHANNELS")
                            img_green_output = gr.Image(label="Image as Green Channel")
                        with gr.Column():
                            rgb_blue_label = gr.Label(label="", value="BLUE CHANNELS")
                            img_blue_output = gr.Image(label="Image as Blue Channel")
                    image_3channels_btn = gr.Button("Show 3 Channels in Image")
                with gr.TabItem("Image with Alpha Channel"):
                    with gr.Row():
                        with gr.Column():
                            alpha_channel_label = gr.Label(label="Source image",
                                                    value="IMAGE WITH ALPHA CHANNEL")
                            alpha_channel_value = gr.Slider(1, 256, label="Alpha Channel", value=128)
                            img_alpha_channel_output = gr.Image(label="Image with Alpha Channel Output")
                            image_alpha_channel_btn = gr.Button("Image with Alpha Channel")
                            alpha_channel_value.change(
                                image_process_alpha_channel,
                                inputs=[alpha_channel_value],
                                outputs=[img_alpha_channel_output]
                            )
                with gr.TabItem("Image with Scratchpad"):
                    with gr.Row():
                        with gr.Column():
                            img_scratch_pad_src = gr.Sketchpad(label="Draw your image")
                            scratch_pd_btn = gr.Button("Update Scribble Image")
                        with gr.Column():
                            img_scratch_pad_out = gr.Image(label="Scribbled Output")

            source_image_loader.click(
                process_source_image,
                [
                    img_source
                ],
                [
                    output_label,
                    img_output
                ]
            )
            image_resize_btn.click(
                image_resizer,
                [
                    image_height,
                    image_width
                ],
                [
                    img_resize_output
                ]
            )
            image_grayscale_btn.click(
                image_convert_grayscale,
                [

                ],
                [
                    img_gray_output
                ]
            )
            image_3channels_btn.click(
                show_3_channels,
                [

                ],
                [
                    img_red_output,
                    img_green_output,
                    img_blue_output
                ]
            )
            image_alpha_channel_btn.click(
                image_process_alpha_channel,
                [
                    alpha_channel_value
                ],
                [
                    img_alpha_channel_output
                ]
            )
            scratch_pd_btn.click(
                image_process_scratchpad,
                [
                    img_scratch_pad_src
                ],
                [
                    img_scratch_pad_out
                ]
            )

    def launch_ui(self):
        self.ui_obj.launch()


