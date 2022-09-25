from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import numpy as np
import pandas as pd
import csv
import sys
from os import path

# load OpenCV's haar cascade for face detection from disk
def start_capture(name, prototxt_file, model_file, output_folder, confidence):
    
    directory = path.dirname(__file__)
    # print("Starting")
    # print(prototxt_file)
    #     prototxt_file = "constants/deploy.prototxt.txt" # make sure these initializations are present before continuing
    #     model_file = "constants/res10_300x300_ssd_iter_140000.caffemodel"
    confidence_used = 0.85
    #     output_folder = "changes/datasets" # make sure these initializations are present before continuing
    name = name.replace(" ", "_")
    # print(name)
    output_folder = os.path.join(directory, output_folder, name)
    # print("Output folder", output_folder)

    # print("[INFO] loading model...")
    prototxt_file = path.join(directory, 'constants', 'deploy.prototxt.txt')
    model_file = path.join(directory, 'constants', 'res10_300x300_ssd_iter_140000.caffemodel')
    net = cv2.dnn.readNetFromCaffe(prototxt_file, model_file)

    # print("Path: ", output_folder)
    path_ = output_folder
    if not os.path.exists(path_):
        # print("Non-Existent path")
        os.makedirs(path_)

    # print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    total = 0

    while True:
        frame = vs.read()
        orig = frame.copy()
        frame = imutils.resize(frame, width=400)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123)
        )

        # pass the blob through the network and obtain the detections and predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]
            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence < confidence_used:
                continue
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the bounding box of the face along with the associated
            # probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
            cv2.putText(
                frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2
            )

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10) & 0xFF

        if key == ord("k"):
            # print(key)
            p = os.path.sep.join([output_folder, "{}.png".format(str(total).zfill(5))])
            # print("z_fill: ", p)
            cv2.imwrite(p, orig)
            total += 1
        elif key == ord("q"):
            break

    # print("[INFO] {} face images stored".format(total))
    # print("[INFO] saving user's information...")
    # with open("./students_data/school_information.csv", "r+") as file_object:

    cv2.destroyAllWindows()
    vs.stop()
    return total


# capture_biometrics("Eze Ihechi Festus", "uj/2014/3n/sl")
