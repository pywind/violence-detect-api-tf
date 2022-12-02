import numpy as np
import cv2
from collections import deque


def predict_by_video_path(model, video, limit=None):

    #print("Loading model ...")
    
    Q = deque(maxlen=128)
    IMG_SIZE = 128
    vs = cv2.VideoCapture(video)
    count = 0
    while True:
        (grabbed, frame) = vs.read()
        ID = vs.get(1)
        if not grabbed:
            break
        try:
            if (ID % 7 == 0):
                count = count + 1
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE)).astype("float32")
                frame = frame.reshape(IMG_SIZE, IMG_SIZE, 3) / 255
                preds = model.predict(np.expand_dims(frame, axis=0))[0]
                Q.append(preds)

                #i = (preds > 0.75)[0]  # np.argmax(results)
                #label = i
                #text = "Violence: {}".format(i)
                #print('prediction:', preds)
                #file = open("output.txt", 'w')
                #file.write(text)
                #file.close()

                #writer.write(output)
                #cv2.imshow("Output", output)
            if limit and count > limit:
                break
        except:
            break
    print("Cleaning up...")
    vs.release()
    results = np.array(Q).mean(axis=0)[0]
    return (results > 0.75, results) 

if __name__ == "__main__":
    #predict_by_video_path('V_7.mp4', limit=30)
    print("predict with video")