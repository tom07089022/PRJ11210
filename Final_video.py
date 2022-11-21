import cv2
import time
import threading
import random
import csv
import socket
import tqdm
import os
import tensorflow as tf
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path
from LF import Learningfocus
#from PF import Phonefocus
from DR import DoubleReaction
from LRS import LongRepString
from LBP import LBP
#from iottalk import DAN

#--Prepare for global variables--#
graph = tf.get_default_graph()
turnon = True
image = 0
putWord = "Focus"
putWord2 = "Focus"
putWord3 = "wait"
putWord4 = "wait"
ear = 0
lrscounter = 0
drcounter = 0
lbpcounter = 0
randomseed = True
drseed = 3
starttime = 0

#--Load Model--#
doubleReaction = DoubleReaction()
lrs = LongRepString()
lbp = LBP()

#--Turn on Webcam--#
def cam(): 
    videotype = 0
    videosource = 'test_video2.mp4'
    if(videotype==0): cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else: cap = cv2.VideoCapture(videosource)
    fps_start = time.time()
    framecounter = 0
    act = ''
    global turnon, image, putWord, putWord2, putWord3, putWord4, ear

    while (turnon):
        success, img = cap.read()
        if(videotype!=0): time.sleep(1/50)
        image = img
        framecounter += 1
        new_fps_time = time.time()
        FPS = framecounter / (new_fps_time - fps_start)
        
        cv2.rectangle(img, (0, 0), (200, 130), (204, 255, 255), -1)
        cv2.putText(img, "FPS: %.2f" % FPS, (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, "Pose: %s" % putWord, (10, 40), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, "Phone: %s" % putWord2, (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, "LBP Status: %s" % putWord3, (10, 80), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, "Reaction: %s" % putWord4, (10, 100), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, "EAR: %.2f" % ear, (10, 120), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        
        if((time.time() - starttime)<10 and starttime != 0):
            if(drseed == 0):
                act = 'PLEASE RAISE YOUR LEFTHAND'
            elif(drseed == 1):
                act = 'PLEASE RAISE YOUR RIGHTHAND'
            elif(drseed == 2):
                act = 'PLEASE STAND UP'
            cv2.putText(img, '{:^27s}'.format(act), (60, 230), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (0, 0, 255), 2)            

        if((time.time() - starttime)>10 and starttime != 0):
            cv2.putText(img, "FAKE DETECTED", (200, 230), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (0, 0, 255), 2)

        if(framecounter>=300):
            framecounter = 0
            fps_start = time.time()
        
        cv2.imshow("E-learning", img)    

        if ((cv2.waitKey(1) == ord('q')) | (cv2.waitKey(1) == 27)):
            turnon = False
    
    cap.release()
    cv2.destroyAllWindows()

#--Define Liveness Detection System--#
def livenessDetection(flat):
    global image, putWord3, putWord4, ear, lrscounter, drcounter, lbpcounter, randomseed, drseed, starttime, lbp, lrs, doubleReaction
    
    with graph.as_default():
        putWord3, lbppr = lbp.prediction(image)
    
    with graph.as_default():
        repblink, ear = lrs.prediction(image)
    
    with graph.as_default():
        putWord4, drpr = doubleReaction.prediction(flat)
        
    #--To count the continuous frame that LBP result keeps being fake--#
    if(lbppr == 0 and lbpcounter < 100):
        lbpcounter = 0
    else:
        lbpcounter += 1

    #--To count the times that LRS predict as repeated blink string--#
    if(repblink == True):
        lrscounter += 1

    #--The condition to start DR--#
    if(lrscounter >= 2 or lbpcounter >= 100):
        #--Randomly choose the action to do--#
        if(randomseed):
            drseed = random.randint(0, 2)
            print(drseed)
            starttime = time.time()
            randomseed = False        
        #--To count the frames that user do the same action as asked--#
        if(drpr == drseed):
            drcounter += 1    
        #--The condition to pass the DR and initialize the parameters--#
        if(drcounter>=10):
            lbpcounter = 0
            lrscounter = 0
            drcounter = 0
            randomseed = True
            drseed = 3
            starttime = 0
            
#--Turn on Liveness Detection System--#            
def run_LD(): 
    global image, turnon
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368))
    while(turnon):       
        humans = e.inference(image, resize_to_default=True, upsample_size=2.0)
        img, flat = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        livenessDetection(flat)

#--Main Function--#        
if __name__ == '__main__':
    #try:
    learningfocus = Learningfocus()
    #phonefocus = Phonefocus()
    camthreading = threading.Thread(target=cam)
    livenessdetectionthreading = threading.Thread(target=run_LD)
    focusscore = 0
    focuscount = 0
    No = 1
    camthreading.start()
    time.sleep(1)
    #Phonefocus.preparefordata(phonefocus)
    livenessdetectionthreading.start()
    
    while(turnon):  
        PosePredict_Result = Learningfocus.posepredict(learningfocus, image)
        #AxisPredict_Result = Phonefocus.axispredict(phonefocus)

        if(PosePredict_Result==0):
            putWord = "Focus"
        elif(PosePredict_Result==1):
            putWord = "Normal"
        else:
            putWord = "Not Focus"
        
        # if(AxisPredict_Result==0):
            # putWord2 = "Focus"
        # elif(AxisPredict_Result==1):
            # putWord2 = "Normal"
        # elif(AxisPredict_Result==2):
            # putWord2 = "Not Focus"
        # else:
            # putWord2 = "Search"    
            
        if (PosePredict_Result==0):    #and(AxisPredict_Result==0)
            focusscore += 4
        elif (PosePredict_Result==0):    #and(AxisPredict_Result==1)
            focusscore += 3
        elif (PosePredict_Result==1):    #and((AxisPredict_Result==0)or(AxisPredict_Result==1))
            focusscore += 2
        elif (AxisPredict_Result==3):        #and((PosePredict_Result==0)or(PosePredict_Result==1))
            focusscore += 1
        else:
            focusscore = focusscore
        focuscount += 1

        #-Write Current Focus Degree into the CSV file for drawing chart later-#
        if (focuscount==200):
            with open('./Data/focus.csv', 'a', newline='') as csvfile:
                fieldnames = ['No.', 'Focus Degree (%)', 'Time (min)']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'No.':str(No), 'Focus Degree (%)':str('%.2f' % (focusscore*100/(focuscount*4))), 'Time (min)':str(time.strftime("%H:%M:%S", time.localtime()))})
            focusscore = 0
            focuscount = 0
            No += 1
    
    camthreading.join()
    livenessdetectionthreading.join()
    #DAN.deregister()
    #except:
    #DAN.deregister()

    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step

    # the ip address or hostname of the server, the receiver
    host = "127.0.0.1"
    # the port, let's use 5001
    port = 5001
    # the name of file we want to send, make sure it exists
    filename = "./Data/focus.csv"
    # get the file size
    filesize = os.path.getsize(filename)

    # create the client socket
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()        