import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso, RidgeCV, LassoCV
from sklearn.metrics import r2_score

X, y = load_diabetes(as_frame=True, return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("shape:", X.shape)

for degree in [1, 2, 3]:
    n_feat = PolynomialFeatures(degree, include_bias=False).fit_transform(X_train).shape[1]

    ols = make_pipeline(PolynomialFeatures(degree, include_bias=False),
                        StandardScaler(), LinearRegression()).fit(X_train, y_train)
    ridge = make_pipeline(PolynomialFeatures(degree, include_bias=False),
                          StandardScaler(), Ridge(alpha=10)).fit(X_train, y_train)

    print(f"deg={degree} feats={n_feat:4d} | "
          f"OLS train R2={r2_score(y_train, ols.predict(X_train)):.3f} "
          f"test R2={r2_score(y_test, ols.predict(X_test)):7.3f} | "
          f"Ridge test R2={r2_score(y_test, ridge.predict(X_test)):.3f}")

print("\n-- alpha sweep (Lasso, degree-1) --")
for alpha in [0.001, 0.01, 0.1, 0.5, 1, 2, 5]:
    pipe = make_pipeline(StandardScaler(), Lasso(alpha=alpha, max_iter=10000)).fit(X_train, y_train)
    n_nonzero = (pipe[-1].coef_ != 0).sum()
    print(f"alpha={alpha:<6} nonzero coefs={n_nonzero:2d}/10  "
          f"test R2={r2_score(y_test, pipe.predict(X_test)):.4f}")

print("\n-- built-in CV selection --")
ridge_cv = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 50))).fit(X_train, y_train)
lasso_cv = make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=42, max_iter=10000)).fit(X_train, y_train)

print(f"RidgeCV best alpha={ridge_cv[-1].alpha_:.4f}  test R2={r2_score(y_test, ridge_cv.predict(X_test)):.4f}")
print(f"LassoCV best alpha={lasso_cv[-1].alpha_:.4f}  test R2={r2_score(y_test, lasso_cv.predict(X_test)):.4f}")
print("\nLasso kept features:", list(X.columns[lasso_cv[-1].coef_ != 0]))