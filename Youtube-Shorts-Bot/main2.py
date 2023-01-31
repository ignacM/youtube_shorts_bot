from video_combiner_2_func import combineVideo, subbing2
from download_most_replayed_clip import download_clip

# Set important parameters: output video location, screensaver video
screensaver = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\screensaver\1.mp4'
final_video = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\combined_videos\result3.mp4'
# Set pvleopard Key
leopard_key = 'nJlVKvSmD5anx+huNCZlVFkv74NxbEbqUlt8q9bQ7d+aGqJe6gtEHg=='
# Set bin location: (can be anywhere)
video1 = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\combined_videos\downloadedvid.mp4'
combined = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\combined.mp4'
combined_subtitles = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\combined_subs.mp4'
audio = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\audio.mp3'
binvideo1 = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid1.mp4'
binvideo2 = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid2.mp4'
subtitles = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\subtitles.srt'

def RunModel(top_video, bottom_video, combined_video, combined_video_2,
             output, audio, bin_vid1, bin_vid2, key, length, link):
    # IMPORTANT: key: to access pvleopard API
    # top_video: absolute path to top video
    # bottom_video: absolute path to screensaver video
    # combined_video: absolute path to location of output video (video1 + video2, can be bin)
    # combined_video_2: absolute path to location of output video with subtitles (video1 + video2 + subtitles)
    # output: absolute path to location of output video with audio (video1 + video2 + subtitles + audio)
    # audio: absolute path to location of where to store audio (can be bin)
    # bin_vid1 = absolute path to location of currently edited video (can be bin)
    # bin_vid2 = absolute path to location of currently edited video (can be bin)

    download_clip(link, top_video)

    combineVideo(top_video, bottom_video, combined_video, combined_video_2, length)

    subbing2(combined_video, audio, subtitles, output)

    return


if __name__ == '__main__':

    input_url = str(input("Enter Youtube Video Link"))  # Ask the user to write a youtube link
    time = int(input("percentage of video"))  # how much % of video (1 = 100%) to download
    # Add input to ask user if to give timestamps, or use the ones from most replayed.
    RunModel(video1, screensaver, combined, combined_subtitles,
             final_video, audio, binvideo1, binvideo2, leopard_key, time, input_url)

