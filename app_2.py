
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

h1 {
    color: #f59e0b;
}

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

.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #f59e0b;
    margin-top: 20px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ========================
# LOAD DATA
# ========================
uploaded_file = st.file_uploader("📂 Upload File Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    df = pd.read_excel("Restruk_Data.xlsx")

# ========================
# VALIDASI KOLOM
# ========================
required_columns = ['Tanggal', 'UNIT', 'ITEM', 'Nilai']

missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"Kolom berikut tidak ditemukan: {missing_cols}")
    st.stop()

# Pastikan nilai numerik untuk formatting dan perbandingan
if 'Nilai' in df.columns:
    df['Nilai'] = pd.to_numeric(df['Nilai'], errors='coerce')

# ========================
# TITLE
# ========================
st.title("🏭 DASHBOARD CONTROL MONITORING GELATIK MILL")

# ========================
# FILTER
# ========================
col1, col2 = st.columns(2)

bulan = col1.selectbox(
    "📅 Bulan",
    [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
)

# Ambil tanggal unik
list_tanggal = sorted(df['Tanggal'].dropna().unique())

tanggal = col2.selectbox("📅 Tanggal", list_tanggal)

# Filter data
filtered_df = df[df['Tanggal'] == tanggal]

st.markdown(f"### 📊 Data STORAGE Tanggal {tanggal} ({bulan})")

# ========================
# ITEM PERSEN
# ========================
percent_items = [
    "FFA",
    "MOIST",
    "DIRTY",
    "CPO_FFA",
    "CPO_MOIST",
    "CPO_DIRTY",
    "CPO_OER",
    "KERNEL_MOIST",
    "KERNEL_DIRTY",
    "KERNEL_KER"
]

# ========================
# BATAS ALERT
# ========================
alert_rules = {
    "FFA": 0.05,
    "CPO_FFA": 0.05,
    "DIRTY": 0.06,
    "MOIST": 0.07
}

# ========================
# CARD PER ITEM
# ========================
items = filtered_df['ITEM'].unique()

# Bagi menjadi 2 kolom dashboard
cols = st.columns(2)

for i, item in enumerate(items):

    item_df = filtered_df[filtered_df['ITEM'] == item]

    with cols[i % 2]:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            f'<div class="card-title">🏢 {item}</div>',
            unsafe_allow_html=True
        )

        param_cols = st.columns(len(item_df))

        for j, (_, row) in enumerate(item_df.iterrows()):

            nilai = row['Nilai']

            # ========================
            # FORMAT NILAI
            # ========================
            if item in percent_items:
                display_nilai = f"{nilai * 100:.2f}%"
            elif item in ["PH"]:
                display_nilai = f"{nilai:.2f}"
            else:
                display_nilai = f"{nilai:,.0f}"

            # ========================
            # WARNA ALERT
            # ========================
            color = "white"

            if item in alert_rules:
                if nilai > alert_rules[item]:
                    color = "#ef4444"  # merah
                else:
                    color = "#22c55e"  # hijau

            # ========================
            # CARD PARAMETER
            # ========================
            param_cols[j].markdown(f"""
                <div class="param-box">
                    <div class="param-label">{row['UNIT']}</div>
                    <div class="param-value" style="color:{color}">
                        {display_nilai}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ========================
# GRAFIK TREND ITEM
# ========================
st.markdown("---")
st.markdown("## 📈 Trend Monitoring Item")

selected_item = st.selectbox(
    "Pilih Item untuk Grafik Trend",
    sorted(df['ITEM'].unique())
)

trend_df = df[df['ITEM'] == selected_item]

fig, ax = plt.subplots(figsize=(12, 5))

for unit in trend_df['UNIT'].unique():

    unit_df = trend_df[trend_df['UNIT'] == unit]

    ax.plot(
        unit_df['Tanggal'],
        unit_df['Nilai'],
        marker='o',
        label=unit
    )

ax.set_title(f'Trend {selected_item}')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Nilai')
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ========================
# TABEL DATA
# ========================
st.markdown("---")
st.markdown("## 📋 Detail Data")

st.dataframe(filtered_df, use_container_width=True)


