from pytube import YouTube
# Input url for automatic download of videos
url = "https://www.youtube.com/results?search_query=free+to+use+gameplay"

# Connect to the YouTube URL
yt = YouTube(url)

# Get the 5 first videos
videos = yt.streams.filter(progressive=True, file_extension='mp4').all()[:5]

download_folder = '/screensaver'
# Download the videos
for vid in videos:
    vid.download("videos", output_path=download_folder)