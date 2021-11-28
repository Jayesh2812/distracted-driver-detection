import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow import Graph
import json
import numpy as np



with  open('./labels.json','r') as f:
    labelInfo=f.read()

labelInfo=json.loads(labelInfo)

model=load_model('./PNP.h5')

def classify():
    pass
def display_img():
    path='./'
    img=image.load_img(os.path.join(path,'img_100286.jpg') ,target_size=(280,200))
    x=image.img_to_array(img)
    x=x/255
    x=x.reshape(1,280,200,3)

    print("this is x",x.shape)
    pred=model.predict(x)

    print(pred)
    pred = list(pred[0])
    max_val = max(pred)
    label_index = pred.index(max_val)
    print(max_val, pred.index(max_val))
    # if pred[0][0]<0.5:
    #     predictedlabel='Normal'
    # else:
    #     predictedlabel='Pneumonia'
    # predictedlabel=labelInfo[str(np.argmax(pred[0]))]
    # print(predictedlabel)
    # context={
    #     'label':predictedlabel,
    #     'prob':pred[0][0],
    # }

    label_list = ["drinking",
"hair and makeup",
"operating the radio",
"reaching behind",
"safe driving",
"talking on the phone - left",
"talking on the phone - right",
"talking to passenger",
"texting - left",
"texting - right"]
    print(label_list[label_index])


display_img()