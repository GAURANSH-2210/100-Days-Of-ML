import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

sonar_data=pd.read_csv("sonar-data.csv", header=None)
print(sonar_data.shape)
print(sonar_data.describe())
print(sonar_data.groupby(60).mean())
X=sonar_data.drop(60, axis=1)
y=sonar_data[60]
print(X)
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, stratify=y, random_state=1)

models = {
    'Logistic Regression': LogisticRegression(),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Decision Tree': DecisionTreeClassifier(),
    'Support Vector Machine': SVC(),
    'Random Forest': RandomForestClassifier(random_state=1)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    X_train_prediction=model.predict(X_train)
    X_test_prediction=model.predict(X_test)
    train_accuracy=accuracy_score(X_train_prediction, y_train)
    test_accuracy=accuracy_score(X_test_prediction, y_test)
    print(f"Model: {name}")
    print(f"Accuracy on training data : {train_accuracy*100:.2f}%")
    print(f"Accuracy on test data : {test_accuracy*100:.2f}%")
    print("-"*30) 