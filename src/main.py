import whisper
import sys
import argparse
import ffmpeg

global model, output_path, video

def main():
    parse_parameters()
    get_subtitles()

def parse_parameters():
    global model, output_path, video
    parser = argparse.ArgumentParser(description='Add subtitles to a video.')
    parser.add_argument(
        '--video',
        nargs='+', type=str,
        help='The path to video file to transcribe.',
        required=True)
    parser.add_argument(
        '--model',
        default='small',
        choices=whisper.available_models(), help='The name of the Whisper model to use.')
    parser.add_argument(
        '--output_dir',
        '-o', type=str,
        default='.',
        help='The directory to save the outputs.')

    args = parser.parse_args().__dict__

    model = args.pop('model')
def get_audio(video_path):
    print(f'Extracting audio from {filename(video_path)}...')
    audio_path = os.path.join(tempfile.gettempdir(), f'{filename(video_path)}.wav')

    try:
        ffmpeg.input(video_path).output(
                audio_path,
                acodec='pcm_s16le', ac=1, ar='16k'
        ).run(quiet=True, overwrite_output=True)
    except FFmpegError as e:
        print(e.stderr)
        raise SystemExit

    return audio_path



def get_audio(arg):
    input = ffmpeg.input(arg)
    return input.audio

def get_subtitles(audo, srt_only, output_path, transcribeFunction):
    

def get_data():
    global model, output_path, video
    model = whisper.load_model(model)
    audios = get_audio(video)
    subtitles = get_subtitles(
        audios, False, output_path, lambda audioPath: model.transcribe(audioPath, **args))

main()