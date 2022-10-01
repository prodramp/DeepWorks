import gradio as gr
from tensorflow import keras
from stable_diffusion_tf.stable_diffusion import StableDiffusion
import argparse
from PIL import Image


class ProcessPrompt(object):
    def __init__(self, sd_ui_obj):
        self.name = "Text to image processor"
        self.description = "Text to image processor with prompt and image saved to disk"
        self.sd_ui_obj = sd_ui_obj
        self.generator = None

        # Stable Diffusion Settings
        self.num_steps = 50
        self.guidance_scale = 7.5
        self.temperature = 1
        self.batch_size = 1
        self.seed = 242424

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

    def generate_image_from_prompt(self, prompt):
        image_generate_status = "Model is not loaded"
        img_out = None
        if self.generator is not None:
            img = self.generator.generate(
                prompt,
                num_steps=self.num_steps,
                unconditional_guidance_scale=self.guidance_scale,
                temperature=self.temperature,
                batch_size=self.batch_size,
                seed=self.seed,
            )
            # Image.fromarray(img[0]).save(args.output)
            image_generate_status = "Image generation failed due to some error."
            if img is not None and len(img) > 0:
                image_generate_status = "Image is generated successfully"
                img_out = Image.fromarray(img[0])

        return image_generate_status, img_out

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
                            text_prompt = gr.Textbox(label="Please input your prompt")
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
                        text_prompt
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

    def launch_ui(self):
        self.sd_ui_obj.launch()

