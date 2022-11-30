from sklearn import svm, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression

from sklearn import model_selection
from sklearn.model_selection import cross_validate, cross_val_score, cross_val_predict

from sklearn.metrics import accuracy_score

import math

import pickle
import numpy as np
import pandas as pd
import json


def cal_rad(arr):
    rad = []
    
    a = math.atan2(arr["x"][0] - arr["x"][1], arr["y"][0] - arr["y"][1]) - math.atan2(arr["x"][1] - arr["x"][2], arr["y"][1] - arr["y"][2])
    # print(a)
    rad.append(a)
    b = math.atan2(arr["x"][1] - arr["x"][2], arr["y"][1] - arr["y"][2]) - math.atan2(arr["x"][2] - arr["x"][3], arr["y"][2] - arr["y"][3])
    rad.append(b)
    
    PI = math.pi
    
    deg = [(rad[0]*180)/PI, (rad[1]*180)/PI]
    # print(deg[0])
    
    return deg


def get_data():
    data = pd.read_json('pose.json')
    print(data.info())
    meta_x = []
    
    # x = data.iloc[:,:4].values
    # 인식 가능한 자료형으로 변환
    for row in data.iloc:
        # print(row["arm_left"])
        deg = [cal_rad(row["arm_left"])[0], cal_rad(row["arm_left"])[1], cal_rad(row["arm_right"])[0], cal_rad(row["arm_right"])[1], cal_rad(row["leg_left"])[0], cal_rad(row["leg_left"])[1], cal_rad(row["leg_right"])[0], cal_rad(row["leg_right"])[1]]
        # deg.append(cal_rad(row["arm_right"]))
        # deg.append(cal_rad(row["leg_left"]))
        # deg.append(cal_rad(row["leg_right"]))

        meta_x.append(deg)
        
    x = np.array(meta_x)
    # print(x.shape)
    
    y = data.iloc[:,4].values
    # print(y.shape)
    
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x,y,test_size=0.1)
    # print(x_train.shape)
    # print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)
    
    return x_train, x_test, y_train, y_test
    
# get_data()

def make_model():
    # model = svm.SVC(kernel = 'linear')
    # model = tree.DecisionTreeClassifier()
    model = RandomForestClassifier(n_jobs = 6)
    # model = SGDClassifier() # 0.4
    # model = LogisticRegression() # 0.7
    
    print(model)
    
    return model

# make_model()


def do_train():
    # 데이터 호출
    x_train, x_test, y_train, y_test = get_data()
    
    # print(x_train.shape)
    # print(y_train.shape)
    
    model = make_model()
    # gram_train = np.dot(x_train, x_train.T)
    
    model.fit(x_train, y_train)
    
    print("학습 완료")
    
    scores = model.score(x_test, y_test)
    
    # print(scores)
    
    # gram_test = np.dot(x_test, x_train.T)
    
    y_pred = model.predict(x_test)
    
    accuracy = accuracy_score(y_test, y_pred)

    print(accuracy)
    
    pickle.dump(model,open("model_linear.m","wb"))
    
    
do_train()