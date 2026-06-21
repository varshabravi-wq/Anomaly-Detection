import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import bcrypt
import numpy as np
from sklearn.linear_model import LinearRegression
import os

st.set_page_config(page_title="AI Anomaly Dashboard", layout="wide")

# ================== SESSION ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================== USERS ==================
users = {
    "admin": bcrypt.hashpw("1234".encode(), bcrypt.gensalt())
}

# ================== LOGIN ==================
def login():
    col1, col2 = st.columns([1,1])

    with col1:
        st.image("bg.jpeg", use_container_width=True)

    with col2:
        st.markdown("## 🔐 Secure Login")
        st.markdown("AI Trend Intelligence System")

        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")

        if st.button("Login", use_container_width=True):
            if username in users:
                if bcrypt.checkpw(password.encode(), users[username]):
                    st.session_state.logged_in = True
                    st.success("Login successful ✅")
                    st.rerun()
                else:
                    st.error("Incorrect password ❌")
            else:
                st.error("User not found ❌")

# ================== LOGOUT ==================
def logout():
    st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

# ================== AUTH ==================
if not st.session_state.logged_in:
    login()
    st.stop()

logout()

# ================== LOAD DATA ==================
with st.spinner("🔄 Processing data..."):
    df = pd.read_csv("../data/processed_trend_data.csv")

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

model = joblib.load("../models/isolation_forest.pkl")

features = df[['post_count', 'likes', 'shares', 'engagement_rate']]
df['anomaly'] = model.predict(features)
df['anomaly_label'] = df['anomaly'].apply(lambda x: "Anomaly" if x == -1 else "Normal")

# 👉 NEW: anomaly score
df['anomaly_score'] = model.decision_function(features)

# ================== SIDEBAR ==================
st.sidebar.title("📊 Dashboard")

platforms = st.sidebar.multiselect(
    "Platforms",
    df['platform'].unique(),
    default=df['platform'].unique()
)

filtered_df = df[df['platform'].isin(platforms)]

hashtag = st.sidebar.selectbox("Hashtag", filtered_df['hashtag'].unique())
filtered_df = filtered_df[filtered_df['hashtag'] == hashtag]

anomalies = filtered_df[filtered_df['anomaly_label'] == "Anomaly"]

# ================== TITLE ==================
st.title("🚀 AI Trend Intelligence Dashboard")
st.markdown("### Detect Viral Trends, Predict Growth & Identify Risks")

# ================== KPI ==================
col1, col2, col3 = st.columns(3)

col1.metric("Total Points", len(filtered_df))
col2.metric("🚨 Anomalies", len(anomalies))
col3.metric("📈 Avg Engagement", round(filtered_df['engagement_rate'].mean(),2))

# ================== ALERT ==================
if len(anomalies) > 0:
    st.error("🚨 High Risk Trend Detected")
    st.toast("⚠️ Live anomaly detected!")
else:
    st.success("✅ Stable Trend")

# ================== 🔥 ADVANCED KPIs ==================
st.subheader("📊 Advanced Insights")

colA, colB = st.columns(2)

trend_volatility = filtered_df['post_count'].std()
colA.metric("🔥 Trend Volatility", round(trend_volatility, 2))

if len(anomalies) > 5:
    colB.error("🔴 HIGH RISK")
elif len(anomalies) > 2:
    colB.warning("🟠 MEDIUM RISK")
else:
    colB.success("🟢 LOW RISK")

# AI Insight
if len(anomalies) > 0:
    st.info("💡 Insight: Sudden spikes suggest viral or coordinated activity.")
else:
    st.success("💡 Insight: Trend behavior is stable and organic.")

# ================== TABS ==================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Trends",
    "🚨 Anomalies",
    "📊 Insights",
    "🔮 Prediction"
])

# ================== TAB 1 ==================
with tab1:
    st.subheader("📈 Trend Visualization")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['post_count'],
        mode='lines',
        name='Trend',
        line=dict(color='cyan', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=anomalies['date'],
        y=anomalies['post_count'],
        mode='markers',
        name='Anomalies',
        marker=dict(color='red', size=12)
    ))

    fig.update_layout(template="plotly_dark", hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

# ================== TAB 2 ==================
with tab2:
    st.subheader("🚨 Detected Anomalies")

    def explain(row):
        if row['engagement_rate'] > 0.8:
            return "🔥 Viral engagement detected"
        elif row['post_count'] > filtered_df['post_count'].mean()*2:
            return "📈 Sudden spike detected"
        return "Normal"

    anomalies = anomalies.copy()
    anomalies['reason'] = anomalies.apply(explain, axis=1)

    st.dataframe(anomalies, use_container_width=True)

    st.download_button(
        "⬇ Download Anomalies",
        anomalies.to_csv(index=False),
        file_name="anomalies.csv"
    )

# ================== TAB 3 ==================
with tab3:
    st.subheader("📊 Deep Insights")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(filtered_df, x="likes", y="shares", color="anomaly_label")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(filtered_df, x="engagement_rate")
        st.plotly_chart(fig, use_container_width=True)

    # Platform comparison
    st.subheader("🌍 Platform Comparison")
    fig = px.bar(filtered_df, x="platform", y="post_count", color="platform")
    st.plotly_chart(fig, use_container_width=True)

    # Anomaly score
    st.subheader("📉 Anomaly Score")
    fig = px.line(filtered_df, x="date", y="anomaly_score")
    st.plotly_chart(fig, use_container_width=True)

# ================== TAB 4 ==================
with tab4:
    st.subheader("🔮 Future Trend Prediction")

    if len(filtered_df) > 5:
        X = np.arange(len(filtered_df)).reshape(-1,1)
        y = filtered_df['post_count']

        lr = LinearRegression().fit(X, y)

        future_X = np.arange(len(filtered_df), len(filtered_df)+5).reshape(-1,1)
        predictions = lr.predict(future_X)

        future_dates = pd.date_range(
            start=filtered_df['date'].iloc[-1],
            periods=6,
            freq='D'
        )[1:]

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['post_count'], name="Actual"))
        fig.add_trace(go.Scatter(x=future_dates, y=predictions, name="Prediction", line=dict(dash='dash')))

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

# ================== 📁 DATA EXPLORER ==================
st.subheader("📁 Data Explorer")

files = os.listdir("../data")
selected_file = st.selectbox("Select Data File", files)

col1, col2 = st.columns(2)

with col1:
    if st.button("📂 Open File"):
        df_view = pd.read_csv(f"../data/{selected_file}")
        st.dataframe(df_view, use_container_width=True)

with col2:
    if st.button("⬇ Download File"):
        df_download = pd.read_csv(f"../data/{selected_file}")
        st.download_button(
            "Download CSV",
            df_download.to_csv(index=False),
            file_name=selected_file
        )

# ================== RAW ==================
with st.expander("📂 View Filtered Data"):
    st.dataframe(filtered_df)

st.download_button(
    "⬇ Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_data.csv"
)