import os
from vid_editer import combineVideo, subbing2
from most_replayed_downloader import download_clip
from vid_uploader import uploader

# Set important parameters: output video location, screensaver video
screensaver = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\screensaver\1.mp4'
final_video = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\videos\vid1.mp4'
# Set pvleopard Key
leopard_key = 'nJlVKvSmD5anx+huNCZlVFkv74NxbEbqUlt8q9bQ7d+aGqJe6gtEHg=='
# Set bin location: (can be anywhere)
video1 = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\combined_videos\downloadedvid.mp4'
combined = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\combined.mp4'
combined_subtitles = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\combined_subs.mp4'
audio_path = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\audio.mp3'

subtitles_path = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\subtitles.srt'


def DownEdUp(top_video, bottom_video, combined_video, subtitles,
             output, audio, link, length):
    """
    Editing the most replayed clip of a provided YouTube video hyperlink:
        1. Given a user-input hyperlink, downloading the most replayed clip from a YouTube video.
        2. Given a location filled with screen saver videos, combine the downloaded clip
         with a randomly chosen clip from the given location.
        3. Using pvleopard API for speach to text generation, use AI to create a transcription,
         input this transcription into the combined video from step 2.

    List of parameters:

    :param top_video: absolute path to top video
    :param bottom_video: absolute path to screensaver video
    :param combined_video: absolute path to location of output video (video1 + video2, can be bin)
    :param subtitles: absolute path of where to store subtitles (can be bin)
    :param output: absolute path to location of output video with audio (video1 + video2 + subtitles + audio)
    :param audio: absolute path to location of where to store audio (can be bin)
    :param link: YouTube hyperlink of video (should have visible most replayed data)
    :param length: (0-1) how long should the video be. 1: full clip included
    :return:

    key to access pvleopard API needs to be set inside subbing2 function.

    """

    download_clip(link, top_video)

    combineVideo(top_video, bottom_video, combined_video, length)

    subbing2(combined_video, audio, subtitles, output)

    uploader()

    return


if __name__ == '__main__':
    # Raise error if location for video1 is not empty.
    if os.path.exists(video1):
        raise ValueError('%s should be empty!' % video1)

    # Requests YouTube hyperlink from user.
    input_url = str(input("Enter Youtube Video Link"))

    """
    Add input to ask user if to give timestamps, or use the ones from most replayed.
    """
    # Run the Downloader, Edit, Uploader function.
    DownEdUp(video1, screensaver, combined, subtitles_path,
             final_video, audio_path, input_url, length=1)
