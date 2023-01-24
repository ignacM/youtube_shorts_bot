# This script combines two videos into one, using a mobile 9:16 aspect ratio

import cv2
import random
from moviepy.editor import VideoFileClip, clips_array
import pvleopard
import numpy as np
import math
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip


def combineVideo(video1_path, ss_path, output_path, output_path2, video_length):
    # Input video files
    percentage_of_video = video_length
    input_video = VideoFileClip(video1_path)
    input_video2 = VideoFileClip(ss_path)
    duration = input_video.duration*percentage_of_video
    input_video = VideoFileClip(video1_path).subclip(0, duration)
    duration2 = input_video2.duration
    x = random.randint(0, round(duration2-duration))

    resolution = input_video.size
    resolution = (resolution[1], resolution[0])

    input_video2 = VideoFileClip(ss_path, target_resolution=resolution).subclip(x, x+duration).without_audio()

    combined_video = clips_array([[input_video], [input_video2]])

    # Output video file
    combined_video.write_videofile(output_path)
    combined_video.write_videofile(output_path2)
    return


def subbing(pvl_key, video_path, video_path2, audio_path, bin_path, bin_path2):
    # Access pvLeopard.
    leopard = pvleopard.create(access_key=pvl_key)
    # Read video files and separate the audio
    videoclip = VideoFileClip(video_path)
    audioclip = videoclip.audio
    audioclip.write_audiofile(audio_path)
    audioclip.close()

    # Produce transcript
    transcript, words = leopard.process_file(audio_path)

    wordcount = len(words)-1
    #secondcount = math.ceil(words[wordcount]["end_sec"])
    secondcount = 1
    seconds = np.arange(0, secondcount, 0.5)
    word = 0

    while word < wordcount:
        for s in seconds:
            s = word + s
            if s > words[word][1]:
                # ADD if statement to let know which vid to take in first iteration
                # ADD statement to hold text, so that next video takes both texts
                # Smoothen video created
                edited_video = VideoFileClip(video_path2).without_audio()
                vid1 = edited_video.subclip(0, words[word][1])
                vid1.write_videofile(bin_path)
                vid1.close()
                original_video = VideoFileClip(video_path).without_audio()
                vid2 = original_video.subclip(words[word][1]-0.5, words[word][2]+0.5)
                # ADD statement if word less than 0.75, then omit 0.75
                # Generate a text clip
                txt_clip = TextClip(txt=words[word][0], fontsize=75, color='white', bg_color='black')
                # setting position of text in the center and duration will be 5 seconds
                txt_clip = txt_clip.set_position((0.4, 0.45), relative=True).set_duration(words[word][2]-words[word][1])
                # Overlay the text clip on the first video clip
                video = CompositeVideoClip([vid2, txt_clip])
                vid2.close()
                video.write_videofile(bin_path2)
                video.close()
                vid1 = VideoFileClip(bin_path)
                video = VideoFileClip(bin_path2)
                finalclip = concatenate_videoclips([vid1, video], method='compose')
                vid1 = finalclip
                vid1.write_videofile(video_path2)
            word = word + 1

    return


def inputAudio(video_path, audio_path, output):
    # Output video file
    finalclip = VideoFileClip(video_path)
    sound = AudioFileClip(audio_path)
    finalclip = finalclip.set_audio(sound)
    finalclip.write_videofile(output)
    return
