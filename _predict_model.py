import numpy as np
import pandas as pd

def predict_sequences(model, data):
    prediction_seqs = []
    for curr_frame in data:
        predicted = model.predict(curr_frame[np.newaxis,:,:])
        prediction_seqs.append(predicted)
    return np.array(prediction_seqs)

def bundle_predicted_actual(true, pred):
    res = pd.DataFrame()
    res['true_bin'] = np.where(true < 0, -1, 1)
    res['pred_bin'] = np.where(pred < 0, -1, 1)
    res['true']  = true
    res['pred'] = pred
    return res