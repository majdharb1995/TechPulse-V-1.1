import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import base64
import os

# 1. Page Configuration
st.set_page_config(page_title="TechPulse | Majd Harb", page_icon="⚡", layout="wide")

# 2. Professional UI & Light Glassmorphism CSS
glass_style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    /* خلفية التطبيق - تدرج فاتح وعصري */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        background-attachment: fixed;
    }

    /* الحاويات الزجاجية الفاتحة */
    .glass-box {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(12px) saturate(180%);
        -webkit-backdrop-filter: blur(12px) saturate(180%);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.7);
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }

    /* تحسين نصوص العناوين والفقرات */
    h1, h2, h3 {
        color: #0f172a !important;
        font-family: 'Inter', sans-serif;
    }
    
    p, span, label {
        color: #334155 !important;
        font-family: 'Inter', sans-serif;
    }

    /* القائمة الجانبية - فاتحة ومتناسقة */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 8px;
        border-radius: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #475569 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        background: rgba(255, 255, 255, 0.8) !important;
        border-radius: 12px;
    }

    /* الإحصائيات (Metrics) */
    .metric-title {
        color: #64748b !important;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #1e293b !important;
        font-weight: 900 !important;
        font-size: 3.2rem !important;
        line-height: 1;
    }

    /* تعديل عناصر المدخلات (Selectbox) */
    .stSelectbox label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
</style>
"""
st.markdown(glass_style, unsafe_allow_html=True)

# 3. Data Engine (نفس منطق الكود الخاص بك)
def load_db():
    try:
        conn = sqlite3.connect('tech_news.db')
        df = pd.read_sql("SELECT * FROM articles ORDER BY id DESC", conn)
        conn.close()
        required_columns = ['category', 'title', 'link', 'fetched_at']
        for col in required_columns:
            if col not in df.columns: df[col] = "General"
        return df
    except: return pd.DataFrame()

df = load_db()

# 4. Header Section - أكثر وضوحاً وحجماً
st.markdown(f"""
    <div class="glass-box">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin:0; font-size: 35px; font-weight: 900; letter-spacing: -1px;">⚡ TechPulse Pipeline</h1>
                <p style="margin:0; font-size: 18px; font-weight: 500; opacity: 0.8;">Data Engineering Portfolio</p>
            </div>
            <div style="text-align:right;">
                <h2 style="margin:0; color:#2563eb !important; font-size: 28px; font-weight: 900;">MAJD HARB</h2>
                <p style="margin:0; font-weight:700; font-size: 14px; color: #64748b;">Lead Architect & Designer</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. Sidebar
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:20px;'>🔍 Controls</h2>", unsafe_allow_html=True)
    if not df.empty:
        cat = st.selectbox("Category Filter", ["All"] + list(df['category'].unique()))
    st.markdown("---")
    st.markdown("<p style='font-size:14px; font-weight:600;'>System Status: <span style='color:#22c55e;'>● Active</span></p>", unsafe_allow_html=True)

# 6. Main Content
if not df.empty:
    # Metrics
    st.markdown('<div style="margin: 20px 0;">', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<p class="metric-title">Database Size</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value">{len(df)}</p>', unsafe_allow_html=True)
    with m2:
        st.markdown('<p class="metric-title">Primary Source</p>', unsafe_allow_html=True)
        st.markdown('<p class="metric-value" style="font-size:2rem !important;">TechCrunch</p>', unsafe_allow_html=True)
    with m3:
        st.markdown('<p class="metric-title">System Load</p>', unsafe_allow_html=True)
        st.markdown('<p class="metric-value" style="font-size:2rem !important; color:#22c55e !important;">Stable</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Dashboard Feed", "📊 Data Analytics"])
    
    with tab1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        display_df = df if cat == "All" else df[df['category'] == cat]
        for _, row in display_df.iterrows():
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.7); padding:25px; border-radius:20px; margin-bottom:18px; border: 1px solid rgba(0,0,0,0.05); transition: 0.3s;">
                    <span style="background:#2563eb; color:white; padding:5px 15px; border-radius:10px; font-size:12px; font-weight:800; text-transform: uppercase;">{row['category']}</span>
                    <h3 style="margin:15px 0 10px 0; color:#1e293b; font-weight: 800; font-size: 1.5rem;">{row['title']}</h3>
                    <p style="color:#64748b; font-size:13px; margin-bottom:15px;">Fetched on: {row['fetched_at']}</p>
                    <a href="{row['link']}" target="_blank" style="color:#2563eb; font-weight:700; text-decoration:none; font-size:16px; display: inline-flex; align-items: center;">Read Article <span style="margin-left:5px;">↗</span></a>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        fig = px.pie(df, names='category', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=16, color="#0f172a")
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("No data found in the database.")

# 7. Global Footer
st.markdown(f"""
    <div style="margin-top:50px; padding:40px; text-align:center; color: #64748b;">
        <p style="font-size: 16px; letter-spacing: 1px; font-weight:600;">© 2026 <b>MAJD HARB</b> | PIPELINE ARCHITECTURE</p>
    </div>
""", unsafe_allow_html=True)