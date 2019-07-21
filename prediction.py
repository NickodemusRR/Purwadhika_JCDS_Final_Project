import joblib
from sklearn.preprocessing import binarize
logreg = joblib.load('model')
def prediction(X):
    """return the prediction result of given X features
    ['male' 'age' 'currentSmoker' 'cigsPerDay' 'BPMeds' 'prevalentStroke' 'prevalentHyp' 
    'diabetes' 'totChol' 'sysBP' 'diaBP' 'BMI' 'heartRate']
    """
    pred_prob = logreg.predict_proba(X)
    prediction = binarize(pred_prob, 0.1)[:,1]
    return prediction[0]