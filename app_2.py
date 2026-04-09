import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="DASHBOARD CONTROL MONITORING GELATIK MILL ", layout="wide")

# ========================
# CSS CLEAN UI
# ========================
st.markdown("""
<style>

/* Background utama */
.stApp {
    background: linear-gradient(145deg, #0e1117, #111827);
    color: #e5e7eb;
}

/* Judul utama */
h1 {
    color: #f59e0b;
}

/* Card container */
.card {
    background: linear-gradient(145deg, #1b2430, #111827);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 
        0 4px 20px rgba(0,0,0,0.5),
        inset 0 0 0.5px rgba(255,255,255,0.1);
    margin-bottom: 20px;
    transition: 0.3s ease;
}

/* Hover effect (biar hidup) */
.card:hover {
    transform: translateY(-3px);
    box-shadow: 
        0 8px 25px rgba(0,0,0,0.7),
        0 0 10px rgba(245,158,11,0.2);
}

/* Title item */
.card-title {
    font-size: 20px;
    font-weight: 600;
    color: #fbbf24;
    margin-bottom: 15px;
}

/* Parameter box */
.param-box {
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    background: linear-gradient(145deg, #1f2937, #111827);
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: inset 0 0 5px rgba(0,0,0,0.5);
    margin: 5px;
    transition: 0.2s;
}

/* Hover kecil */
.param-box:hover {
    transform: scale(1.03);
    box-shadow: 0 0 8px rgba(34,197,94,0.3);
}

/* Label parameter */
.param-label {
    font-size: 13px;
    color: #9ca3af;
    letter-spacing: 0.5px;
}

/* Nilai utama */
.param-value {
    font-size: 24px;
    font-weight: bold;
    color: #f9fafb;
}

/* Selectbox styling */
div[data-baseweb="select"] {
    background-color: #1f2937 !important;
    border-radius: 10px;
}

/* Scrollbar biar modern */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
# ========================
# LOAD DATA
# ========================
df = pd.read_csv("data_bersih.csv")

st.title("🏭 DASHBOARD CONTROL MONITORING GELATIK MILL")

# ========================
# FILTER
# ========================
col1, col2 = st.columns(2)

bulan = col1.selectbox(
    "📅 Bulan",
    ["Januari","Februari","Maret","April","Mei","Juni",
     "Juli","Agustus","September","Oktober","November","Desember"]
)

tanggal = col2.selectbox("📅 Tanggal", sorted(df['TANGGAL'].unique()))

filtered_df = df[df['TANGGAL'] == tanggal]

st.markdown(f"### 📊 Data Tanggal {tanggal} ({bulan})")

# ========================
# CARD PER ITEM
# ========================
items = filtered_df['ITEM'].unique()
cols = st.columns(2)

for i, item in enumerate(items):
    item_df = filtered_df[filtered_df['ITEM'] == item]

    with cols[i % 2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(f'<div class="card-title">🏢 {item}</div>', unsafe_allow_html=True)

        param_cols = st.columns(len(item_df))

        for j, (_, row) in enumerate(item_df.iterrows()):
            param_cols[j].markdown(f"""
                <div class="param-box">
                    <div class="param-label">{row['PARAMETER']}</div>
                    <div class="param-value">{row['NILAI']}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


