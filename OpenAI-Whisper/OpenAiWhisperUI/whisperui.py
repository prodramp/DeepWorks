import whisper
import gradio as gr
import os
from pytube import YouTube


class WhisperModelUI(object):
    def __init__(self, ui_obj):
        self.name = "Whisper Model Processor UI"
        self.description = "This class is designed to build UI for our Whisper Model"
        self.ui_obj = ui_obj
        self.audio_files_list = ['No content']
        self.whisper_model = whisper.model.Whisper
        self.video_store_path = 'data_files'

    def load_content(self, file_list):
        video_out_path = os.path.join(os.getcwd(), self.video_store_path)

        self.audio_files_list = [f for f in os.listdir(video_out_path)
                            if os.path.isfile(video_out_path + "/" + f)
                            and (f.endswith(".mp4") or f.endswith('mp3'))]

        return gr.Dropdown.update(choices=self.audio_files_list)

    def load_whisper_model(self, model_type):
        try:
            asr_model = whisper.load_model(model_type.lower())
            self.whisper_model = asr_model
            status = "{} Model is loaded successfully".format(model_type)
        except:
            status = "error in loading {} model".format(model_type)

        return status, str(self.whisper_model)

    def load_youtube_video(self, video_url):
        video_out_path = os.path.join(os.getcwd(), self.video_store_path)
        yt = YouTube(video_url)
        local_video_path = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().download(video_out_path)
        return local_video_path

    def get_video_to_text(self,
                          transcribe_or_decode,
                          video_list_dropdown_file_name,
                          language_detect,
                          translate_or_transcribe
                          ):
        debug_text = ""
        try:
            video_out_path = os.path.join(os.getcwd(), 'data_files')
            video_full_path = os.path.join(video_out_path, video_list_dropdown_file_name)
            if not os.path.isfile(video_full_path):
                video_text = "Selected video/audio is could not be located.."
            else:
                video_text = "Bad choice or result.."
                if transcribe_or_decode == 'Transcribe':
                    video_text, debug_text = self.run_asr_with_transcribe(video_full_path, language_detect,
                                                                          translate_or_transcribe)
                elif transcribe_or_decode == 'Decode':
                    audio = whisper.load_audio(video_full_path)
                    video_text, debug_text = self.run_asr_with_decode(audio, language_detect,
                                                                      translate_or_transcribe)
        except:
            video_text = "Error processing audio..."
        return video_text, debug_text

    def run_asr_with_decode(self, audio, language_detect, translate_or_transcribe):
        debug_info = "None.."

        if 'encoder' not in dir(self.whisper_model) or 'decoder' not in dir(self.whisper_model):
            return "Model is not loaded, please load the model first", debug_info

        if self.whisper_model.encoder is None or self.whisper_model.decoder is None:
            return "Model is not loaded, please load the model first", debug_info

        try:
            # pad/trim it to fit 30 seconds
            audio = whisper.pad_or_trim(audio)

            # make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(self.whisper_model.device)

            if language_detect == 'Detect':
                # detect the spoken language
                _, probs = self.whisper_model.detect_language(mel)
                # print(f"Detected language: {max(probs, key=probs.get)}")

            # decode the audio
            # mps crash if fp16=False is not used

            task_type = 'transcribe'
            if translate_or_transcribe == 'Translate':
                task_type = 'translate'

            if language_detect != 'Detect':
                options = whisper.DecodingOptions(fp16=False,
                                                  language=language_detect,
                                                  task=task_type)
            else:
                options = whisper.DecodingOptions(fp16=False,
                                                  task=task_type)

            result = whisper.decode(self.whisper_model, mel, options)
            result_text = result.text
            debug_info = str(result)
        except:
            result_text = "Error handing audio to text.."
        return result_text, debug_info

    def run_asr_with_transcribe(self, audio_path, language_detect, translate_or_transcribe):
        result_text = "Error..."
        debug_info = "None.."

        if 'encoder' not in dir(self.whisper_model) or 'decoder' not in dir(self.whisper_model):
            return "Model is not loaded, please load the model first", debug_info

        if self.whisper_model.encoder is None or self.whisper_model.decoder is None:
            return "Model is not loaded, please load the model first", debug_info

        task_type = 'transcribe'
        if translate_or_transcribe == 'Translate':
            task_type = 'translate'

        transcribe_options = dict(beam_size=5, best_of=5,
                                  fp16=False,
                                  task=task_type,
                                  without_timestamps=False)
        if language_detect != 'Detect':
            transcribe_options['language'] = language_detect

        transcription = self.whisper_model.transcribe(audio_path, **transcribe_options)
        if transcription is not None:
            result_text = transcription['text']
            debug_info = str(transcription)
        return result_text, debug_info

    def create_whisper_ui(self):
        with self.ui_obj:
            gr.Markdown("Whisper ASR Model UI")
            with gr.Tabs():
                with gr.TabItem("YouTube to Text"):
                    with gr.Row():
                        with gr.Column():
                            asr_model_type = gr.Radio(['Tiny', 'Base', 'Small', 'Medium', 'Large'],
                                                      label="Whisper Model Type",
                                                      value='Base'
                                                      )
                            model_status_lbl = gr.Label(label="Model Load Status...")
                            load_model_btn = gr.Button("Load Whisper Model")
                            youtube_url = gr.Textbox(label="YouTube URL",
                                                     # value="https://www.youtube.com/watch?v=Y2nHd7El8iw"
                                                     value="https://www.youtube.com/watch?v=PpH_mi923_A"
                                                     )
                            youtube_video = gr.Video(label="YouTube Video")
                            get_video_btn = gr.Button("Load YouTube URL")
                        with gr.Column():
                            video_list_dropdown = gr.Dropdown(self.audio_files_list, label="Saved Videos")
                            load_video_list_btn = gr.Button("Load All Videos")
                            transcribe_or_decode = gr.Radio(['Transcribe', 'Decode'],
                                                            label="ASR Options",
                                                            value='Transcribe'
                                                            )
                            language_detect = gr.Dropdown(['Detect', 'English', 'Hindi', 'Japanese'],
                                                          label="Provide Language or detect")
                            translate_or_transcribe = gr.Dropdown(['Transcribe', 'Translate'],
                                                                  label="Set your output task - Translate or Transcribe")
                            get_video_txt_btn = gr.Button("Convert Video to Text")
                            video_text = gr.Textbox(label="Video to Text", lines=10)
                with gr.TabItem("Debug Info"):
                    with gr.Row():
                        with gr.Column():
                            debug_text = gr.Textbox(label="Debug Details", lines=20)
            load_model_btn.click(
                self.load_whisper_model,
                [
                    asr_model_type
                ],
                [
                    model_status_lbl,
                    debug_text
                ]
            )
            get_video_btn.click(
                self.load_youtube_video,
                [
                    youtube_url
                ],
                [
                    youtube_video
                ]
            )
            load_video_list_btn.click(
                self.load_content,
                [
                    video_list_dropdown
                ],
                [
                    video_list_dropdown
                ]
            )
            get_video_txt_btn.click(
                self.get_video_to_text,
                [
                    transcribe_or_decode,
                    video_list_dropdown,
                    language_detect,
                    translate_or_transcribe
                ],
                [
                    video_text,
                    debug_text
                ]
            )

    def launch_ui(self):
        self.ui_obj.launch(debug=True)
