import pandas as pd
import moviepy as mp
import cv2
import os
import ffmpeg
import cvlib as cv
import matplotlib.pyplot as plt

def check_rotation(path_video_file):
    # this returns meta-data of the video file in form of a dictionary
    meta_dict = ffmpeg.probe(path_video_file)

    # from the dictionary, meta_dict['streams'][0]['tags']['rotate'] is the key
    # we are looking for
    rotateCode = None
    try:
        if int(meta_dict['streams'][0]['tags']['rotate']) == 90:
            rotateCode = cv2.ROTATE_90_CLOCKWISE
        elif int(meta_dict['streams'][0]['tags']['rotate']) == 180:
            rotateCode = cv2.ROTATE_180
        elif int(meta_dict['streams'][0]['tags']['rotate']) == 270:
            rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE
    except:
        print("No metadata found")

    return rotateCode

def get_frames(path_video, video_name):
    input_vid = cv2.VideoCapture(path_video)
    width = input_vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = input_vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    output_vid = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('m','p','4','v'), 29.89, (int(width),int(height)))
 
    rotate_code = check_rotation(path_video)
    currentFrame = 0

    while(True):
        ret, frame = input_vid.read()
        if ret:
            #name = './Videos/frames/frame'+str(currentFrame)+'.jpg'
            print('Working on Frame: {}'.format(currentFrame))
            if rotate_code is not None:
                frame = cv2.rotate(frame, rotate_code)
            #cv2.imwrite(name,frame)
            bbox, label, conf = cv.detect_common_objects(frame)
            output = cv.object_detection.draw_bbox(frame, bbox, label,conf)
            output_vid.write(output)

            currentFrame += 1
        else:
            break

    input_vid.release()
    cv2.destroyAllWindows()

#input_vid = 'Videos\\input.mp4'
#test = 'Videos\\test2.mp4'
#get_frames(input_vid)

def get_objects(image_folder):
    currentFrame = 0
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    #frame = cv2.imread(os.path.join(image_folder, images[0]))
    for image in images:
        frame = cv2.imread(os.path.join(image_folder, image))
        
        bbox, label, conf = cv.detect_common_objects(frame)
        output = cv.object_detection.draw_bbox(frame, bbox, label,conf)
        out_name = './Videos/output/frame'+str(currentFrame)+'.jpg'

        print("Identifying Object in Frame: {}".format(currentFrame))
        cv2.imwrite(out_name, output)
        currentFrame += 1

#get_objects()

def get_video(image_folder, video_name):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('m','p','4','v'), 29.89, (width,height))
    number  = 0
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
        print('Writing Frame:{}'.format(number))
        number += 1

    cv2.destroyAllWindows()
    video.release()


#image_folder = 'Videos\\output'
#ideo_name = 'video.mp4'
#get_video(image_folder, video_name)

#import cv2
#import os
if __name__ == "__main__":
    get_frames('Videos\\test2.mp4','output_2.mp4')
    #get_objects('Videos\\frames')
    #get_video('Videos\\output','output_2.mp4')