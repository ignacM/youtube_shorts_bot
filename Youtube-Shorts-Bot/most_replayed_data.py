import requests, json
import os
import matplotlib.pyplot as plt
import re
import subprocess

# Adapted from https://github.com/Benjamin-Loison/YouTube-operational-API

def getContentFromURL(url):
    return requests.get(url).text

def getTimeStamp(yt_link):
    # input_url = str(input("Enter Video Link")) # Ask the user to write a youtube link
    # videoID finds the id of the video usually between the first = and &
    videoID = re.findall('=(.*?)&', yt_link) # Find between = and &

    videoID = videoID[0]    # Obtain the first id
    # try:
    #     url = f'https://yt2.lemnoslife.com/videos?part=mostReplayed&id={videoID}'
    #     content = getContentFromURL(url)
    #     data = json.loads(content) # Download content of data
    # except AttributeError (or whatever the error name is):
    #     url = f'http://localhost/YouTube-operational-API/noKey/videos?part=snippet&id={videoID}'
    # except:
    #     url = f'https://yt.lemnoslife.com/videos?part=mostReplayed&id={videoID}'

    url = f'https://yt.lemnoslife.com/videos?part=mostReplayed&id={videoID}'   # Download youtube video data per videoID
    #url = f'http://localhost/YouTube-operational-API/noKey/videos?part=snippet&id={videoID}' # Download youtube video data per videoID

    content = getContentFromURL(url)
    data = json.loads(content)  # Download content of data

    print(data)

    # Do a dictionary // list search to find the mostReplayed parameters
    start_timestamp = data['items'][-1]['mostReplayed']['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeStartMillis']/1000
    end_timestamp = data['items'][-1]['mostReplayed']['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeEndMillis']/1000
    video_length = data['items'][-1]['mostReplayed']['heatMarkers'][-1]['heatMarkerRenderer']['timeRangeStartMillis']/1000


    # Expanding %time of video
    start_timestamp = start_timestamp - 5
    end_timestamp = end_timestamp + 3

    print(start_timestamp)
    print(end_timestamp)

    """Y = []
    for heatMarker in data['items'][0]['mostReplayed']['heatMarkers']:
        heatMarker = heatMarker['heatMarkerRenderer']
        intensityScoreNormalized = heatMarker['heatMarkerIntensityScoreNormalized']
        Y += [intensityScoreNormalized]
    
    plt.plot(Y)
    plt.show()
    print(Y)"""

    return videoID, start_timestamp, end_timestamp


def download_clip(link, output_filename,
                  tmp_dir='/tmp/kinetics',
                  num_attempts=5,
                  url_base='https://www.youtube.com/watch?v='):
    """Download a video from youtube if exists and is not blocked.
    arguments:
    ---------
    video_identifier: str
        Unique YouTube video identifier (11 characters)
    output_filename: str
        File path where the video will be stored.
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
    return status, 'Downloaded'

if __name__ == '__main__':
    input_url = str(input("Enter Video Link"))  # Ask the user to write a youtube link
    output = r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\combined_videos\downloadedvid.mp4'
    download_clip(input_url, output)
