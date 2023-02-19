import os
import whisper
import sys
import argparse
import ffmpeg
import tempfile
import warnings
from typing import Iterator, TextIO
from utils import filename, format_timestamp
from ffmpeg import Error as FFmpegError

def main():
    # Add command line arguments
    parser = argparse.ArgumentParser(description='Add subtitles to a video.')
    parser.add_argument(
        '--video',
        nargs='+', type=str,
        help='The path to video file to transcribe.',
        required=True)
    parser.add_argument(
        '--model',
        default='tiny',
        choices=whisper.available_models(), help='The name of the Whisper model to use.')
    parser.add_argument(
        '--output',
        '-o', type=str,
        default='.',
        help='The directory to save the outputs.')

    args = parser.parse_args().__dict__

    # Read model, output directory and video path from command line arguments
    model = args.pop('model')
    output_dir = args.pop('output')
    video_path = ''.join(args.pop('video'))

    print(f'Video path: {video_path}\nModel: {model}\n')

    # Get model, audio and subtitle data
    model = whisper.load_model(model)
    audio_path = get_audio(video_path)
    subtitles_path = get_subtitles(
        video_path,
        audio_path,
        output_dir,
        lambda audioPath: model.transcribe(audioPath, **args)
    )

    print(f'Overlaying subtitles to {filename(video_path)}...')

    # Prepare output path
    output_path = os.path.join(output_dir, f'{filename(video_path)}.mp4')

    # Prepare video and audio data
    video = ffmpeg.input(video_path)
    audio = video.audio

    # Overlay subtitles to video
    try:
        ffmpeg.concat(video.filter("subtitles", subtitles_path), audio, v=1, a=1).output(output_path).run()
    except FFmpegError as e:
        print(e.stderr)
        raise SystemExit

    print(f'Saved subtitled video to {os.path.abspath(output_path)}.')


'''
Creates temporary audio file extracted from video using ffmpeg.
'''
def get_audio(video_path):
    print(f'Extracting audio from {filename(video_path)}...')

    # Prepare audio path
    audio_path = os.path.join(tempfile.gettempdir(), f'{filename(video_path)}.wav')

    # Extract audio from video
    try:
        ffmpeg.input(video_path).output(
                audio_path,
                acodec='pcm_s16le', ac=1, ar='16k'
        ).run(quiet=True, overwrite_output=True)
    except FFmpegError as e:
        print(e.stderr)
        raise SystemExit

    return audio_path


'''
Creates temporary subtitle file extracted from video using Whisper.
'''
def get_subtitles(video_path, audio_path, output_dir, transcribe):
    # Prepare subtitle path
    srt_path = os.path.join('.', f'{filename(video_path)}.srt')

    print(f'Generating subtitles for {filename(video_path)}... This might take a while.')

    # Transcribe subtitles
    try:
        warnings.filterwarnings('ignore')
        result = transcribe(audio_path)
        warnings.filterwarnings('default')

        # Write results to subtitles file
        with open(srt_path, 'w', encoding='utf-8') as srt:
            for i, segment in enumerate(result["segments"], start=1):
                print(
                    f'{i}\n'
                    f'{format_timestamp(segment["start"], always_include_hours=True)} --> '
                    f'{format_timestamp(segment["end"], always_include_hours=True)}\n'
                    f'{segment["text"].strip().replace("-->", "->")}\n',
                    file=srt,
                    flush=True,
                )
    except Error as e:
        print(e.stderr)
        raise SystemExit

    return srt_path


main()