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
        print("No rotation metadata found")

    return rotateCode

def get_frames(path_video, video_name):
    
    input_vid = cv2.VideoCapture(path_video)
    width = input_vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = input_vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = input_vid.get(cv2.CAP_PROP_FPS)
    
    output_vid = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('m','p','4','v'), fps, (int(width),int(height)))
 
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
    output_vid.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore')
    #import tensorflow as tf
    import cv2
    import os
    import ffmpeg
    import cvlib as cv
    import argparse

    parser = argparse.ArgumentParser(description="Input and output paths")
    parser.add_argument('input_path', type = str, help='Path to input video')
    parser.add_argument('output_path',type = str, help='Output File name')
    args = parser.parse_args()
    input_file = args.input_path
    output_file = args.output_path
    
    get_frames(input_file,output_file)