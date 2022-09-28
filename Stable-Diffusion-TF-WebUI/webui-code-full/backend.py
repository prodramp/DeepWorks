from tensorflow import keras
from stable_diffusion_tf.stable_diffusion import Text2Image
from PIL import Image, ImageDraw, ImageFont
import gradio as gr
import os
import json
from transformers import pipeline

# generator = None


def save_images(img=None):
    dir_name = os.getcwd() + "/output"
    files = [f for f in os.listdir(dir_name) if os.path.isfile(dir_name + '/' + f) and f.endswith('.png')]
    file_id = len(files)
    file_id = file_id + 1
    output_file_name = '{}/art_image_{}.png'.format(dir_name, str(file_id))
    if img is not None:
        Image.fromarray(img[0]).save(output_file_name)
        return "art_image_{}.png".format(str(file_id))
    return "art_image_{}.png".format(str(file_id))


def update_prompt(prompt, artist_name_opt, photo_style_opt, art_styles_choices,
                  color_choice_opt,
                  design_choice_opt,
                  output_choice_opt
                  ):
    if photo_style_opt != 'None':
        prompt = prompt + ", " + photo_style_opt
    if len(art_styles_choices) > 0:
        if len(art_styles_choices) == 1 and art_styles_choices[0] != 'None':
            prompt = prompt + " , ".join(art_styles_choices)
    if color_choice_opt != 'None':
        prompt = prompt + ", " + color_choice_opt
    if design_choice_opt != 'None':
        prompt = prompt + ", " + design_choice_opt
    if output_choice_opt != 'None':
        prompt = prompt + ", " + output_choice_opt
    if artist_name_opt != 'None':
        prompt = prompt + ", style by " + artist_name_opt

    return prompt


def generate_error_image(message, color):
    width = 512
    height = 512
    if message is None or len(message.strip()) == 0:
        message = "There is no message"
    # font = ImageFont.truetype("arial.ttf", size=20)
    img = Image.new('RGB', (width, height), color=color)
    imgDraw = ImageDraw.Draw(img)
    textWidth, textHeight = imgDraw.textsize(message)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2
    imgDraw.text((xText, yText), message, fill=(255, 255, 0))
    return img


def find_file_info_in_json(json_data, file_name):
    img_json = [json_item for json_item in json_data if json_item['image_file_name'] == file_name]
    if img_json is not None and len(img_json) > 0:
        return True
    return False


def get_file_info_in_json(image_file_name):
    json_file_path = os.getcwd() + "/output/output_images.json"
    json_file_data = open(json_file_path)
    image_data = json.load(json_file_data)

    if 'all_images' in image_data:
        img_json = [json_item for json_item in image_data['all_images'] if json_item['image_file_name'] == image_file_name]
        if img_json is not None and len(img_json) > 0:
            return str(img_json)
    return "Missing prompt.."


def update_json(prompt, artist_name_opt, photo_style_opt,
                art_styles_choices, color_choice_opt, design_choice_opt, output_choice_opt,
                image_file_name):
    prompt = prompt.replace("\"", "")
    prompt = prompt.replace("\'", "")
    json_data = {
        "prompt": prompt,
        "photo_style": photo_style_opt,
        "artist_name": artist_name_opt,
        "art_styles": art_styles_choices,
        "color_choice": color_choice_opt,
        "design_choice": design_choice_opt,
        "output_choice": output_choice_opt,
        "image_file_name": image_file_name
    }
    json_file_path = os.getcwd() + "/output/output_images.json"
    json_file_data = open(json_file_path)
    image_data = json.load(json_file_data)

    if 'all_images' in image_data:
        # Serializing json
        if not find_file_info_in_json(image_data['all_images'], image_file_name):
            image_data['all_images'].append(json_data)
            json_object = json.dumps(image_data, indent=4)
            with open(json_file_path, "w") as outfile:
                outfile.write(json_object)


