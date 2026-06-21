import pandas as pd
from anomaly_detector import train_model, detect_anomalies

def main():
    print("🚀 Starting Anomaly Detection System...")

    # Load data
    try:
        df = pd.read_csv("data/processed_trend_data.csv")
        print("✅ Data loaded!")
    except Exception as e:
        print("❌ Error:", e)
        return

    # Train model
    print("🧠 Training model...")
    train_model(df)

    # Detect anomalies
    print("🔍 Detecting anomalies...")
    result_df = detect_anomalies(df)

    # Show results
    print("\n📊 Sample Output:")
    print(result_df.head())

    # Save results
    result_df.to_csv("data/anomaly_output.csv", index=False)
    print("✅ Output saved!")

    # Count anomalies
    print(f"🚨 Total anomalies: {result_df['anomaly'].sum()}")

if __name__ == "__main__":
    main()