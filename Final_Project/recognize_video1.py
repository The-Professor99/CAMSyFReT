from imutils.video import VideoStream, FPS
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
import time
from datetime import datetime
import pandas as pd
from os import path

classNames = ["unknown"]
names_and_time = []
all_names = []
directory = path.dirname(__file__)
from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def mark_attendance(name, probability):
    capture_time = datetime.now().strftime("%Y-%m-%d")
    details = {
        "Student's Name": name,
        capture_time: str(round(probability * 100, 3)) + "%",
    }
    names_and_time.append(details)
    classNames.append(name)


def pandas_manipulation():
    file_name = path.join(directory, 'attendance_records', 'Attendance_Records.csv')

    try:
        v = pd.read_csv(file_name)
        try:
            v.drop(
                [
                    "Unnamed: 0",
                    "Total Number of classes Held",
                    "Total Number of classes Attended",
                    "Percentage Attendance",
                ],
                axis=1,
                inplace=True,
            )
        except KeyError:
            v = pd.DataFrame()
            v["Student's Name"] = all_names
    except FileNotFoundError:
        v = pd.DataFrame()
        v["Student's Name"] = all_names
    # print(v)
    classNames.remove("unknown")
    captured = set(classNames)
    # print("Captured: ", captured)
    attendance = {}
    for name in all_names:
        if name in captured:
            individual_attendance = {name: 1}
        else:
            individual_attendance = {name: 0}
        attendance.update(individual_attendance)
    capture_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    v[capture_time] = v["Student's Name"].map(attendance)
    j = 0
    for i in v.columns:
        if is_date(i):
            j += 1
    v["Total Number of classes Attended"] = v.values[:, 1:].sum(axis=1)
    v["Total Number of classes Held"] = j
    v["Percentage Attendance"] = (
        v["Total Number of classes Attended"] / v["Total Number of classes Held"]
    ) * 100
    v["Percentage Attendance"] = v["Percentage Attendance"].astype("float").round()
    return v


def save_attendance_records(records, path):
    records = pandas_manipulation()
    if not os.path.exists(path):
        # print("Creating Folder!")
        os.makedirs(path)
    file_name =  "Attendance_Records.csv"
    # print(file_name)
    # print(path)
    full_path = os.path.join(directory, path, file_name)
    # print(full_path)
    records.to_csv(full_path)


def takeAttendance(confidence_set):
    # print("[INFO] loading face detector...")
    protoPath = path.join(directory, 'constants', 'deploy.prototxt.txt')
    modelPath = path.join(directory, 'constants', 'res10_300x300_ssd_iter_140000.caffemodel')
    detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
    confidence_used = confidence_set

    # load our serialized face embedding model from disk
    # print("[INFO] loading face recognizer...")
    model_path = path.join(directory, "openface_nn4.small2.v1.t7")

    embedder = cv2.dnn.readNetFromTorch(model_path)

    # load the actual face recognition model along with the label encoder
    recognizer_path = path.join(directory, 'output', 'recognizer.pickle')

    recognizer = pickle.loads(open(recognizer_path, "rb").read())
    le_path = path.join(directory, 'output', 'le.pickle')
    le = pickle.loads(open(le_path, "rb").read())

    # initialize the video stream then allow the camera sensor to warm up
    # print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

    # start the FPS throughput estimator
    fps = FPS().start()

    # loop over the frames from the video stream
    while True:
        frame = vs.read()

        # resize the frame to have a width of 600 pixels ( while maintaining the aspect
        # ratio), and then grab the image dimensions
        frame = imutils.resize(frame, width=600)
        (h, w) = frame.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),
            1.0,
            (300, 300),
            (104.0, 177.0, 123.0),
            swapRB=False,
            crop=False,
        )

        # apply OpenCV's deep learning-based face detector to localize faces in the
        # input image
        detector.setInput(imageBlob)
        detections = detector.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections
            if confidence > confidence_used:
                # print("confidence: ", confidence, confidence_used)
                # compute the (x, y) -coordinates of the bounding box for the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI
                face = frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                # construct a blob for the face ROI, then pass the blob through the face
                # embedding model to obtain the 128-d quantification of the face
                faceBlob = cv2.dnn.blobFromImage(
                    face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False
                )
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                # perform classification to recognize the face
                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]
                if not len(all_names):
                    # print(le.classes_)
                    untitled_names = list(le.classes_)
                    untitled_names.remove("unknown")
                    to_titlecase = []
                    for name in untitled_names:
                        name = name.title()
                        to_titlecase.append(name)
                    untitled_names = to_titlecase
                    all_names.extend(untitled_names)
                    # print(all_names, "Names")
                if proba < 0.6:
                    # print("Prior Name: ", name)
                    name = "unknown"
                # print("Probability Measured: ", proba)
                # print("Name Gained: ", name)
                if name not in classNames:
                    mark_attendance(name, proba)

                # draw the bounding box of the face along with the associated probability
                text = "{}: {:.2f}%".format(name, proba * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                if name != "unknown":
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        text,
                        (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.45,
                        (0, 255, 0),
                        2,
                    )
                else:
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    cv2.putText(
                        frame,
                        text,
                        (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.45,
                        (0, 0, 255),
                        2,
                    )

        fps.update()

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            break

    fps.stop()
    folder_path = "attendance_records/"
    # print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    # print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    cv2.destroyAllWindows()
    vs.stop()
    if len(names_and_time):
        save_attendance_records(names_and_time, folder_path)
        return names_and_time
    else:
        return None
