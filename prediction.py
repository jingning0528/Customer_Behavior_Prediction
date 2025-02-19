import csv_read_write
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier, StackingClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

import profile_features
import text_features


def train(path):
    profile_features.profile_features_extraction(path)
    text_features.text_features_extraction(path)
    data = np.array(pd.read_csv("data/All_features.csv", low_memory=False))
    label = np.array(pd.read_csv("data/label.csv", low_memory=False))
    train_count = len(data) // 3
    X_train = data[train_count:]
    y_train = label[train_count:]
    clf1 = SVC(kernel='linear', probability=True, class_weight={0: 1, 1: 20}, C=1, random_state=42)
    clf2 = MLPClassifier(random_state=1, max_iter=300)
    clf3 = AdaBoostClassifier(n_estimators=100)
    estimators = [('svm', clf1), ('mlp', clf2), ('ada', clf3)]
    vote_clf = VotingClassifier(estimators=estimators, voting='soft', weights=[1, 1, 1]).fit(X_train, np.ravel(y_train,order='C'))
    model_file = "saved_model.joblib"
    joblib.dump(vote_clf, model_file)
    return vote_clf


def prediction(path_predict, result):
    profile_features.profile_features_extraction(path_predict)
    text_features.text_features_extraction(path_predict)
    data = np.array(pd.read_csv("data/All_features.csv", low_memory=False))
    model_file = "saved_model.joblib"
    clf = joblib.load(model_file)
    pred =clf.predict(data)
    csv_read_write.list_write_csv(result, "prediction_result", pred.tolist())
    print(pred)


# train("data/training_data.csv.csv", "data/label.csv")
# prediction("data/training_data.csv")


