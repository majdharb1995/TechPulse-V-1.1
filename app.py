import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import feedparser
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="TechPulse | Majd Harb", page_icon="⚡", layout="wide")

# --- إدارة اللغات ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'

def toggle_lang():
    st.session_state.lang = 'AR' if st.session_state.lang == 'EN' else 'EN'

texts = {
    'EN': {
        'dir': 'ltr', 'font': 'Plus Jakarta Sans', 'title': 'TechPulse', 'subtitle': 'OS',
        'lead': 'Lead Engineer', 'filters': 'FILTERS', 'cat_label': 'Select Category',
        'src_label': 'Select Source', 'all_src': 'All Sources', 'all_cats': 'All Categories',
        'status': 'STATUS: ACTIVE', 'm1': 'Total Records', 'm2': 'Top Source', 'm3': 'Latency',
        'tab1': '📋 LATEST FEED', 'tab2': '📊 ANALYTICS', 'waiting': 'Fetching fresh data...',
        'stored': 'Stored at', 'view': 'VIEW DATA ↗', 'footer': 'DESIGNED & ENGINEERED BY MAJD HARB © 2026'
    },
    'AR': {
        'dir': 'rtl', 'font': 'Cairo', 'title': 'نبض التقنية', 'subtitle': 'نظام',
        'lead': 'المهندس المسؤول', 'filters': 'تصفية البيانات', 'cat_label': 'اختر الفئة',
        'src_label': 'اختر المصدر', 'all_src': 'جميع المصادر', 'all_cats': 'جميع الفئات',
        'status': 'الحالة: نشط', 'm1': 'إجمالي السجلات', 'm2': 'المصدر الرئيسي', 'm3': 'زمن الاستجابة',
        'tab1': '📋 آخر الأخبار', 'tab2': '📊 التحليلات', 'waiting': 'جاري جلب بيانات جديدة...',
        'stored': 'تاريخ التخزين', 'view': 'عرض البيانات ↗', 'footer': 'تصميم وهندسة مجد حرب © 2026'
    }
}

L = texts[st.session_state.lang]

