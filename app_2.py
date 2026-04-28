import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="Dashboard Monitoring", layout="wide")

# ========================
# CSS CLEAN UI
# ========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #0e1117, #111827);
    color: #e5e7eb;
}
h1 { color: #f59e0b; }

.card {
    background: linear-gradient(145deg, #1b2430, #111827);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    margin-bottom: 20px;
    transition: 0.3s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.7);
}

.card-title {
    font-size: 20px;
    font-weight: 600;
    color: #fbbf24;
    margin-bottom: 15px;
}

.param-box {
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    background: #1f2937;
    margin: 5px;
}

.param-label {
    font-size: 13px;
    color: #9ca3af;
}

.param-value {
    font-size: 22px;
    font-weight: bold;
    color: #f9fafb;
}
</style>
""", unsafe_allow_html=True)

# ========================
# LOAD DATA
# ========================
uploaded_file = st.file_uploader("📂 Upload File Excel", type=["xlsx"])
df = pd.read_excel("Restruk_Data.xlsx")

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

tanggal = col2.selectbox("📅 Tanggal", sorted(df['Tanggal'].unique()))

filtered_df = df[df['Tanggal'] == tanggal]

st.markdown(f"### 📊 Data STORAGE Tanggal {tanggal} ({bulan})")
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
            nilai = row['Nilai']

            # FORMAT NILAI
            if item in ["FFA", "MOIST", "DIRTY"]:
                display_nilai = f"{nilai*100:.2f}%"
            else:
                display_nilai = f"{nilai:,.0f}"

            # WARNA ALERT
            color = "white"
            if item == "FFA" and nilai > 0.05:
                color = "red"

            param_cols[j].markdown(f"""
                <div class="param-box">
                    <div class="param-label">{row['UNIT']}</div>
                    <div class="param-value" style="color:{color}">
                        {display_nilai}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

