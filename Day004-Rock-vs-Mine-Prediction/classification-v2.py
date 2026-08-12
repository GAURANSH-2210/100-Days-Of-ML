"""
Sonar classification
My first attempt used train_test_split(test_size=0.1). This script reproduces those numbers, then shows why they
could not support the conclusions I drew from them.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import (train_test_split, RepeatedStratifiedKFold,
                                     cross_val_score, GridSearchCV)
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

URL = "sonar-data.csv"
df = pd.read_csv(URL, header=None)
X = df.drop(60, axis=1)
y = df[60]

print("=" * 72)
print("PART 1 - REPRODUCING MY ORIGINAL 90/10 SPLIT")
print("=" * 72)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, stratify=y, random_state=1)

print(f"train={len(X_train)} rows   test={len(X_test)} rows")
print(f"one test prediction is worth {100/len(X_test):.2f} percentage points\n")

original = {
    "Logistic Regression":    LogisticRegression(max_iter=5000),
    "K-Nearest Neighbors":    KNeighborsClassifier(),
    "Decision Tree":          DecisionTreeClassifier(random_state=1),
    "Support Vector Machine": SVC(),
    "Random Forest":          RandomForestClassifier(random_state=1),
}

for name, model in original.items():
    model.fit(X_train, y_train)
    # NOTE: accuracy_score(y_true, y_pred) — my original had these reversed.
    # Accuracy is symmetric so it didn't change the answer, but the same
    # mistake with precision_score or f1_score would have been silent and wrong.
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    print(f"{name:24s} train={train_acc*100:6.2f}%  test={test_acc*100:6.2f}%  "
          f"({round(test_acc*len(X_test))}/{len(X_test)})  gap={(train_acc-test_acc)*100:5.1f}pts")

# ---------------------------------------------------------------
print("\n" + "=" * 72)
print("PART 2 - PROBLEM A: UNSEEDED TREES ARE A COIN FLIP")
print("=" * 72)

# My original DecisionTreeClassifier() had no random_state.
accs = [accuracy_score(y_test, DecisionTreeClassifier().fit(X_train, y_train).predict(X_test))
        for _ in range(20)]

print("20 runs of DecisionTreeClassifier() with no random_state, identical data:")
print("  " + "  ".join(f"{a*100:.1f}" for a in accs))
print(f"  min={min(accs)*100:.2f}%  max={max(accs)*100:.2f}%  "
      f"spread={(max(accs)-min(accs))*100:.2f} points")

# ---------------------------------------------------------------
print("\n" + "=" * 72)
print("PART 3 - PROBLEM B: THE SPLIT ITSELF IS A LOTTERY")
print("=" * 72)

print("Same LogReg, same code, only random_state of the split changes:")
results = []
for seed in range(10):
    a, b, c, d = train_test_split(X, y, test_size=0.1, stratify=y, random_state=seed)
    model = LogisticRegression(max_iter=5000).fit(a, c)
    results.append(accuracy_score(d, model.predict(b)))

print("  " + "  ".join(f"{a*100:.1f}" for a in results))
print(f"  min={min(results)*100:.2f}%  max={max(results)*100:.2f}%  "
      f"spread={(max(results)-min(results))*100:.2f} points")

print("\n" + "=" * 72)
print("PART 4 - THE FIX: REPEATED STRATIFIED CV (5 x 10 = 50 estimates)")
print("=" * 72)

cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
y_enc = LabelEncoder().fit_transform(y)

fixed = {
    "Logistic Regression":    Pipeline([("s", StandardScaler()), ("m", LogisticRegression(max_iter=5000))]),
    "K-Nearest Neighbors":    Pipeline([("s", StandardScaler()), ("m", KNeighborsClassifier())]),
    "Decision Tree":          DecisionTreeClassifier(random_state=42),
    "Support Vector Machine": Pipeline([("s", StandardScaler()), ("m", SVC(random_state=42))]),
    "Random Forest":          RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=42),
}

rows = []
for name, model in fixed.items():
    scores = cross_val_score(model, X, y_enc, cv=cv, scoring="accuracy", n_jobs=-1)
    rows.append({
        "model": name, "mean": scores.mean()*100, "std": scores.std()*100,
        "min": scores.min()*100, "max": scores.max()*100,
        "95%_lo": (scores.mean()-1.96*scores.std())*100,
        "95%_hi": (scores.mean()+1.96*scores.std())*100,
    })

print(pd.DataFrame(rows).sort_values("mean", ascending=False)
      .to_string(index=False, float_format=lambda v: f"{v:.2f}"))

print("\n" + "=" * 72)
print("PART 5 - TUNING, DONE WITHOUT LEAKAGE")
print("=" * 72)

grid = GridSearchCV(
    Pipeline([("s", StandardScaler()), ("m", SVC(random_state=42))]),
    {"m__C": [0.1, 1, 10, 100], "m__gamma": ["scale", 0.01, 0.1]},
    cv=cv, scoring="accuracy", n_jobs=-1,
)
grid.fit(X, y_enc)
print(f"best params: {grid.best_params_}")
print(f"CV accuracy: {grid.best_score_*100:.2f}%")