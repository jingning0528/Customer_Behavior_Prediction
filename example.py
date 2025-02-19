import prediction
import profile_features
import text_features
import time


def example():
    start = time.time()

    # Training

    #original_data = "data/training_data.csv"
    #prediction.train(original_data)

    # Prediction
    predict_data = "data/training_data.csv"
    predict_result = "data/training_data.csv"
    prediction.prediction(predict_data, predict_result)

    end = time.time()
    print("Run time:"+str(end-start))


example()
