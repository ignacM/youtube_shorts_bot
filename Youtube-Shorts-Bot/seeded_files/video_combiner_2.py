# This script combines two videos into one, using a mobile 9:16 aspect ratio

import cv2
import numpy as np
import random
from moviepy.editor import VideoFileClip, clips_array

def combineVideo(video1_path, ss_path, output_path, output_path2):
    # Input video files
    input_video = VideoFileClip(video1_path)
    input_video2 = VideoFileClip(ss_path)
    duration = input_video.duration
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

if __name__ == '__main__':
    # Input video files
    input_video = VideoFileClip("./videos/1.mp4").subclip(2, 17)
    input_video2 = VideoFileClip('../screensaver/1.mp4')
    duration = input_video.duration
    duration2 = input_video2.duration
    x = random.randint(0, round(duration2-duration))

    resolution = input_video.size
    resolution = (resolution[1], resolution[0])

    input_video2 = VideoFileClip('../screensaver/1.mp4', target_resolution=resolution).subclip(x, x + duration).without_audio()

    combined_video = clips_array([[input_video],[input_video2]])

    # Output video file
    combined_video.write_videofile("./combined_videos/try.mp4")
    output_video = "./combined_videos/try.mp4"