"""
 This script contains functions to combine two videos into one, create subtitles using pvleopard AI,
 and to write subtitles into a video.
"""

import cv2
import random
import numpy as np
import pvleopard
import math
import time
import re
from pvleopard import Sequence, Optional
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip, clips_array
from moviepy.tools import cvsecs
from moviepy.video.VideoClip import TextClip, VideoClip
from moviepy.video.tools.subtitles import SubtitlesClip


def combineVideo(video1_path, ss_path, output_path, video_length):
    """
    Video combiner that takes to videos and plays one on top of the other. The combiner randomly selects
    a clip of the second video with the same duration as the first video.
    :param video1_path: video path of the video that goes on top
    :param ss_path: video path of the video that goes below the top video.
    :param output_path: Desired path of the output
    :param video_length: Percentage [0-1] of how long should the top video be cropped to. For full video
                        duration select 1.
    :return:
    """
    print('..................')
    print('..................')
    print('..................')
    print('Combining Video...')
    print('..................')
    print('..................')
    print('..................')
    # Input video files
    percentage_of_video = video_length
    input_video = VideoFileClip(video1_path)
    input_video2 = VideoFileClip(ss_path)
    if video_length != 1:
        duration = input_video.duration * percentage_of_video
        input_video = VideoFileClip(video1_path).subclip(0, duration)
        duration2 = input_video2.duration
        x = random.randint(0, round(duration2 - duration))
    else:
        duration = input_video.duration
        duration2 = input_video2.duration
        x = random.randint(0, round(duration2 - duration))

    resolution = input_video.size
    resolution = (resolution[1], resolution[0])

    input_video2 = VideoFileClip(ss_path, target_resolution=resolution).subclip(x, x+duration).without_audio()

    combined_video = clips_array([[input_video], [input_video2]])

    # Output video file
    combined_video.write_videofile(output_path)
    # combined_video.write_videofile(output_path2)

    print('................')
    print('................')
    print('................')
    print('Video Combined')
    print('................')
    print('................')
    print('................')
    return


def subbing(pvl_key, video_path, video_path2, audio_path, bin_path, bin_path2):
    """
    Seeded function since moviepy has an accessible working unreleased developing-stage function that can
    create subtitles more efficiently. This function works but is more computationally expensive.
    Need to use the function inputAudio afterwards to play the sound.

    :param pvl_key: Insert the key provided by pvleopard API
    :param video_path: input path: video without subtitles
    :param video_path2: output path: video with subtitles
    :param audio_path:
    :param bin_path: bin path needed to locally store the video (can be any path)
    :param bin_path2: bin path needed to locally store the video (can be any path)
    :return:
    """
    # Access pvLeopard.
    leopard = pvleopard.create(access_key=pvl_key)
    # Read video files and separate the audio
    videoclip = VideoFileClip(video_path)
    audioclip = videoclip.audio
    audioclip.write_audiofile(audio_path)
    audioclip.close()

    # Produce transcript using pvleopard API:
    transcript, words = leopard.process_file(audio_path)

    wordcount = len(words)-1
    #secondcount = math.ceil(words[wordcount]["end_sec"])
    secondcount = 1
    seconds = np.arange(0, secondcount, 0.5) # Storing a numbers 0, 0.5, 1 to iterate over every word
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
                vid2 = original_video.subclip(words[word][1]-0.3, words[word][2]+0.3)
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

    print('................')
    print('................')
    print('................')
    print('Video Subbed')
    print('................')
    print('................')
    print('................')
    return


def inputAudio(video_path, audio_path, output):
    """
    inputAudio takes a recorded audio and plays it onto a video
    :param video_path: soundless video path
    :param audio_path: audio path
    :param output: location of ouput video with sound
    :return:
    """
    # Output video file
    finalclip = VideoFileClip(video_path)
    sound = AudioFileClip(audio_path)
    finalclip = finalclip.set_audio(sound)
    finalclip.write_videofile(output)
    return


def subbing2(video_path, audio_path, subtitles_path, final_path):
    """
    This function uses the Experimental module for subtitles from moviepy. It uses pvleopard to
    create an AI generated transcript of the video.

    Adapted from experimental module availabe at:
    https://zulko.github.io/moviepy/_modules/moviepy/video/tools/subtitles.html#SubtitlesClip

    :param video_path: path of the video
    :param audio_path: path of where to store the audio of the video (needed for pvleopard transcript generation)
    :param subtitles_path: path of where to store the subtitles
    :param final_path: desired output path of the video
    :return:

    Other parameters needed are pvLeopard key, which can be input below

    """

    # Read video files and separate the audio
    videoclip = VideoFileClip(video_path)
    audioclip = videoclip.audio
    audioclip.write_audiofile(audio_path)

    # Access pvLeopard API.
    key = 'nJlVKvSmD5anx+huNCZlVFkv74NxbEbqUlt8q9bQ7d+aGqJe6gtEHg=='
    leopard = pvleopard.create(access_key=key)
    # Produce transcript with pvleopard.
    transcript, words = leopard.process_file(audio_path)

    # Write generated subtitles into a srt file.
    with open(subtitles_path, 'w') as f:
        f.write(to_srt(words))

    # Read the subtitles with desired font, size, color etc.
    generator = lambda txt: TextClip(txt, font='Georgia-Regular', fontsize=65, color='white', bg_color='black')
    sub = SubtitlesClip(subtitles_path, generator)

    # Write the final video with the subtitles.
    final = CompositeVideoClip([videoclip, sub.set_position("center")])
    final.write_videofile(final_path, fps=videoclip.fps)


def second_to_timecode(x: float) -> str:
    """
    Adapted from:
    https://picovoice.ai/blog/how-to-create-subtitles-for-any-video-with-python/#:~:text=How%20to%20Create%20Subtitles%20for%20any%20Video%20with,No%20speech%20recognition%20technology%20is%20100%25%20accurate.%20
    """

    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)
    return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)


def to_srt(
        words: Sequence[pvleopard.Leopard.Word],
        endpoint_sec: float = 1.,
        length_limit: Optional[int] = 4) -> str:
    """
    Set: length_limit: Optional[int] =
    as the number of maximum words per subtitle eg if 4  then:

    Hello my name is
    Ignacio and what is
    your name?

    Adapted from:
    https://picovoice.ai/blog/how-to-create-subtitles-for-any-video-with-python/#:~:text=How%20to%20Create%20Subtitles%20for%20any%20Video%20with,No%20speech%20recognition%20technology%20is%20100%25%20accurate.%20

    """

    def _helper(end: int) -> None:
        lines.append("%d" % section)
        lines.append(
            "%s --> %s" %
            (
                second_to_timecode(words[start].start_sec),
                second_to_timecode(words[end].end_sec)
            )
        )
        lines.append(' '.join(x.word for x in words[start:(end + 1)]))
        lines.append('')

    lines = list()
    section = 0
    start = 0
    for k in range(1, len(words)):
        if ((words[k].start_sec - words[k - 1].end_sec) >= endpoint_sec) or \
                (length_limit is not None and (k - start) >= length_limit):
            _helper(k - 1)
            start = k
            section += 1
    _helper(len(words) - 1)
    return '\n'.join(lines)


#if __name__ == '__main__':