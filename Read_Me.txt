/**********Customer Behaviour Prediction***********/

Please see example.py for usage.

    When you want to update the model: 

    # Training
    original_data = "data/training_data.csv"
    profile_features.profile_features_extraction(original_data)
    text_features.text_features_extraction(original_data)
    prediction.train()

    When you want to do a prediction:
    
    # Prediction
    predict_data = "data/training_data.csv"
    predict_result = "data/prediction_result.csv"
    prediction.prediction(predict_data, predict_result)



1. Feature Extraction
    There are two part in the feature extraction: profile and text. All the features will be used in training and prediction.
	
2. Training
    After the first training, a model will be saved named "saved_model.joblib". You don't have to train model every time unless you have new labeled dataset and want to update the model.

3. Prediction
    You can write result in the same file and there will be a new column named "predict_result".
    