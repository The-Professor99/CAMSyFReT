from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
from os import path


def extractEmbeddings(confidence_set):
    # Load our serialized face detector from disk
    # print("[INFO] loading face detector...")
    directory = path.dirname(__file__)
    protoPath = path.join(directory, 'constants', 'deploy.prototxt.txt')
    modelPath = path.join(directory, 'constants', 'res10_300x300_ssd_iter_140000.caffemodel')
    detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

    # Load our serialized face embedding model from disk
    # print("[INFO] loading face recognizer...")
    model_path = path.join(directory, "openface_nn4.small2.v1.t7")

    embedder = cv2.dnn.readNetFromTorch(model_path)

    # print("[INFO] quantifying faces...")
    dataset_path = path.join(directory, 'changes', 'dataset')
    imagePaths = list(paths.list_images(dataset_path))
    # print("Image Paths: ", imagePaths)
    confidence_used = confidence_set

    # initialize our lists of extracted facial embeddings and corresponding people names
    knownEmbeddings = []
    knownNames = []

    # initialize the total number of faces processed
    total = 0

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        # print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
        # print("Image Path checking: ", imagePath)
        name = imagePath.split(os.path.sep)[-2]
        # print("Image Path Name: ", name)

        # load the image, resize it to have a width of 600 pixels (while maintaining the aspect ratio), and then grab the image dimensions
        image = cv2.imread(imagePath)
        images = image.copy()
        image = imutils.resize(image, width=600)
        (h, w) = image.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)),
            1.0,
            (300, 300),
            (104.0, 177.0, 123.0),
            swapRB=False,
            crop=False,
        )

        # apply OpenCV's deep learning based face detector to localize faces in the input image
        detector.setInput(imageBlob)
        detections = detector.forward()

        # ensure at least one face was found
        if len(detections) > 0:
            # we're making the assumption that each image has only one face
            # so find the bounding box with the largest probability
            i = np.argmax(detections[0, 0, :, 2])
            confidence = detections[0, 0, i, 2]

            # ensure that the detection with the largest probability also means
            # our minimum probability test (thus helping filter out weak detections)
            if confidence > confidence_used:
                # print("Confidence passed")
                # compute the (x, y) -coordinates of the bounding box for the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI and grab the ROI dimensions
                # print("startx, y, endx, y: ", startX, startY, endX, endY)
                face = image[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]
                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                # construct a blob for the face ROI, then pass the blob through our face
                # embedding model to obtain the 128-d quantification of the face
                faceBlob = cv2.dnn.blobFromImage(
                    face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False
                )
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                # add the name of the person + corresponding face embedding to their
                # respective lists
                knownNames.append(name)
                knownEmbeddings.append(vec.flatten())
                total += 1
    # else:

    # print("Else Path: ", imagePath)
    # dump the facial embeddings + names to disk
    # print("[INFO] serializing {} encodings...".format(total))
    data = {"embeddings": knownEmbeddings, "names": knownNames}
    # print("All Data: ", knownNames)
    embeddings_path = path.join(directory, 'output', 'embeddings.pickle')
    f = open(embeddings_path, "wb")
    f.write(pickle.dumps(data))
    f.close()
    return "Embeddings Extracted"
