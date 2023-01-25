import requests, json
import matplotlib.pyplot as plt
import re

# Adapted from https://github.com/Benjamin-Loison/YouTube-operational-API

def getContentFromURL(url):
    return requests.get(url).text

url = str(input("Enter Video Link")) # Ask the user to write a youtube link
# videoID finds the id of the video usually between the first = and &
videoID = re.findall('=(.*?)&', url) # Find between = and &

videoId = videoID[0] # Obtain the first id
url = f'https://yt.lemnoslife.com/videos?part=mostReplayed&id={videoId}' # Download youtube video data per videoID

content = getContentFromURL(url)
data = json.loads(content) # Download content of data

# Do a dictionary // list search to find the mostReplayed parameters
start_timestamp = data['items'][-1]['mostReplayed']['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeStartMillis']
end_timestamp = data['items'][-1]['mostReplayed']['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeEndMillis']

print(start_timestamp)
print(end_timestamp)

"""time = re.search(r'visibleTimeRangeStartMillis":\s*(.*?),', data)
print(time)"""


"""Y = []
for heatMarker in data['items'][0]['mostReplayed']['heatMarkers']:
    heatMarker = heatMarker['heatMarkerRenderer']
    intensityScoreNormalized = heatMarker['heatMarkerIntensityScoreNormalized']
    Y += [intensityScoreNormalized]

plt.plot(Y)
plt.show()
print(Y)"""