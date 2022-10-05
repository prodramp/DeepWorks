import os

import gradio as gr
from tensorflow import keras
from stable_diffusion_tf.stable_diffusion import StableDiffusion
import argparse
from PIL import Image
from transformers import pipeline
import json


def calculate_all_saved_images():
    img_save_folder = 'output'
    img_save_dir_full_path = os.getcwd() + "/" + img_save_folder

    image_files_list = [f for f in os.listdir(img_save_dir_full_path)
                             if os.path.isfile(img_save_dir_full_path + "/" + f)
                             and f.endswith(".png")]

    return len(image_files_list)


def find_image_file_node_in_json(image_file_name):
    json_content_file = "output_images.json"
    json_content_folder = "output"
    json_file_name_path = os.path.join(os.getcwd(), json_content_folder, json_content_file)

    json_file_data = open(json_file_name_path)
    json_image_data = json.load(json_file_data)
    if "images" in json_image_data:
        selected_json_node = [json_item for json_item in json_image_data['images']
                          if json_item['saved_image_name'] == image_file_name]
        if selected_json_node is not None and len(selected_json_node) > 0:
            return True

    return False


def update_json_content(prompt, art_styles_choices,
                               artist_name_opt,
                               photo_style_opt,
                               design_choice_opt,
                               color_choice_opt, saved_image_name):

    prompt = prompt.replace("\"", "")
    prompt = prompt.replace("\'", "")
    json_data = {
        "prompt": prompt,
        "art_styles_choices": art_styles_choices,
        "artist_name_opt": artist_name_opt,
        "photo_style_opt": photo_style_opt,
        "design_choice_opt": design_choice_opt,
        "color_choice_opt": color_choice_opt,
        "saved_image_name": saved_image_name
    }
    json_content_file = "output_images.json"
    json_content_folder = "output"
    json_file_name_path = os.path.join(os.getcwd(), json_content_folder, json_content_file)

    json_file_data = open(json_file_name_path)
    json_image_data = json.load(json_file_data)
    if "images" in json_image_data:
        # Check the file in the JSON first before appending
        if not find_image_file_node_in_json(saved_image_name):
            json_image_data['images'].append(json_data)
            json_to_save = json.dumps(json_image_data, indent=4)
            with open(json_file_name_path, "w") as outjsonfile:
                outjsonfile.write(json_to_save)


def get_selected_prompt_in_json(image_file_name):
    selected_prompt = "Missing prompt"
    json_content_file = "output_images.json"
    json_content_folder = "output"
    json_file_name_path = os.path.join(os.getcwd(), json_content_folder, json_content_file)

    json_file_data = open(json_file_name_path)
    json_image_data = json.load(json_file_data)
    if "images" in json_image_data:
        selected_json_node = [json_item for json_item in json_image_data['images']
                          if json_item['saved_image_name'] == image_file_name]
        if selected_json_node is not None and len(selected_json_node) > 0:
            selected_prompt = str(selected_json_node)

    return selected_prompt


