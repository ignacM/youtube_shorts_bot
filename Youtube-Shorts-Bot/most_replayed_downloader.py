"""
Script contains several functions like obtaining most replayed data from a video, downloading a video using mrd,
or downloading video with given timestamps.
"""

import requests
import json
import os
import matplotlib.pyplot as plt
import re
import subprocess
from moviepy.editor import VideoFileClip

def getContentFromURL(url):
    """
    Adapted from https://github.com/Benjamin-Loison/YouTube-operational-API
    """
    return requests.get(url).text


def getVideoID(url):
    # videoID finds the id of the video usually between the first = and &
    videoID = re.findall('=(.*?)&', url) # Find between = and &
    videoID = videoID[0]    # Obtain the first id
    return videoID


def getTimeStamp(yt_link):
    """
    Adapted from https://github.com/Benjamin-Loison/YouTube-operational-API

    :param yt_link: give YouTube hyperlink
    :return:
    """
    # input_url = str(input("Enter Video Link")) # Ask the user to write a youtube link
    videoID = getVideoID(yt_link)

    try:
        try:
            url = f'https://yt.lemnoslife.com/videos?part=mostReplayed&id={videoID}'
            content = getContentFromURL(url)
            data = json.loads(content) # Download content of data
        except:
            url = f'http://localhost/YouTube-operational-API/noKey/videos?part=snippet&id={videoID}'
            """
            Hosting of the server needs to be ocurring, more on how to host a server can be found in:
            https://github.com/Benjamin-Loison/YouTube-operational-API/blob/main/README.md
            """
    except:
        url = f'https://yt2.lemnoslife.com/videos?part=mostReplayed&id={videoID}'


    # url = f'https://yt.lemnoslife.com/videos?part=mostReplayed&id={videoID}'   # Download youtube video data per videoID
    # url = f'http://localhost/YouTube-operational-API/noKey/videos?part=snippet&id={videoID}' # Download youtube video data per videoID

    content = getContentFromURL(url)
    data = json.loads(content)  # Download content of data

    # print(data)

    # Do a dictionary // list search to find the mostReplayed parameters
    start_timestamp = data['items'][-1]['mostReplayed']['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeStartMillis']/1000
    end_timestamp = data['items'][-1]['mostReplayed']['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeEndMillis']/1000
    video_length = data['items'][-1]['mostReplayed']['heatMarkers'][-1]['heatMarkerRenderer']['timeRangeStartMillis']/1000

    # Expanding %time of video
    start_timestamp = start_timestamp - 5
    if start_timestamp < 0:
        start_timestamp = 0
    end_timestamp = end_timestamp + 3

    print('Clip starts at %s' % start_timestamp)
    print('Clip ends at %s' % end_timestamp)

    """Y = []
    for heatMarker in data['items'][0]['mostReplayed']['heatMarkers']:
        heatMarker = heatMarker['heatMarkerRenderer']
        intensityScoreNormalized = heatMarker['heatMarkerIntensityScoreNormalized']
        Y += [intensityScoreNormalized]
    
    plt.plot(Y)
    plt.show()
    print(Y)"""

    return videoID, start_timestamp, end_timestamp


