import whisper
import os


def whisper_decode(model, audio):
    # model = whisper.load_model("base")

    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions(
        task='translate',
        fp16=False)
    result = whisper.decode(model, mel, options)
    # print the recognized text
    print(result.text)


def whisper_transcribe(model, audio):
    result = model.transcribe(audio)
    print(result["text"])


def try_whisper_model(model_type, choice):
    model = whisper.load_model(model_type)
    data_file = os.path.join(os.path.curdir, 'data_files', 'bharat.mp3')
    audio = whisper.load_audio(data_file)
    if choice == 'decode':
        whisper_decode(model, audio)
    elif choice == 'transcribe':
        whisper_transcribe(model, audio)
