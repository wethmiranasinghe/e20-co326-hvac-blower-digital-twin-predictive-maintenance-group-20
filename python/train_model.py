import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

df = pd.read_csv("normal_fan_data.csv")

X = df[["current", "moving_avg"]]

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)

joblib.dump(model, "fan_anomaly_model.pkl")
print("Saved fan_anomaly_model.pkl")