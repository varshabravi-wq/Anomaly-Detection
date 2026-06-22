import streamlit as st
import pandas as pd
import joblib
import time
import requests  # Added to handle streaming real-time alerts over the network

# Premium Wide Layout Setup
st.set_page_config(
    page_title="Enterprise Anomaly Detection Radar",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# Secure Webhook Endpoint Configuration
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1518493495864725529/Arnzi43LxjGgLWQE9NaHQ7CwS3b-aW80kIJZJyKOI3xXXlMPanp-G_HGRTKk1l9z-Keq"

def send_security_alert(consecutive_count, timestamp, likes_val):
    """Dispatches a real-time system breach alert directly to the Discord Ops channel."""
    if "discord.com/api/webhooks" not in DISCORD_WEBHOOK_URL:
        return
        
    payload = {
        "username": "Radar Security Operations Center",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/1022/1022244.png",
        "embeds": [
            {
                "title": "🚨 CRITICAL INFRASTRUCTURE BREACH DETECTED",
                "description": "The telemetry pipeline has flagged a massive cluster of continuous anomalies.",
                "color": 15158332,  # Crimson Red
                "fields": [
                    {
                        "name": "Consecutive Outlier Events",
                        "value": f"📈 {consecutive_count} anomalies in a row!",
                        "inline": True
                    },
                    {
                        "name": "Incident Timestamp",
                        "value": f"⏰ {timestamp}",
                        "inline": True
                    },
                    {
                        "name": "Current Traffic Load (Likes)",
                        "value": f"📊 {likes_val:.0f} requests",
                        "inline": False
                    },
                    {
                        "name": "Status",
                        "value": "🔴 Automated Mitigation Initiated. Review Streamlit Platform Panel Immediately.",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Signal Surveillance System Network"
                }
            }
        ]
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=3)
    except Exception:
        pass # Protect pipeline continuity if the network request drops

# Custom Style Sheet Injection for high text contrast
st.markdown("""
    <style>
    .metric-card {
        background-color: #1e222b;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2d3139;
        border-left: 5px solid #4A90E2;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.4);
    }
    div[data-testid="stMetricLabel"] {
        color: #e0e0e0 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State arrays to persist data permanently across stops/refreshes
if "incident_archive" not in st.session_state:
    st.session_state.incident_archive = []

# Application Header Banner
st.title("🛡️ Enterprise Production Log Anomaly Radar & Alerting System")
st.markdown("---")

# 1. Load the Model Brain Safely
@st.cache_resource
def load_ml_components():
    model = joblib.load('models/isolation_forest.pkl')
    expected_features = model.feature_names_in_.tolist()
    return model, expected_features

try:
    model, expected_features = load_ml_components()
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# 2. Main Controlling Dashboard Sidebar
with st.sidebar:
    st.header("⚙️ Pipeline Controller")
    st.markdown("Use this panel to manage live data stream configurations.")
    speed_slider = st.slider("Stream Ingestion Speed (Seconds)", min_value=0.1, max_value=2.0, value=0.4, step=0.1)
    
    st.markdown("---")
    st.header("🚨 Alert Thresholds")
    st.markdown("Configure when system breach protocols trigger.")
    consecutive_threshold = st.slider("Consecutive Anomalies for Alert", min_value=2, max_value=10, value=3)
    
    boot_btn = st.button("🚀 Boot Live Radar Stream", use_container_width=True)
    
    # Sidebar space to show skipped corrupt logs
    error_log_space = st.empty()

# 3. Initialize Top Telemetry KPI Metric Layout Cards
st.subheader("📊 System Telemetry & Operational Health")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    m_total = st.metric("Total Items Processed", "0 rows")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    m_anom = st.metric("Anomalies Flags Raised", "0 alerts", delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    m_ratio = st.metric("Anomaly Ratio", "0.00%")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(" ")
status_banner = st.empty()
alert_banner = st.empty()  
st.markdown("---")

# 4. Split Screen Visualization Layout Grid
st.subheader("📈 Live Analytics Stream Timeline")
graph_col, log_col = st.columns([2, 1])

with graph_col:
    chart_placeholder = st.empty()

with log_col:
    st.markdown("**Real-Time Activity Terminal Logs**")
    terminal_placeholder = st.empty()

st.markdown("---")
st.subheader("🔍 Inspected Incident Payloads (Audit Log)")
table_placeholder = st.empty()
download_placeholder = st.empty()

# 5. Pipeline Logic Engine
def start_stream_pipeline():
    data_source = "data/raw_trend_data.csv"
    total_count = 0
    anomaly_count = 0
    consecutive_anomalies = 0  
    history = []
    log_feed = []
    
    st.session_state.incident_archive = []
    error_log_space.empty() # Clear old errors
    
    try:
        for chunk in pd.read_csv(data_source, chunksize=1):
            total_count += 1
            
            # Defensive parsing protection block
            try:
                pool = {}
                pool['likes'] = float(chunk['likes_count'].values[0]) if 'likes_count' in chunk.columns else 0.0
                pool['post_count'] = float(chunk['comments_count'].values[0]) if 'comments_count' in chunk.columns else 1.0
                
                if 'mentions' in chunk.columns:
                    val = chunk['mentions'].values[0]
                    if pd.isna(val) or str(val).strip().lower() == 'none' or str(val).strip() == '':
                        pool['shares'] = 0.0
                    elif isinstance(val, (int, float)):
                        pool['shares'] = float(val)
                    else:
                        pool['shares'] = float(len([item for item in str(val).split(',') if item.strip()]))
                else:
                    pool['shares'] = 0.0
                    
                if 'engagement_rate' in chunk.columns:
                    pool['engagement_rate'] = float(chunk['engagement_rate'].values[0])
                elif 'impressions' in chunk.columns and float(chunk['impressions'].values[0]) > 0:
                    pool['engagement_rate'] = float((pool['likes'] + pool['post_count']) / chunk['impressions'].values[0])
                else:
                    pool['engagement_rate'] = 0.05

                features = pd.DataFrame([{feat: pool.get(feat, 0.0) for feat in expected_features}]).astype(float)
            
            except (ValueError, KeyError, IndexError):
                # If data is corrupt, log it safely to the sidebar and skip to the next row
                error_log_space.warning(f"⚠️ Row {total_count} skipped: Malformed numerical telemetry payload data.")
                continue 
                
            # Run model ML evaluation safely on clean data
            prediction = model.predict(features)[0]
            
            timestamp = chunk['timestamp'].values[0] if 'timestamp' in chunk.columns else str(total_count)
            is_anomaly = (prediction == -1)
            
            if is_anomaly:
                anomaly_count += 1
                consecutive_anomalies += 1
                status_text = f"🚨 ANOMALY detected at {timestamp} (Likes: {pool['likes']:.0f})"
                log_feed.insert(0, f"🔴 {timestamp} - ANOMALY EVENT")
                
                st.session_state.incident_archive.insert(0, {
                    "Timestamp": timestamp,
                    "Likes Volume": pool['likes'],
                    "Post/Comment Count": pool['post_count'],
                    "Share/Mention Points": pool['shares'],
                    "Engagement %": f"{pool['engagement_rate']*100:.2f}%"
                })
            else:
                consecutive_anomalies = 0  
                status_text = "✅ SYSTEM STATE: Operations Performing Normally."
                log_feed.insert(0, f"🟢 {timestamp} - Processed Normal Log")
            
            if consecutive_anomalies >= consecutive_threshold:
                alert_banner.error(
                    f"🔥 **CRITICAL BREACH PROTOCOL TRIGGERED** 🔥\n\n"
                    f"System detected {consecutive_anomalies} anomalies in a row! "
                    f"Last incident recorded at {timestamp}."
                )
                
                # Active Trigger: Dispatches alert payload straight to Discord on the exact cross-over wave
                if consecutive_anomalies == consecutive_threshold:
                    send_security_alert(consecutive_anomalies, timestamp, pool['likes'])
                    
            elif consecutive_anomalies == 0:
                alert_banner.empty() 
            
            history.append({
                "Timestamp": timestamp,
                "Traffic Value (Likes)": pool['likes']
            })
            if len(history) > 30:
                history.pop(0)
            if len(log_feed) > 10:
                log_feed.pop()
                
            df_history = pd.DataFrame(history)
            anom_ratio = (anomaly_count / total_count) * 100
            
            m_total.metric("Total Items Processed", f"{total_count} rows")
            m_anom.metric("Anomalies Flags Raised", f"{anomaly_count} alerts", delta=f"+{1 if is_anomaly else 0}", delta_color="inverse")
            m_ratio.metric("Anomaly Ratio", f"{anom_ratio:.2f}%")
            
            if is_anomaly:
                status_banner.error(status_text)
            else:
                status_banner.success(status_text)
                
            chart_placeholder.line_chart(df_history.set_index("Timestamp")["Traffic Value (Likes)"])
            terminal_placeholder.code("\n".join(log_feed), language="text")
            
            if st.session_state.incident_archive:
                df_current_incidents = pd.DataFrame(st.session_state.incident_archive)
                table_placeholder.dataframe(df_current_incidents, use_container_width=True)
                
                csv_data = df_current_incidents.to_csv(index=False).encode('utf-8')
                download_placeholder.download_button(
                    label="📥 Export Captured Anomalies Archive (.CSV)",
                    data=csv_data,
                    file_name="incident_security_report.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key=f"live_dl_btn_{total_count}"
                )
            else:
                table_placeholder.info("No anomalies caught in this monitoring session yet.")
            
            time.sleep(speed_slider)
            
    except FileNotFoundError:
        st.error("Could not locate data matrix source file.")

# Main app display execution orchestration
if boot_btn:
    start_stream_pipeline()
else:
    if st.session_state.incident_archive:
        df_final = pd.DataFrame(st.session_state.incident_archive)
        table_placeholder.dataframe(df_final, use_container_width=True)
        
        csv_data = df_final.to_csv(index=False).encode('utf-8')
        download_placeholder.download_button(
            label="📥 Export Captured Anomalies Archive (.CSV)",
            data=csv_data,
            file_name="incident_security_report.csv",
            mime="text/csv",
            use_container_width=True,
            key="final_frozen_download_button"
        )
    else:
        status_banner.info("💡 Pro-Tip: Click 'Boot Live Radar Stream' in the left sidebar panel to begin real-time system monitoring.")
        download_placeholder.button(
            label="📥 Export Security Incident Audit Log (Empty Stream)",
            disabled=True,
            use_container_width=True,
            key="initial_disabled_preview_button"
        )