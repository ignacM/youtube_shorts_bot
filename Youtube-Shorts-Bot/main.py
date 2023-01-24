from video_combiner_2_func import combineVideo, subbing, inputAudio

# Set important parameters, input video, output video location, screensaver, how much % of video (1 = 100%)
video1 = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\videos\1.mp4'
screensaver = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\screensaver\1.mp4'
final_video = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\combined_videos\result3.mp4'
time = 0.2

# Set pvleopard Key
leopard_key = 'nJlVKvSmD5anx+huNCZlVFkv74NxbEbqUlt8q9bQ7d+aGqJe6gtEHg=='

# Set bin location
combined = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\combined.mp4'
combined_subtitles = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\combined_subs.mp4'
audio = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\audio.mp3'
binvideo1 = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid1.mp4'
binvideo2 = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid2.mp4'



def RunModel(top_video, bottom_video, combined_video, combined_video_2, output, audio, bin_vid1, bin_vid2, key, length):
    # IMPORTANT: key: to access pvleopard API
    # top_video: absolute path to top video
    # bottom_video: absolute path to screensaver video
    # combined_video: absolute path to location of output video (video1 + video2, can be bin)
    # combined_video_2: absolute path to location of output video with subtitles (video1 + video2 + subtitles)
    # output: absolute path to location of output video with audio (video1 + video2 + subtitles + audio)
    # audio: absolute path to location of where to store audio (can be bin)
    # bin_vid1 = absolute path to location of currently edited video (can be bin)
    # bin_vid2 = absolute path to location of currently edited video (can be bin)

    combineVideo(top_video, bottom_video, combined_video, combined_video_2, length)
    subbing(key, combined_video, combined_video_2, audio, bin_vid1, bin_vid2)
    inputAudio(combined_video_2, audio, output)
    return


if __name__ == '__main__':
    RunModel(video1, screensaver, combined, combined_subtitles,
             final_video, audio, binvideo1, binvideo2, leopard_key, time)






