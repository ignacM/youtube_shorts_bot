# This script combines two videos into one, using a mobile 9:16 aspect ratio

import cv2
import random
from moviepy.editor import VideoFileClip, clips_array
from moviepy.video.tools import subtitles
import pvleopard
from pvleopard import Sequence, Optional
import numpy as np
import math
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.tools import subtitles
import re
import numpy as np
from moviepy.tools import cvsecs
from moviepy.video.VideoClip import TextClip, VideoClip
from moviepy.video.tools.subtitles import SubtitlesClip



def combineVideo(video1_path, ss_path, output_path, output_path2, video_length):
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

    print('................')
    print('................')
    print('................')
    print('Video Combined')
    print('................')
    print('................')
    print('................')
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
    # Output video file
    finalclip = VideoFileClip(video_path)
    sound = AudioFileClip(audio_path)
    finalclip = finalclip.set_audio(sound)
    finalclip.write_videofile(output)
    return


def subbing2(video_path, audio_path, subtitles_path, final_path):
    # Access pvLeopard.
    key = 'nJlVKvSmD5anx+huNCZlVFkv74NxbEbqUlt8q9bQ7d+aGqJe6gtEHg=='
    leopard = pvleopard.create(access_key=key)
    # Read video files and separate the audio
    videoclip = VideoFileClip(video_path)
    audioclip = videoclip.audio
    audioclip.write_audiofile(audio_path)


    # Produce transcript
    transcript, words = leopard.process_file(audio_path)

    with open(subtitles_path, 'w') as f:
        f.write(to_srt(words))

    generator = lambda txt: TextClip(txt, font='Georgia-Regular', fontsize=75, color='white', bg_color='black')
    sub = SubtitlesClip(subtitles_path, generator)

    final = CompositeVideoClip([videoclip, sub.set_position("center")])
    final.write_videofile(final_path, fps=videoclip.fps)


def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)
    return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)

def to_srt(
        words: Sequence[pvleopard.Leopard.Word],
        endpoint_sec: float = 1.,
        length_limit: Optional[int] = 6) -> str:
    """
    Set: length_limit: Optional[int] =
    as the number of maximum words per subtitle eg if 4  then:

    Hello my name is
    Ignacio and what is
    your name?

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