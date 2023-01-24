import pvleopard
import numpy as np
import math
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip

# Access pvLeopard.
leopard = pvleopard.create(access_key='nJlVKvSmD5anx+huNCZlVFkv74NxbEbqUlt8q9bQ7d+aGqJe6gtEHg==')

# Read video files and separate the audio
videoclip = VideoFileClip('./combined_videos/result.mp4')
audioclip = videoclip.audio
audioclip.write_audiofile('./audio/result.mp3')
audioclip.close()

# Produce transcript
transcript, words = leopard.process_file('./audio/result.mp3')

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
            edited_video = VideoFileClip('./combined_videos/result2.mp4').without_audio()
            vid1 = edited_video.subclip(0, words[word][1])
            vid1.write_videofile("./combined_videos/vid1.mp4")
            original_video = VideoFileClip('./combined_videos/result.mp4').without_audio()
            vid2 = original_video.subclip(words[word][1]-1, words[word][2]+0.5)
            # Generate a text clip
            txt_clip = TextClip(txt=words[word][0], fontsize=75, color='white', bg_color='black')
            # setting position of text in the center and duration will be 5 seconds
            txt_clip = txt_clip.set_position((0.4, 0.45), relative=True).set_duration(words[word][2]-words[word][1])
            # Overlay the text clip on the first video clip
            video = CompositeVideoClip([vid2, txt_clip])
            video.write_videofile("./combined_videos/video.mp4")
            vid1 = VideoFileClip('./combined_videos/vid1.mp4')
            video = VideoFileClip('./combined_videos/video.mp4')
            finalclip = concatenate_videoclips([vid1, video], method='compose')
            vid1 = finalclip
            vid1.write_videofile("./combined_videos/result2.mp4")
        word = word + 1


"""
# Output video file
finalclip = VideoFileClip("./combined_videos/result2.mp4")
sound = AudioFileClip('./audio/result.mp3')
finalclip.audio = sound
finalclip.write_videofile("./combined_videos/result2.mp4")"""