class ProcessPrompt(object):
    def __init__(self, sd_ui_obj):
        self.name = "Text to image processor"
        self.description = "Text to image processor with prompt and image saved to disk"
        self.sd_ui_obj = sd_ui_obj
        self.generator = None
        self.text_prompt = None
        self.images_total = calculate_all_saved_images()
        self.image_files_list = ['Please select load image button to get the files list']

        # Stable Diffusion Settings
        self.num_steps = 50
        self.guidance_scale = 7.5
        self.temperature = 1
        self.batch_size = 1
        self.seed = 242424

        # Prompt specific properties
        self.artist_names = [
            'None',
            ' Katsuhiro Otomo', 'Masamune Shirow', 'pantone', 'vincent van gogh', 'ansel adams',
            'Leonardo da Vinci', 'Pablo Picasso', 'Michelangelo', 'Rembrandt', 'Claude Monet',
            'Johannes Vermeer', 'Jackson Pollock', 'Paul Cézanne', 'Dan Mumford', 'Krzysztof Maziarz',
            'magdalena pagowska'
        ]
        self.color_choice = [
            'None', 'red', 'black', 'gray', 'black & white', 'golden', 'green', 'blue'
        ]
        self.design_choice = [
            'None', 'smooth', 'sharp', 'focus', 'denoise', 'sharp focus', 'detailed'
        ]
        self.art_styles = [
            'None', 'dramatic light', 'character design', 'shoo art', 'diablo art',
            'final fantasy', 'dark fantasy', 'game character', 'Whimsical Art', 'concept art',
            'design concept', '3d style', 'renaissance style', 'futuristic art', 'disney style',
            'ancient scroll', 'animation', 'funny', 'castelvania style', 'digital art', 'Steampunk art',
            'character concept', 'Anthropomorphic art', 'trendy art'
        ]
        self.photo_style = [
            'None', 'painting', 'photo', 'cinematic', 'illustration', 'hyperealistic', 'gothic',
            'realistic', 'typography', 'overdetailed', 'unreal engine 5 render', 'octane render',
            'animation'
        ]

    def update_sd_settings(self, batch_size, temperature, num_steps, guidance_scale, seed):
        self.num_steps = num_steps
        self.guidance_scale = guidance_scale
        self.temperature = temperature
        self.batch_size = batch_size
        self.seed = seed

        sd_settings_value = {
                    "Batch Size": self.batch_size,
                    "Temperature": self.temperature,
                    "Sampling Steps": self.num_steps,
                    "Guidance Scale": self.guidance_scale,
                    "Seed": self.seed
        }
        return str(sd_settings_value)

    def load_sd_models(self, img_height, img_width):
        generator = StableDiffusion(img_height=img_height, img_width=img_width, jit_compile=False)
        model_status = "Models are not loaded"
        if generator is not None:
            model_status = "Model is loaded successfully"
        self.generator = generator
        return model_status

    def save_image_to_disk(self, img_to_save=None):
        final_image_name = None
        if img_to_save is not None:
            img_save_folder = 'output'
            img_save_dir_full_path = os.getcwd() + "/" + img_save_folder

            files_list = [f for f in os.listdir(img_save_dir_full_path)
                          if os.path.isfile(img_save_dir_full_path + "/" + f)
                          and f.endswith(".png")]
            image_id = len(files_list)
            image_id = image_id + 1
            output_file_name = "{}/art_image_{}.png".format(img_save_dir_full_path, image_id)
            Image.fromarray(img_to_save).save(output_file_name)
            self.images_total = image_id
            final_image_name = "art_image_{}.png".format(image_id)
        return final_image_name

    def update_prompt(self, prompt, art_styles_choices,
                                    artist_name_opt,
                                   photo_style_opt,
                                   design_choice_opt,
                                   color_choice_opt):
        if photo_style_opt != 'None':
            prompt = prompt + ", " + photo_style_opt
        if color_choice_opt != 'None':
            prompt = prompt + ", " + color_choice_opt
        if design_choice_opt != 'None':
            prompt = prompt + ", " + design_choice_opt
        if len(art_styles_choices) > 0 and 'None' not in art_styles_choices:
            prompt = prompt + ", " + ", ".join(art_styles_choices)
        if artist_name_opt != 'None':
            prompt = prompt + ", style by " + artist_name_opt

        self.text_prompt = prompt

    def generate_image_from_prompt(self, prompt,
                                   art_styles_choices,
                                   artist_name_opt,
                                   photo_style_opt,
                                   design_choice_opt,
                                   color_choice_opt
                                   ):
        image_generate_status = "Model is not loaded"
        img_out = None
        if self.generator is not None:
            self.update_prompt(prompt,
                               art_styles_choices,
                               artist_name_opt,
                               photo_style_opt,
                               design_choice_opt,
                               color_choice_opt)
            img = self.generator.generate(
                self.text_prompt,
                num_steps=self.num_steps,
                unconditional_guidance_scale=self.guidance_scale,
                temperature=self.temperature,
                batch_size=self.batch_size,
                seed=self.seed,
            )
            image_generate_status = "Image generation failed due to some error."
            if img is not None and len(img) > 0:
                image_generate_status = "Image is generated successfully"
                saved_image_name = self.save_image_to_disk(img[0])
                if saved_image_name is not None:
                    update_json_content(prompt,
                               art_styles_choices,
                               artist_name_opt,
                               photo_style_opt,
                               design_choice_opt,
                               color_choice_opt,
                                        saved_image_name)
                img_out = Image.fromarray(img[0])

        return image_generate_status, img_out

    def process_microphone_audio(self, audio):
        p = pipeline("automatic-speech-recognition")
        text = p(audio)["text"]
        self.text_prompt = text
        return self.text_prompt

    def load_saved_images_from_disk(self, files_list):
        if self.images_total > 0:
            img_save_folder = 'output'
            img_save_dir_full_path = os.getcwd() + "/" + img_save_folder

            self.image_files_list = [f for f in os.listdir(img_save_dir_full_path)
                          if os.path.isfile(img_save_dir_full_path + "/" + f)
                          and f.endswith(".png")]

        return gr.Dropdown.update(choices=self.image_files_list)

    def display_selected_image(self, selected_image):
        image = None
        prompt_info = "Prompt not found.."
        if selected_image is not None: #  and len(selected_image_list) > 0:
            img_save_folder = 'output'
            img_save_dir_full_path = os.getcwd() + "/" + img_save_folder
            full_image_name = os.path.join(img_save_dir_full_path, selected_image)
            if os.path.isfile(full_image_name):
                image = Image.open(full_image_name)
                prompt_info = get_selected_prompt_in_json(selected_image)
        return image, prompt_info


    def generate_ui(self):
        with self.sd_ui_obj:
            gr.Markdown("Text to Image Processing using Stable Diffusion Tensorflow Model")
            with gr.Tabs():
                with gr.TabItem("Load Stable Diffusion Model"):
                    with gr.Row():
                        with gr.Column():
                            img_input_height = gr.Slider(label="Image Height", minimum=64, maximum=1024, value=512, step=64)
                            img_input_width = gr.Slider(label="Image Width", minimum=64, maximum=1024, value=512, step=64)
                            model_loader_output = gr.Label(label="Model Status")
                            model_loader_button = gr.Button("Load Stable Diffusion Model")
                with gr.TabItem("Text to Image Prompt"):
                    with gr.Row():
                        with gr.Column():
                            audio_prompt = gr.Audio(source="microphone", type="filepath")
                            audio_prompt_btn = gr.Button(label="Record Prompt from Microphone")
                            text_prompt = gr.Textbox(label="Please input your prompt", lines=3)
                            art_styles_choices = gr.CheckboxGroup(self.art_styles,
                                                                  select='None',
                                                                  label="Art Style Choices")
                            artist_name_opt = gr.Radio(self.artist_names, value='None', label="Artist Name")
                            photo_style_opt = gr.Radio(self.photo_style, value='None', label="Photo Style Choice")
                            design_choice_opt = gr.Radio(self.design_choice, value='None', label="Design Choice")
                            color_choice_opt = gr.Radio(self.color_choice, value='None', label="Color Choice")
                            img_out = gr.Image()
                            image_generation_status = gr.Label("Image Generation Status")
                            image_generation_button = gr.Button("Generate Image")
                with gr.TabItem("Stable Diffusion Settings"):
                    with gr.Row():
                        with gr.Column():
                            sd_settings_label = gr.Label(label="Current Settings: Not updated..")
                            sd_batch_size = gr.Slider(label="Batch Size", minimum=1, maximum=10, value=1, step=1)
                            sd_temperature = gr.Slider(label="Temperature", minimum=1, maximum=10, value=5, step=1)
                            sd_step = gr.Slider(label="Sampling Step", minimum=1, maximum=100, value=50, step=5)
                            sd_scale = gr.Slider(label="Guidance Scale", minimum=1, maximum=10, value=7.5, step=0.5)
                            sd_seed = gr.Slider(label="Random Seed Value", minimum=10000, maximum=100000, value=242454, step=1000)
                            sd_settings_button = gr.Button("Save Stable Diffusion Settings")
                with gr.TabItem("Load and Display Saved Images"):
                    with gr.Row():
                        with gr.Column():
                            load_saved_image_btn = gr.Button("Load Saved Images")
                            saved_images_list = gr.Dropdown(self.image_files_list, label="Saved Images")
                            display_selected_image_btn = gr.Button("Display Selected Image")
                            saved_prompt_info = gr.Label(label="Saved Prompt")
                            saved_image_display = gr.Image(label="Saved Image")
                audio_prompt_btn.click(
                    self.process_microphone_audio,
                    [
                        audio_prompt
                    ],
                    [
                        text_prompt
                    ]
                )
                model_loader_button.click(
                    self.load_sd_models,
                    [
                        img_input_height,
                        img_input_width,
                    ],
                    [
                        model_loader_output
                    ]
                )
                image_generation_button.click(
                    self.generate_image_from_prompt,
                    [
                        text_prompt,
                        art_styles_choices,
                        artist_name_opt,
                        photo_style_opt,
                        design_choice_opt,
                        color_choice_opt
                    ],
                    [
                        image_generation_status,
                        img_out
                    ]
                )
                sd_settings_button.click(
                    self.update_sd_settings,
                    [
                        sd_batch_size,
                        sd_temperature,
                        sd_step,
                        sd_scale,
                        sd_seed
                    ],
                    [
                        sd_settings_label
                    ]
                )
                load_saved_image_btn.click(
                    self.load_saved_images_from_disk,
                    [
                        saved_images_list
                    ],
                    [
                        saved_images_list
                    ]
                )
                display_selected_image_btn.click(
                    self.display_selected_image,
                    [
                        saved_images_list
                    ],
                    [
                        saved_image_display,
                        saved_prompt_info
                    ]
                )

    def launch_ui(self):
        self.sd_ui_obj.launch()

