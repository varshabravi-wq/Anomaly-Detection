import time
import pandas as pd
import joblib

# 1. Load your pre-trained model safely
try:
    model = joblib.load('models/isolation_forest.pkl')
    print("✅ Successfully loaded anomaly detection model.")
    expected_features = model.feature_names_in_.tolist()
    print(f"📋 Model expects these features in order: {expected_features}")
except FileNotFoundError:
    print("❌ Error: models/isolation_forest.pkl not found. Run train_model.py first!")
    exit()
except AttributeError:
    expected_features = ['post_count', 'likes', 'shares', 'engagement_rate']

# 2. Memory-efficient data generator (Simulates live stream)
def log_streamer(file_path):
    """Reads a CSV file line by line to mimic live production data."""
    print(f"📡 Opening live stream from {file_path}...")
    try:
        for chunk in pd.read_csv(file_path, chunksize=1):
            time.sleep(0.5)  # Pause to simulate real-time traffic
            yield chunk
    except FileNotFoundError:
        print(f"❌ Error: {file_path} not found.")
        return

# 3. Process the live incoming stream
def run_live_detection():
    data_source = "data/raw_trend_data.csv" 
    stream = log_streamer(data_source)
    
    print("\n🚀 Starting Anomaly Detection Stream Tracker...")
    print("-" * 75)
    print(f"{'TIMESTAMP':<20} | {'LIKES':<10} | {'SHARES/MENTIONS':<17} | {'STATUS':<10}")
    print("-" * 75)
    
    for row in stream:
        timestamp = row['timestamp'].values[0] if 'timestamp' in row.columns else "Live Entry"
        
        # --- SAFE TYPE CASTING POOL ---
        pool = {}
        pool['likes'] = float(row['likes_count'].values[0]) if 'likes_count' in row.columns else 0.0
        pool['post_count'] = float(row['comments_count'].values[0]) if 'comments_count' in row.columns else 1.0
        
        # Force 'shares' to count strings instead of passing text to the model
        if 'mentions' in row.columns:
            val = row['mentions'].values[0]
            if pd.isna(val) or str(val).strip().lower() == 'none' or str(val).strip() == '':
                pool['shares'] = 0.0
            elif isinstance(val, (int, float)):
                pool['shares'] = float(val)
            else:
                # Count items separated by commas to get a clean mathematical float
                pool['shares'] = float(len([item for item in str(val).split(',') if item.strip()]))
        else:
            pool['shares'] = 0.0
        
        # Calculate or default engagement_rate safely as a pure float
        if 'engagement_rate' in row.columns:
            pool['engagement_rate'] = float(row['engagement_rate'].values[0])
        elif 'impressions' in row.columns and float(row['impressions'].values[0]) > 0:
            pool['engagement_rate'] = float((pool['likes'] + pool['post_count']) / row['impressions'].values[0])
        else:
            pool['engagement_rate'] = 0.05
            
        # Build the final DataFrame using the exact feature pool keys
        features = pd.DataFrame([{feat: pool.get(feat, 0.0) for feat in expected_features}])
        
        # Double-check: ensure everything going into the model is strictly numeric float
        features = features.astype(float)
        
        # Predict: Anomaly = -1, Normal = 1
        prediction = model.predict(features)[0]
        status = "🚨 ANOMALY" if prediction == -1 else "✅ NORMAL"
            
        print(f"{str(timestamp):<20} | {pool['likes']:<10.0f} | {pool['shares']:<17.0f} | {status:<10}")

if __name__ == "__main__":
    run_live_detection()