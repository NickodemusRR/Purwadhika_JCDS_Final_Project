import numpy as np 
import pandas as pd 
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import binarize
data = pd.read_csv('./dataset/framingham.csv')
data.drop(['education', 'glucose'], axis=1, inplace=True)
data.dropna(inplace=True)
X = data.drop('TenYearCHD', axis=1)
y = data['TenYearCHD']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
logreg = LogisticRegression(solver='liblinear')
logreg.fit(X_train, y_train)
joblib.dump(logreg, 'model')