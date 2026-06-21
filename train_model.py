import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load processed data
df = pd.read_csv("data/processed_trend_data.csv")

# Features for anomaly detection
features = df[['post_count', 'likes', 'shares', 'comments', 'engagement_rate', 'z_score']]

# Train model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(features)

# Save model
joblib.dump(model, "models/isolation_forest.pkl")

print("✅ Model trained and saved!")