import os
import time
from vid_editer import combineVideo, subbing2, inputAudio, randSFX, addSFX, watermark
from most_replayed_downloader import download_clip_most_replayed, download_clip_timestamps
from vid_uploader import uploader
from vid_cropper import vidCropper

# Set important parameters: output video location, screensaver video
screensaver = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\screensaver\1.mp4'
final_video = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\videos\vid1.mp4'
bg_song = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\audio\gangster.mp3'
sfx = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\sfx'
# Set pvleopard Key
leopard_key = 'nJlVKvSmD5anx+huNCZlVFkv74NxbEbqUlt8q9bQ7d+aGqJe6gtEHg=='
# Set bin location: (can be anywhere)
bin_loc = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid1.1.mp4'
video1 = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid1.mp4'
combined = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid12.mp4'
combined_subtitles = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid1234.mp4'
audio_path = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\audio.mp3'
ar_edited = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid123.mp4'
subbed_video = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid1234.mp4'
audio_video = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid12345.mp4'
subtitles_path = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\subtitles.srt'


def DownEdUp(top_video, bin, vid_audio, ar_video, subtitles, sub_vid, bg_audio,
             output, audio, link, answer):
    """
    Editing the most replayed clip of a provided YouTube video hyperlink:
        1. Given a user-input hyperlink, downloading the most replayed clip from a YouTube video,
        or by giving timestamps
        2. Given a location filled with screen saver videos, combine the downloaded clip
         with a randomly chosen clip from the given location.
        3. Using pvleopard API for speach to text generation, use AI to create a transcription,
         input this transcription into the combined video from step 2.

    List of parameters:

    :param top_video: absolute path to top video
    :param bottom_video: absolute path to screensaver video
    :param combined_video: absolute path to location of output video (video1 + video2, can be bin)
    :param ar_video: absolute path of where to store AR adjusted video
    :param subtitles: absolute path of where to store subtitles (can be bin)
    :param output: absolute path to location of output video with audio (video1 + video2 + subtitles + audio)
    :param audio: absolute path to location of where to store audio (can be bin)
    :param link: YouTube hyperlink of video (should have visible most replayed data)
    :param answer: select 1 for most replayed data and 2 for input timestamps
    :param length: (0-1) how long should the video be. 1: full clip included
    :return:

    key to access pvleopard API needs to be set inside subbing2 function.

    """

    if answer == 1:
        download_clip_most_replayed(link, top_video)
    else:
        starting_time = str(input("What is the starting time?"))
        starting_time = sum(x * float(t) for x, t in zip([1, 60, 3600], reversed(starting_time.split(":"))))-1
        # -1 seconds because uploader lags in first downloaded frame
        ending_time = str(input("What is the ending time?"))
        ending_time = sum(x * float(t) for x, t in zip([1, 60, 3600], reversed(ending_time.split(":"))))+7
        # +3 seconds because moviepy fails to compile the last 3 seconds
        download_clip_timestamps(link, top_video, bin, starting_time, ending_time)

    time.sleep(2)

    vidCropper(top_video, ar_video)

    subbing2(ar_video, audio, subtitles, sub_vid)

    inputAudio(sub_vid, bg_audio, vid_audio)

    watermark(vid_audio, output)

    uploader()

    return



if __name__ == '__main__':
    # Raise error if location for video1 is not empty.
    if os.path.exists(video1):
        # Delete location of video 1
        os.remove(video1)
    if os.path.exists(bin_loc):
        # Delete location of video 1
        os.remove(bin_loc)

    # Requests YouTube hyperlink from user.
    input_url = str(input("Enter Youtube Video Link"))

    # Asks user the type of download
    dl_type = int(input("Enter 1 for most replayed data, or 2 for user selected timestamps"))

    #bg_song = str(input("Direction of bg_song"))
    # Run the Downloader, Edit, Uploader function.
    DownEdUp(video1, bin_loc, audio_video, ar_edited, subtitles_path, subbed_video, bg_song,
             final_video, audio_path, input_url, dl_type)