# 2. Ultra-Modern Professional CSS
style = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Cairo:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {{ font-family: '{L['font']}', sans-serif; direction: {L['dir']}; text-align: {'right' if L['dir'] == 'rtl' else 'left'}; }}
    .stApp {{ background: radial-gradient(circle at top right, #f8fafc, #eff6ff); background-attachment: fixed; }}
    [data-testid="stSidebar"] {{ direction: {L['dir']}; }}
    .glass-card {{
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(15px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.05);
    }}
    .article-card {{
        background: white; padding: 20px; border-radius: 15px; border: 1px solid #f1f5f9;
        margin-bottom: 15px; transition: 0.3s;
    }}
    .article-card:hover {{ transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.03); }}
    .tag {{ font-size: 9px; font-weight: 800; padding: 4px 10px; border-radius: 20px; background: #eff6ff; color: #2563eb; margin-inline-end: 5px; }}
    .src-tag {{ background: #f1f5f9; color: #475569; }}
    .m-value {{ font-size: 2.1rem !important; font-weight: 800 !important; color: #0f172a; line-height: 1.2; }}
    .m-title {{ font-size: 11px !important; text-transform: uppercase; color: #64748b; font-weight: 800; }}
</style>
"""
st.markdown(style, unsafe_allow_html=True)

# 3. Data Engine (Multi-Source Scraper)
@st.cache_data(ttl=86400)
def load_and_sync_db():
    SOURCES = {
        'TechCrunch': 'https://techcrunch.com/feed/',
        'The Verge': 'https://www.theverge.com/rss/index.xml',
        'Wired': 'https://www.wired.com/feed/rss'
    }
    
    all_articles = []
    for name, url in SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                all_articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'category': entry.get('category', 'Technology'),
                    'source': name,
                    'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M')
                })
        except: continue
    
    df_new = pd.DataFrame(all_articles)
    
    if not df_new.empty:
        conn = sqlite3.connect('tech_news.db')
        df_new.to_sql('articles', conn, if_exists='replace', index=False)
        conn.close()
        return df_new
    else:
        try:
            conn = sqlite3.connect('tech_news.db')
            df = pd.read_sql("SELECT * FROM articles ORDER BY fetched_at DESC", conn)
            conn.close()
            return df
        except:
            return pd.DataFrame(columns=['category', 'title', 'link', 'fetched_at', 'source'])

df = load_and_sync_db()

# 4. Header & Language Toggle
header_col1, header_col2 = st.columns([4, 1])
with header_col2:
    st.button("🌐 English" if st.session_state.lang == 'AR' else "🌐 العربية", on_click=toggle_lang)

st.markdown(f"""
    <div class="glass-card" style="display: flex; justify-content: space-between; align-items: center; padding: 20px 40px;">
        <div><h1 style="margin:0; font-size: 26px; font-weight: 800;">⚡ {L['title']} <span style="font-weight:300; color:#64748b;">{L['subtitle']}</span></h1></div>
        <div style="text-align: {'left' if L['dir'] == 'rtl' else 'right'};">
            <p style="margin:0; font-size: 11px; font-weight: 800; color: #2563eb;">{L['lead']}</p>
            <h2 style="margin:0; font-size: 18px; font-weight: 700;">MAJD HARB</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. Layout
col_side, col_main = st.columns([1, 4], gap="medium")

with col_side:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:14px; font-weight:800; margin-bottom:15px;'>{L['filters']}</p>", unsafe_allow_html=True)
    
    cat = st.selectbox(L['cat_label'], [L['all_cats']] + sorted(list(df['category'].unique())))
    src_filter = st.selectbox(L['src_label'], [L['all_src']] + sorted(list(df['source'].unique())))
    
    st.markdown("<hr style='opacity:0.1'>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:10px; color:#94a3b8;'>SYSTEM V2.2.0<br>{L['status']}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    # Dynamic Metrics
    top_source = df['source'].mode()[0] if not df.empty else "N/A"
    m1, m2, m3 = st.columns(3)
    for m, title, val in zip([m1, m2, m3], [L['m1'], L['m2'], L['m3']], [len(df), top_source, "18ms"]):
        with m:
            st.markdown(f'<div class="glass-card" style="padding: 15px 20px;"><p class="m-title">{title}</p><p class="m-value">{val}</p></div>', unsafe_allow_html=True)

    t1, t2 = st.tabs([L['tab1'], L['tab2']])
    
    with t1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        f_df = df.copy()
        if cat != L['all_cats']: f_df = f_df[f_df['category'] == cat]
        if src_filter != L['all_src']: f_df = f_df[f_df['source'] == src_filter]

        if f_df.empty:
            st.info(L['waiting'])
        else:
            for _, row in f_df.head(20).iterrows():
                st.markdown(f"""
                    <div class="article-card">
                        <div style="margin-bottom:8px;">
                            <span class="tag">{row['category']}</span>
                            <span class="tag src-tag">📍 {row['source']}</span>
                        </div>
                        <h3 class="art-title" style="margin: 10px 0;">{row['title']}</h3>
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-direction: {'row-reverse' if L['dir'] == 'rtl' else 'row'};">
                            <span class="art-meta" style="font-size:11px; color:#94a3b8;">{L['stored']}: {row['fetched_at']}</span>
                            <a href="{row['link']}" target="_blank" style="font-size: 12px; color: #2563eb; font-weight: 700; text-decoration: none;">{L['view']}</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if not df.empty:
            fig = px.pie(df, names='source', hole=0.7, color_discrete_sequence=px.colors.qualitative.Safe)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(family=L['font']))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div style="text-align: center; padding: 40px; opacity: 0.4; font-size: 11px; font-weight: 600; letter-spacing: 2px;">{L['footer']}</div>', unsafe_allow_html=True)