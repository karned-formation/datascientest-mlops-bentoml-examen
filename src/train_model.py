import bentoml
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from sklearn.preprocessing import StandardScaler

X_train = pd.read_csv('../data/processed/X_train.csv')
y_train = pd.read_csv('../data/processed/y_train.csv')
X_test = pd.read_csv('../data/processed/X_test.csv')
y_test = pd.read_csv('../data/processed/y_test.csv')

colonnes = ['GRE Score', 'TOEFL Score', 'CGPA']
scaler_std = StandardScaler()
X_train[colonnes] = scaler_std.fit_transform(X_train[colonnes])

model = LinearRegression()
model.fit(X_train, y_train)

joblib.dump(scaler_std, '../models/scaler_std.pkl')
bentoml.sklearn.save_model("linear_regression", model)

X_test[colonnes] = scaler_std.transform(X_test[colonnes])
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred)
print(f"R² score: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

