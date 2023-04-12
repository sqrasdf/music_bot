# download song from youtube

from pytube import YouTube

from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup
import numpy as np
import math

import random
import os
from moviepy.editor import *


def make_video(link):

    # url input from user
    link = link.strip()
    yt = YouTube(link)

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    my_filename = yt.title + " (speed up).mp4"
    
    # download the file
    out_file = video.download(filename="temp.mp3")

    # result of success
    print(yt.title + " has been successfully downloaded.")


    # bass boost and speed up


    AudioSegment.converter = "D:\\programs\\ffmpeg\\bin\\ffmpeg.exe"
    attenuate_db = 0
    accentuate_db = 8

    def bass_line_freq(track):
        sample_track = list(track)
        # c-value
        est_mean = np.mean(sample_track)
        # a-value
        est_std = 3 * np.std(sample_track) / (math.sqrt(2))
        bass_factor = int(round((est_std - est_mean) * 0.005))
        return bass_factor

    file = "temp.mp3"
    # sound = AudioSegment.from_mp3(file)
    try:
        sound = AudioSegment.from_file(file, "mp3")
    except:
        sound = AudioSegment.from_file(file, format="mp4")

    faster = speedup(sound, playback_speed=1.25)
    print("speeding up done")
    # print(bass_line_freq(faster.get_array_of_samples()))
    filtered = faster.low_pass_filter(bass_line_freq(faster.get_array_of_samples()))
    speed_bass = (faster - attenuate_db).overlay(filtered + accentuate_db)
    speed_bass.export("temp.mp3", "mp3")
    print("bass boosting done")


    # creting video with gif and audio


    gif_path = "./gifs/" + random.choice(os.listdir("./gifs"))
    gif = VideoFileClip(gif_path)
    audio = AudioFileClip("temp.mp3")

    # Set the duration of the video based on the audio duration
    duration = audio.duration

    # Create a black clip with the same size as the GIF and audio
    black_clip = ColorClip(size=gif.size, color=(0, 0, 0), duration=duration)

    # Set the audio for the black clip
    black_clip = black_clip.set_audio(audio)

    # Overlay the GIF on the black clip, centered
    gif = gif.resize(height=480)  # Resize the GIF to desired height
    gif = gif.set_position(("center", "center"))  # Set the position of the GIF to the center
    gif = gif.fx(vfx.loop, duration=duration)
    video = CompositeVideoClip([black_clip, gif.set_start(0)], size=(1920, 1080))

    # video = video.set_duration(10)

    # Write the video to a file
    video.write_videofile(f"./results/{my_filename}", codec='libx264', fps=24)
    print("video is done :D\n\n")