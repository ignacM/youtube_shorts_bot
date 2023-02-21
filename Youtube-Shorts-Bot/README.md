# Youtube-Shorts-Bot
 This bot uses a downloaded screensaver video and a user input YouTube link to edit and generate a video.
1. The bot downloads the most replayed clip from a YouTube video. 
2. Combines it with a saved screensaver video.
3. Then, using an AI, subtitles are generated and printed onto the video. 
4. Background music is edited onto the video
5. Finally, the video is uploaded to YouTube

[main2.py](main2.py) can be used instead to download a video with given timestamps.
   
The bot has other uses that can be called to main:
1. Adding sound effect randomly or in a specified location 
2. Adjusting video Aspect Ratio
# Set up the Bot
 1. Install The Necessary Libraries: pip install -r requirements.txt<br>
2. Download a video containing a lot of clips (screensaver location)
3. Check locations in main.py
4. Add pvleopard key (in subbing2 function inside of [vid_editer.py](vid_editer.py))
5. Get a YouTube link and run main.py