class ProcessPrompt(object):
    def __init__(self, ui_obj):
        self.name = "Text to Image Processor"
        self.ui_obj = ui_obj
        self.generator = None

        self.batch_size = 1
        self.temperature_value = 1
        self.scale_value = 7.5
        self.steps_value = 10
        self.seed_value = 45245

        self.current_image = None
        self.current_prompt = None
        self.files_list_options = ['Please load the images using the Load Image button']
        self.artist_names = [
            'None',
            ' Katsuhiro Otomo', 'Masamune Shirow', 'pantone', 'vincent van gogh', 'ansel adams',
            'Leonardo da Vinci', 'Pablo Picasso', 'Michelangelo', 'Rembrandt', 'Claude Monet',
            'Johannes Vermeer', 'Jackson Pollock', 'Paul Cézanne', 'Dan Mumford', 'Krzysztof Maziarz',
            'magdalena pagowska',
        ]
        self.color_choice = [
            'None', 'red', 'black', 'gray', 'black & white', 'golden', 'green', 'blue'
        ]
        self.design_choice = [
            'None', 'smooth', 'sharp', 'focus', 'denoise', 'sharp focus', 'detailed'
        ]
        self.output_choice = [
                'None', '2k', '4k', '8k'
        ]
        self.art_styles = [
            'None', 'dramatic light', 'character design', 'shoo art', 'diablo art',
            'final fantasy', 'dark fantasy', 'game character', 'Whimsical Art', 'concept art',
            'design concept', '3d style', 'renaissance style', 'futuristic art', 'disney style',
            'ancient scroll', 'animation', 'funny', 'castelvania style', 'digital art', 'Steampunk art',
            'character concept', 'Anthropomorphic art', 'trendy art'
        ]
        self.photo_style = [
            'None', 'painting', 'photo',  'cinematic', 'illustration', 'hyperealistic', 'gothic',
            'realistic', 'typography', 'overdetailed', 'unreal engine 5 render', 'octane render',
            'animation'
        ]

    def load_all_images(self, file_in_choices):
        dir_name = os.getcwd() + "/output"
        files = [f for f in os.listdir(dir_name) if os.path.isfile(dir_name + "/" + f) and f.endswith('.png')]
        self.files_list_options = files
        return gr.Dropdown.update(choices=self.files_list_options), "{} files are loaded in the list".format(len(files))

    def show_saved_image(self, img_name):
        img = None
        image_info = "Prompt missing..."
        if img_name is not None and len(img_name) > 0:
            image_info = get_file_info_in_json(img_name)
            full_image_name = os.getcwd() + "/output/" + img_name
            if os.path.isfile(full_image_name):
                img = Image.open(full_image_name)
                self.current_image = full_image_name
        return img, image_info

    def generate_image(self, prompt,
                       art_styles_choices, photo_style_opt, artist_name_opt,
                       color_choice_opt,
                       design_choice_opt,
                       output_choice_opt
                       ):
        # keras.mixed_precision.set_global_policy("mixed_float16")
        prompt = update_prompt(prompt,
                               artist_name_opt,
                               photo_style_opt,
                               art_styles_choices,
                               color_choice_opt,
                               design_choice_opt,
                               output_choice_opt
                               )
        if self.generator is None:
            return "Please load the model first from the first tab", \
                   generate_error_image('Model is not found..', 'red')

        if prompt is None or len(prompt) == 0 or len(prompt) > 150:
            return "Please keep your model under 25 words and about 60 characters.", \
                   generate_error_image('Your prompt is very long', 'red')

        img = self.generator.generate(
            prompt,
            num_steps=self.steps_value,
            unconditional_guidance_scale=self.scale_value,
            temperature=self.temperature_value,
            batch_size=self.batch_size,
            seed=self.seed_value,
        )
        image_file_name = save_images(img)
        if image_file_name is not None:
            update_json(prompt, artist_name_opt,
                                   photo_style_opt,
                                   art_styles_choices,
                                   color_choice_opt,
                                   design_choice_opt,
                                   output_choice_opt,
                        image_file_name)
        self.current_image = img[0]
        return prompt, Image.fromarray(img[0])

    def show_current_image(self):
        if self.current_image is None:
            return generate_error_image('There is no image generate recently', 'red')
        return self.current_image

    def load_all_models(self, img_size):
        img_height = img_size
        img_width = img_size
        model_status = "Model is not loaded.."
        full_model_path = os.getcwd() + "/models"
        try:
            global generator
            self.generator = Text2Image(img_height=img_height,
                                   img_width=img_width,
                                   model_path=full_model_path,
                                   jit_compile=False)
            # self.generator = generator
            model_status = "Models are loaded.."
        except:
            print("Error")
        return model_status

    def update_settings(self, batch_size_step, temperature_step, scale, steps, seed):
        self.batch_size = batch_size_step
        self.temperature_value = temperature_step
        self.scale_value = scale
        self.steps_value = steps
        self.seed_value = seed

        settings_json = {'batch_size': self.batch_size,
                         'temperature_value': self.temperature_value,
                         'scale_value': self.scale_value,
                         'steps_value': self.steps_value,
                         'seed_value': self.seed_value
                         }
        return str(settings_json)

    def transcribe_audio(self, audio):
        p = pipeline("automatic-speech-recognition")
        text = p(audio)["text"]
        self.current_prompt = text
        return text

    def create_application_ui(self):
        with self.ui_obj:
            gr.Markdown("Text to Image with Stable Diffusion")
            with gr.Tabs():
                with gr.TabItem("Load your Models"):
                    with gr.Row():
                        with gr.Column():
                            model_label = gr.Label(label="Please make sure models are loaded..")
                            slider_size = gr.Slider(64, 1024,
                                                     label="Set your Target Image Size Square(H x W)",
                                                     value=512, step=64)
                            model_loader_btn = gr.Button("Load Models")
                        with gr.Column():
                            model_status = gr.Label(label="Model Info")
                with gr.TabItem("Generate Image > Text Prompt"):
                    with gr.Row():
                        with gr.Column():
                            audio_prompt = gr.Audio(source="microphone", type="filepath")
                            audio_prompt_button = gr.Button("Create Prompt from Audio Input")
                            # img_source = gr.Image(label="Please select source Image")
                            text_input = gr.Textbox(lines=3, placeholder="Prompt Here...")
                            art_styles_choices = gr.CheckboxGroup(self.art_styles,
                                                                 select='None',
                                                                 label="Artist Choices")
                            photo_style_opt = gr.Radio(self.photo_style, value='None',
                                                                 label="Photo Style Choices")
                            artist_name_opt = gr.Radio(self.artist_names, value='None', label="Art Style Choices")
                            color_choice_opt = gr.Radio(self.color_choice, value='None', label="Color Choices")
                            design_choice_opt = gr.Radio(self.design_choice, value='None', label="Design Choices")
                            output_choice_opt = gr.Radio(self.output_choice, value='None', label="Output Image Choices")
                            source_image_loader = gr.Button("Load above Image")
                        with gr.Column():
                            output_label = gr.Label(label="Image Info")
                            img_output = gr.Image(label="Image Output")
                with gr.TabItem("Load Images/Display Images"):
                    with gr.Row():
                        with gr.Column():
                            img_prompt = gr.Label(label="Images")
                            image_loader_btn = gr.Button("Load Saved Images ....")
                            files_list = gr.Dropdown(self.files_list_options,
                                                     label="Output Images..")
                            image_display_btn = gr.Button("Display Selected Images")
                            current_image_btn = gr.Button("Show current Image")
                        with gr.Column():
                            images_status = gr.Label(label="Model Info")
                            save_img_output = gr.Image(label="Image Output")
                with gr.TabItem("Image Generation Settings"):
                    with gr.Row():
                        with gr.Column():
                            settings_info = gr.Label(label="Current Settings Info")
                            batch_size_step = gr.Slider(1, 16,
                                                     label="Batch Size",
                                                     value=1, step=1)
                            temperature_step = gr.Slider(1, 10,
                                                     label="Temperature Value",
                                                     value=5, step=1)
                            slider_scale = gr.Slider(1, 10,
                                                     label="Unconditional guidance scale: eps = eps(x, empty) + scale * (eps(x, cond) - eps(x, empty))",
                                                     value=7.5, step=0.5)
                            slider_step = gr.Slider(1, 100,
                                                     label="Number of ddim sampling steps",
                                                     value=50, step=5)
                            slider_seed = gr.Slider(1000, 100000,
                                                     label="(Optional) Specify a seed integer for reproducible results",
                                                     value=50000, step=1000)
                            image_settings_btn = gr.Button("Update Settings")
            audio_prompt_button.click(
                self.transcribe_audio,
                [
                    audio_prompt
                ],
                [
                    text_input
                ]
            )

            model_loader_btn.click(
                self.load_all_models,
                [
                    slider_size,
                ],
                [
                    model_status
                ]
            )
            source_image_loader.click(
                self.generate_image,
                [
                    text_input,
                    art_styles_choices,
                    photo_style_opt,
                    artist_name_opt,
                    color_choice_opt,
                    design_choice_opt,
                    output_choice_opt
                ],
                [
                    output_label,
                    img_output
                ]
            )
            image_loader_btn.click(
                self.load_all_images,
                [
                    files_list,
                ],
                [
                    files_list,
                    images_status
                ]
            )
            image_display_btn.click(
                self.show_saved_image,
                [
                    files_list
                ],
                [
                    save_img_output,
                    img_prompt
                ]
            )
            current_image_btn.click(
                self.show_current_image,
                [

                ],
                [
                    save_img_output
                ]
            )
            image_settings_btn.click(
                self.update_settings,
                [
                    batch_size_step,
                    temperature_step,
                    slider_scale,
                    slider_step,
                    slider_seed,
                ],
                [
                    settings_info
                ]
            )

    def launch_ui(self):
        self.ui_obj.launch()
