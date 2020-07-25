import receive
import extract
import os
import numpy as np
import time
from pygame import mixer
from tensorflow.keras.models import load_model

# from keras.models import load_model

clf_list = []
now_time = 0
pre_time = 0
sound_path = os.path.join(extract.path, "sounds")


def get_model():
    path = os.path.join(extract.path, "models")
    print(os.listdir(path))
    model_name = os.path.join(path, input("Select Model (Copy and Paste it): "))
    model = load_model(model_name)
    return model


def realtime_classification(model, data):
    # model = get_model()
    path = os.path.join(extract.path, "patterns")
    pattern_names = os.listdir(path)
    model.predict(data)
    pattern_idx = int(np.argmax(model.predict(data)))
    pred = pattern_names[pattern_idx]
    return pred


def realtime_prediction(clf):
    global clf_list
    global now_time
    global pre_time
    global sound_path

    if clf != "normal":
        now_time = time.time()
        if (now_time - pre_time) > 1:
            clf_list.append(clf)
            if (len(clf_list) >= 3) & (len(set(clf_list)) == 1):
                print(clf_list[-1])
                if os.path.exists(sound_path):
                    mixer.init()
                    mixer.music.load(os.path.join(sound_path, clf))
                    mixer.music.set_volume(0.5)
                    mixer.music.play()
                pre_time = time.time()
                clf_list = []


if __name__ == "__main__":
    model = get_model()
