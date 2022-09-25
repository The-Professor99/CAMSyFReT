from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle
from .extract_embeddings1 import extractEmbeddings
from os import path


def train_model(confidence):
    directory = path.dirname(__file__)
    extractEmbeddings(confidence)
    # print("[INFO] loading face embeddings...")
    embeddings_path = path.join(directory, 'output', 'embeddings.pickle')
    data = pickle.loads(open(embeddings_path, "rb").read())

    # encode the labels
    # print("[INFO] encoding labels...")
    le = LabelEncoder()
    labels = le.fit_transform(data["names"])

    # train the model used to accept the 128-d embeddings of the face and then produce
    # the actual face recognition
    # print("[INFO] training model...")
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(data["embeddings"], labels)

    # write the actual face recognition model to disk
    recognizer_path = path.join(directory, 'output', 'recognizer.pickle')
    f = open(recognizer_path, "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    # write the label encoder to disk
    encoder_path = path.join(directory, 'output', 'le.pickle')
    f = open(encoder_path, "wb")
    f.write(pickle.dumps(le))
    f.close()
    return 1
