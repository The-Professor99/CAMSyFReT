from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle
from .extract_embeddings1 import extractEmbeddings
from os import path

def resourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        
        base_path = sys._MEIPASS
        base_path = path.join(base_path, "Final_Project")
    except Exception:
        base_path = path.dirname(__file__)
    return path.join(base_path, relative_path)
    
def train_model(confidence):
    directory = path.dirname(__file__)
    extractEmbeddings(confidence)
    # print("[INFO] loading face embeddings...")
    embeddings_path = resourcePath(path.join('output', 'embeddings.pickle')) #path.join(directory, 'output', 'embeddings.pickle')
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
    recognizer_path =  resourcePath(path.join('output', 'recognizer.pickle')) #path.join(directory, 'output', 'recognizer.pickle')
    f = open(recognizer_path, "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    # write the label encoder to disk
    encoder_path = resourcePath(path.join('output', 'le.pickle')) #path.join(directory, 'output', 'le.pickle')
    f = open(encoder_path, "wb")
    f.write(pickle.dumps(le))
    f.close()
    return 1