def download_clip_most_replayed(link, output_filename,
                  tmp_dir='/tmp/kinetics',
                  num_attempts=5,
                  url_base='https://www.youtube.com/watch?v='):
    """
    Adapted from still-unresolved youtube-dl issue 622: https://github.com/ytdl-org/youtube-dl/issues/622

    Download a video from YouTube if exists and is not blocked.

    :param link: given YouTube hyperlink
    :param output_filename: str
        File path where the video will be stored.
    :param num_attempts: given
    :param url_base: given
    :return:

    arguments:
    ------
    video_identifier: str
        Unique YouTube video identifier (11 characters)
    start_time: float
        Indicates the begining time in seconds from where the video
        will be trimmed.
    end_time: float
        Indicates the ending time in seconds of the trimmed video.
    """

    video_identifier, start_time, end_time = getTimeStamp(link)


    # Defensive argument checking.
    assert isinstance(video_identifier, str), 'video_identifier must be string'
    assert isinstance(output_filename, str), 'output_filename must be string'
    assert len(video_identifier) == 11, 'video_identifier %s must have length 11' %video_identifier

    print('..................')
    print('..................')
    print('..................')
    print('Downloading Clip...')
    print('..................')
    print('..................')
    print('..................')
    status = False
    # Construct command line for getting the direct video link.
    # tmp_filename = os.path.join(tmp_dir,
    #                             '%s.%%(ext)s' % uuid.uuid4())
    # command = ['youtube-dl',
    #            '--quiet', '--no-warnings',
    #            '-f', 'mp4',
    #            '-o', '"%s"' % tmp_filename,
    #            '"%s"' % (url_base + video_identifier)]
    # command = ' '.join(command)
    attempts = 0
    # while True:
    #     try:
    #         output = subprocess.check_output(command, shell=True,
    #                                          stderr=subprocess.STDOUT)
    #     except subprocess.CalledProcessError as err:
    #         attempts += 1
    #         if attempts == num_attempts:
    #             return status, err.output
    #     else:
    #         break

    # tmp_filename = glob.glob('%s*' % tmp_filename.split('.')[0])[0]
    # Construct command to trim the videos (ffmpeg required).
    # command = ['download.bat',
    #             '"%s"' % (url_base + video_identifier), str(start_time), str(end_time - start_time),
    #         #    '-threads', '1',
    #         #    '-loglevel', 'panic',
    #            '%s' % output_filename]
    command = ['powershell.exe ffmpeg',
                '-ss', str(start_time),
                '-i', '$(youtube-dl',
                '-f', 'mp4',
                '-g', '"%s")' % (url_base + video_identifier),
                '-t', str(end_time-start_time),
                '-c:v', 'libx264', '-c:a', 'copy', '%s' % output_filename]
    command = ' '.join(command)
    try:
        output = subprocess.check_output(command, shell=True,
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        return status, err.output
    # while True:
    #     try:
    #         output = subprocess.check_output(command, shell=True,
    #                                          stderr=subprocess.STDOUT)
    #     except subprocess.CalledProcessError as err:
    #         attempts += 1
    #         if attempts == num_attempts:
    #             return status, err.output
    #     else:
    #         break
    #  command = ['ffmpeg',
    #            '-i', '"%s"' % tmp_filename,
    #            '-ss', str(start_time),
    #            '-t', str(end_time - start_time),
    #            '-c:v', 'libx264', '-c:a', 'copy',
    #            '-threads', '1',
    #            '-loglevel', 'panic',
    #            '"%s"' % output_filename]
    # command = ' '.join(command)
    # try:
    #     output = subprocess.check_output(command, shell=True,
    #                                      stderr=subprocess.STDOUT)
    # except subprocess.CalledProcessError as err:
    #     return status, err.output
    # for /F "tokens=* delims=" %a in ('youtube-dl --get-url "%s"' %(url_base + video_identifier)) do (ffmpeg -ss 3 -i %a -t 15 output_filename)
    # Check if the video was successfully saved.
    status = os.path.exists(output_filename)
    # os.remove(tmp_filename)
    print('..................')
    print('..................')
    print('..................')
    print('Clip Downloaded')
    print('..................')
    print('..................')
    print('..................')
    return status, 'Downloaded'


def download_clip_timestamps(link, output_2, output_filename, start, end,
                  tmp_dir='/tmp/kinetics',
                  num_attempts=5,
                  url_base='https://www.youtube.com/watch?v='):
    """
    Adapted from still-unresolved youtube-dl issue 622: https://github.com/ytdl-org/youtube-dl/issues/622

    Download a video from YouTube if exists and is not blocked.

    :param link: given YouTube hyperlink
    :param output_2: path where the video will be stored.
    :param output_filename: str
        File path where the video will be stored.
    :param start: starting point of video (in seconds)
    :param end: ending point of video clip (in seconds)
    :param num_attempts: given
    :param url_base: given
    :return:

    arguments:
    ------
    video_identifier: str
        Unique YouTube video identifier (11 characters)
    start_time: float
        Indicates the begining time in seconds from where the video
        will be trimmed.
    end_time: float
        Indicates the ending time in seconds of the trimmed video.
    """

    video_identifier = getVideoID(link)
    start_time = start
    end_time = end

    # Defensive argument checking.
    assert isinstance(video_identifier, str), 'video_identifier must be string'
    assert isinstance(output_filename, str), 'output_filename must be string'
    assert len(video_identifier) == 11, 'video_identifier %s must have length 11' %video_identifier

    print('..................')
    print('..................')
    print('..................')
    print('Downloading Clip...')
    print('..................')
    print('..................')
    print('..................')

    status = False
    # Construct command line for getting the direct video link.
    # tmp_filename = os.path.join(tmp_dir,
    #                             '%s.%%(ext)s' % uuid.uuid4())
    # command = ['youtube-dl',
    #            '--quiet', '--no-warnings',
    #            '-f', 'mp4',
    #            '-o', '"%s"' % tmp_filename,
    #            '"%s"' % (url_base + video_identifier)]
    # command = ' '.join(command)
    attempts = 0
    # while True:
    #     try:
    #         output = subprocess.check_output(command, shell=True,
    #                                          stderr=subprocess.STDOUT)
    #     except subprocess.CalledProcessError as err:
    #         attempts += 1
    #         if attempts == num_attempts:
    #             return status, err.output
    #     else:
    #         break

    # tmp_filename = glob.glob('%s*' % tmp_filename.split('.')[0])[0]
    # Construct command to trim the videos (ffmpeg required).
    # command = ['download.bat',
    #             '"%s"' % (url_base + video_identifier), str(start_time), str(end_time - start_time),
    #         #    '-threads', '1',
    #         #    '-loglevel', 'panic',
    #            '%s' % output_filename]
    command = ['powershell.exe ffmpeg',
               '-ss', str(start_time),
               '-i', '$(youtube-dl',
               '-f', 'mp4',
               '-g', '"%s")' % (url_base + video_identifier),
               '-t', str(end_time - start_time),
               '-c:v', 'libx264', '-c:a', 'copy', '%s' % output_filename]
    command = ' '.join(command)
    try:
        output = subprocess.check_output(command, shell=True,
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        return status, err.output
    # while True:
    #     try:
    #         output = subprocess.check_output(command, shell=True,
    #                                          stderr=subprocess.STDOUT)
    #     except subprocess.CalledProcessError as err:
    #         attempts += 1
    #         if attempts == num_attempts:
    #             return status, err.output
    #     else:
    #         break
    #  command = ['ffmpeg',
    #            '-i', '"%s"' % tmp_filename,
    #            '-ss', str(start_time),
    #            '-t', str(end_time - start_time),
    #            '-c:v', 'libx264', '-c:a', 'copy',
    #            '-threads', '1',
    #            '-loglevel', 'panic',
    #            '"%s"' % output_filename]
    # command = ' '.join(command)
    # try:
    #     output = subprocess.check_output(command, shell=True,
    #                                      stderr=subprocess.STDOUT)
    # except subprocess.CalledProcessError as err:
    #     return status, err.output
    # for /F "tokens=* delims=" %a in ('youtube-dl --get-url "%s"' %(url_base + video_identifier)) do (ffmpeg -ss 3 -i %a -t 15 output_filename)
    # Check if the video was successfully saved.
    status = os.path.exists(output_filename)

    final = VideoFileClip(output_filename).subclip(1, -7)
    final.write_videofile(output_2, fps=final.fps)
    final.close

    # os.remove(tmp_filename)
    print('..................')
    print('..................')
    print('..................')
    print('Clip Downloaded')
    print('..................')
    print('..................')
    print('..................')


    return status, 'Downloaded'


if __name__ == '__main__':
    input_url = str(input("Enter Video Link"))  # Ask the user to write a YouTube link
    bin_loc = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\vid1.1.mp4'
    output = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\combined_videos\downloadedvid.mp4'
    download_clip_timestamps(input_url, bin_loc, output, 10, 15)

