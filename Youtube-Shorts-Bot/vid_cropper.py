import numpy as np
import cv2
from moviepy.audio import AudioClip
from moviepy.editor import VideoFileClip

def vidCropper(input_path, output_path,
               bin_path=r'C:\Users\ignac\PycharmProjects\youtube_video_bot\Youtube-Shorts-Bot\bin\ar_vid_bin.mp4'):
    """
    Crops an input video into a specified AR. Then stored in output path.
    :param input_path: path for video needed to be edited
    :param output_path: desired output path of new video
    :param bin_path: path of where to store bin video (for local updating)

    Other parameters that can be changed is the AR, which is the aspect ratio. AR selected is 9:16.
    :return:
    """
    # Open the video
    cap = cv2.VideoCapture(input_path)
    sound = VideoFileClip(input_path).audio
    # Initialize frame counter
    cnt = 0

    # Some characteristics from the original video
    w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    #print(w_frame)
    #print(h_frame)

    # Here you can define your croping frames.
    AR = 0.5625 # Standard 9:16
    new_width = int(h_frame*AR)
    new_height = int(h_frame)
    x = int((w_frame-new_width)/2)
    # -5 and +5 specified below to make aspect ratio slightly bigger.
    x, y, h, w = x-5, 0, new_height, new_width+5


    # output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(bin_path, fourcc, fps, (w, h))

    print('..................')
    print('..................')
    print('..................')
    print('Cropping Video...')
    print('..................')
    print('..................')
    print('..................')
    
    
    # Now we start
    while(cap.isOpened()):
        ret, frame = cap.read()
    
        cnt += 1 # Counting frames
    
        # Avoid problems when video finish
        if ret==True:
            # Croping the frame
            crop_frame = frame[y:y+h, x:x+w]
    
            # Percentage
            xx = cnt *100/frames
            print(int(xx),'%')
    
            # Saving from the desired frames
            #if 15 <= cnt <= 90:
            #    out.write(crop_frame)
    
            # I see the answer now. Here you save all the video
            out.write(crop_frame)
    
            # Just to see the video in real time          
            #cv2.imshow('frame',frame)
            #cv2.imshow('croped',crop_frame)
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    final = VideoFileClip(bin_path)
    final.audio = sound
    final.write_videofile(output_path)

    print('..................')
    print('..................')
    print('..................')
    print('Video Cropped')
    print('..................')
    print('..................')
    print('..................')


if __name__ == '__main__':
    video = r'C:\Users\ignac\Downloads\result3.mp4'
    vidCropper(video)
