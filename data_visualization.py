import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():

    # INPUTS
    labeled_data_dir = "./labeled/"
    n = 4 # sequence to study (0,1,2,3 or 4)
    show_video = False
    
    files_list = os.listdir(labeled_data_dir)
    files_list.sort()
    files_list_videos = []
    files_list_txt = []
    for file in files_list:
        if file[-3:] == "txt":
            files_list_txt.append(file)
        if file[-3:] == "mp4":
            files_list_videos.append(file)

    my_video = cv2.VideoCapture("".join((labeled_data_dir,files_list_videos[n])))

    if(my_video.isOpened() == False):
        print("Error opening video file.")

    if show_video:
        while(my_video.isOpened()):
            ret,frame = my_video.read()
            if ret == True:
                cv2.imshow("Frame",frame)
                k = cv2.waitKey(50)
                if k == 113:  # ASCII code for 'q' key
                    break
            else:
                break


    # Text files
    direction_of_travel = np.loadtxt(("".join((labeled_data_dir,files_list_txt[n]))),delimiter=" ")
    pitch_angle_rad = direction_of_travel[:,0]
    yaw_angle_rad = direction_of_travel[:,1]
    N = len(pitch_angle_rad)
    fps = 20
    time = np.linspace(0,N/fps,N)

    fig,(ax1,ax2) = plt.subplots(nrows=2,ncols=1)
    ax1.plot(time,pitch_angle_rad)
    ax1.set_ylabel("Pitch angle (radians)")
    ax1.set_xlim(0,time[-1])
    ax1.set_title(files_list_txt[n])
    ax2.plot(time,yaw_angle_rad)
    ax2.set_ylabel("Yaw angle (radians)")
    ax2.set_xlabel("Time (seconds)")
    ax2.set_xlim(0,time[-1])
    plt.show()

if __name__ == '__main__':
    main()