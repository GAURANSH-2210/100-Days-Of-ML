import numpy as np
import pandas as pd
import time
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (RandomForestRegressor, GradientBoostingRegressor,
                              HistGradientBoostingRegressor)
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = sns.load_dataset("diamonds")

mask = (df[["x", "y", "z"]] > 0).all(axis=1) & (df["y"] < 30) & (df["z"] < 30)
df = df[mask].copy()

cut_order     = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
color_order   = ["J", "I", "H", "G", "F", "E", "D"]
clarity_order = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

num_cols = ["carat", "depth", "table", "x", "y", "z"]
cat_cols = ["cut", "color", "clarity"]

X = df[num_cols + cat_cols]
y = np.log(df["price"])

preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OrdinalEncoder(categories=[cut_order, color_order, clarity_order]), cat_cols),
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Linear":        LinearRegression(),
    "Ridge":         Ridge(alpha=1.0),
    "Lasso":         Lasso(alpha=0.001, max_iter=5000),
    "ElasticNet":    ElasticNet(alpha=0.001, l1_ratio=0.5, max_iter=5000),
    "KNN(k=10)":     KNeighborsRegressor(n_neighbors=10, n_jobs=-1),
    "DecisionTree":  DecisionTreeRegressor(max_depth=10, random_state=42),
    "RandomForest":  RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=42),
    "GradBoost":     GradientBoostingRegressor(random_state=42),
    "HistGradBoost": HistGradientBoostingRegressor(random_state=42),
}

rows = []
for name, model in models.items():
    pipe = Pipeline([("pre", preprocess), ("model", model)])

    start = time.time()
    pipe.fit(X_train, y_train)
    fit_time = time.time() - start

    pred_log = pipe.predict(X_test)

    true_dollars = np.exp(y_test)
    pred_dollars = np.exp(pred_log)

    rows.append({
        "model":    name,
        "R2_log":   r2_score(y_test, pred_log),
        "RMSE_log": np.sqrt(mean_squared_error(y_test, pred_log)),
        "MAE_$":    mean_absolute_error(true_dollars, pred_dollars),
        "MAPE_%":   np.mean(np.abs(true_dollars - pred_dollars) / true_dollars) * 100,
        "fit_s":    fit_time,
    })

results = pd.DataFrame(rows).sort_values("R2_log", ascending=False)
print(results.to_string(index=False, float_format=lambda v: f"{v:.4f}"))