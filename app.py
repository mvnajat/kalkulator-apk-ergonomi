import streamlit as st
import pandas as pd
import math
import io
import altair as alt

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="IE Toolkit: Waktu Kerja & Ergonomi",
    page_icon="⚙️",
    layout="wide"
)
# =====================================================================
# SIDEBAR (IDENTITAS & PANDUAN)
# =====================================================================
with st.sidebar:
    # 1. Logo atau Identitas Kampus/Kelas
    st.image("https://www.figma.com/community/file/1193446104276170734/ui-mobile-app-ecampus-pelita-bangsa", width=80) # Contoh ikon industri, bisa diganti URL logo kampus
    st.markdown("### 🎓 Teknik Industri")
    st.markdown("**Universitas Pelita Bangsa**")
    st.markdown("Kelas: **J253B**")
    
    st.divider()
    
    # 2. Informasi Pembuat
    st.markdown("#### 👨‍💻 Dibuat Oleh: Munajat")
    st.markdown("Mahasiswa Teknik Industri")
    st.markdown("*Kolaborator:* Web Praktikum APK & Ergonomi")
    
    st.divider()
    
    # 3. Panduan Singkat Penggunaan Web
    st.markdown("#### 📖 Panduan Singkat:")
    st.markdown(
        """
        1. **Tab 1 (Waktu Baku):** Masukkan data waktu (detik) dipisahkan koma, sesuaikan Westinghouse, lalu lihat grafik & unduh laporan Excel.
        2. **Tab 2 (RULA):** Pilih posisi postur tubuh sesuai kondisi nyata untuk melihat skor risiko *Action Level*.
        3. **Tab 3 (REBA):** Lakukan evaluasi seluruh tubuh secara komprehensif.
        """
    )
    
    st.divider()
    st.caption("© 2026 - IE Toolkit Project")
    
# =====================================================================
# MATRIKS LOOKUP TABLE RESMI RULA & REBA
# =====================================================================

# --- 1. MATRIKS RULA (McAtamney & Corlett, 1993) ---
# RULA Tabel A: [Upper Arm 1-6][Lower Arm 1-3][Wrist 1-4][Wrist Twist 1-2]
RULA_TABLE_A = [
    # Upper Arm = 1
    [[[1, 2], [2, 2], [2, 3], [3, 3]], [[2, 2], [2, 2], [3, 3], [3, 3]], [[2, 3], [3, 3], [3, 3], [4, 4]]],
    # Upper Arm = 2
    [[[2, 3], [3, 3], [3, 4], [4, 4]], [[3, 3], [3, 3], [3, 4], [4, 4]], [[3, 4], [4, 4], [4, 4], [5, 5]]],
    # Upper Arm = 3
    [[[3, 3], [4, 4], [4, 4], [5, 5]], [[3, 4], [4, 4], [4, 4], [5, 5]], [[4, 4], [4, 4], [4, 5], [5, 5]]],
    # Upper Arm = 4
    [[[4, 4], [4, 4], [4, 5], [5, 5]], [[4, 4], [4, 4], [4, 5], [5, 5]], [[4, 4], [4, 5], [5, 5], [6, 6]]],
    # Upper Arm = 5
    [[[5, 5], [5, 5], [5, 6], [6, 7]], [[5, 6], [6, 6], [6, 7], [7, 7]], [[6, 6], [6, 7], [7, 7], [7, 8]]],
    # Upper Arm = 6
    [[[7, 7], [7, 7], [7, 8], [8, 9]], [[8, 8], [8, 8], [8, 9], [9, 9]], [[9, 9], [9, 9], [9, 9], [9, 9]]]
]

# RULA Tabel B: [Neck 1-6][Trunk 1-6][Legs 1-2]
RULA_TABLE_B = [
    [[1, 3], [2, 3], [3, 4], [5, 5], [6, 6], [7, 7]], # Neck = 1
    [[2, 3], [2, 3], [4, 5], [5, 5], [6, 7], [7, 7]], # Neck = 2
    [[3, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 7]], # Neck = 3
    [[5, 5], [5, 6], [6, 7], [7, 7], [7, 7], [8, 8]], # Neck = 4
    [[7, 7], [7, 7], [7, 8], [8, 8], [8, 8], [8, 8]], # Neck = 5
    [[8, 8], [8, 8], [8, 8], [8, 9], [9, 9], [9, 9]]  # Neck = 6
]

# RULA Tabel C: [Score C (1..8+)][Score D (1..7+)]
RULA_TABLE_C = [
    [1, 2, 3, 3, 4, 5, 5], # Score C = 1
    [2, 2, 3, 4, 4, 5, 5], # Score C = 2
    [3, 3, 3, 4, 4, 5, 6], # Score C = 3
    [3, 3, 3, 4, 5, 6, 6], # Score C = 4
    [4, 4, 4, 5, 6, 7, 7], # Score C = 5
    [4, 4, 5, 6, 6, 7, 7], # Score C = 6
    [5, 5, 6, 6, 7, 7, 7], # Score C = 7
    [5, 5, 6, 7, 7, 7, 7]  # Score C >= 8
]

# --- 2. MATRIKS REBA (Hignett & McAtamney, 2000) ---
# REBA Tabel A: [Trunk 1-5][Neck 1-3][Legs 1-4]
REBA_TABLE_A = [
    [[1, 2, 3, 4], [1, 2, 3, 4], [3, 3, 5, 6]], # Trunk = 1
    [[2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]], # Trunk = 2
    [[2, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8]], # Trunk = 3
    [[3, 5, 6, 7], [5, 6, 7, 8], [6, 7, 8, 9]], # Trunk = 4
    [[4, 6, 7, 8], [6, 7, 8, 9], [7, 8, 9, 9]]  # Trunk = 5
]

# REBA Tabel B: [Upper Arm 1-6][Lower Arm 1-2][Wrist 1-3]
REBA_TABLE_B = [
    [[1, 2, 2], [1, 2, 3]], # Upper Arm = 1
    [[1, 2, 3], [2, 3, 4]], # Upper Arm = 2
    [[3, 4, 5], [4, 5, 5]], # Upper Arm = 3
    [[4, 5, 5], [5, 6, 7]], # Upper Arm = 4
    [[6, 7, 8], [7, 8, 8]], # Upper Arm = 5
    [[7, 8, 8], [8, 9, 9]]  # Upper Arm = 6
]

# REBA Tabel C: [Score A (1..12)][Score B (1..12)]
REBA_TABLE_C = [
    [1, 1, 1, 2, 3, 3, 4, 5, 6, 7, 7, 7],     # Score A = 1
    [1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8],     # Score A = 2
    [2, 3, 3, 3, 4, 5, 6, 7, 7, 8, 8, 8],     # Score A = 3
    [3, 4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9],     # Score A = 4
    [4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9, 9],     # Score A = 5
    [6, 6, 6, 7, 8, 8, 9, 9, 10, 10, 10, 10], # Score A = 6
    [7, 7, 7, 8, 9, 9, 9, 10, 10, 11, 11, 11],# Score A = 7
    [8, 8, 8, 9, 10, 10, 10, 10, 10, 11, 11, 11], # Score A = 8
    [9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12],# Score A = 9
    [10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 12], # Score A = 10
    [11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12], # Score A = 11
    [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]  # Score A = 12
]


# =====================================================================
# HEADER & NAVIGASI TAB
# =====================================================================
st.title("⚙️ Kalkulator Pengukuran Waktu Kerja & Ergonomi")
st.caption("Aplikasi Web Teknik Industri — Analisis Perancangan Kerja (APK) & Ergonomi")

tab1, tab2, tab3 = st.tabs([
    "⏱️ 1. Kalkulator Waktu Baku & Uji Data",
    "🧍 2. Skoring RULA (Matriks Lengkap)",
    "🏃 3. Skoring REBA (Matriks Lengkap)"
])


# =====================================================================
# TAB 1: KALKULATOR WAKTU KERJA & UJI DATA
# =====================================================================
with tab1:
    st.subheader("Perhitungan Waktu Baku, Uji Keseragaman, & Uji Kecukupan Data")
    
    col_input, col_hasil = st.columns([1.1, 1.3])
    
    with col_input:
        st.markdown("#### A. Data Waktu Pengamatan")
        data_raw = st.text_area(
            "Masukkan data waktu pengamatan (detik), pisahkan dengan koma:",
            value="12.5, 13.0, 12.8, 12.4, 15.8, 12.7, 12.9, 12.5, 12.6, 13.0, 12.7, 12.8",
            help="Contoh di atas memiliki 1 data ekstrem (15.8) untuk menguji fitur outlier."
        )
        
        st.markdown("#### B. Parameter Uji Statistik")
        u1, u2 = st.columns(2)
        with u1:
            konf_dict = {"99% (k = 3)": 3.0, "95% (k = 2)": 2.0, "68% (k = 1)": 1.0}
            k_label = st.selectbox("Tingkat Kepercayaan", list(konf_dict.keys()), index=1)
            k_val = konf_dict[k_label]
            
            pembagi_std = st.radio(
                "Rumus Standar Deviasi",
                ["Sampel (N - 1)", "Populasi (N)"],
                horizontal=True
            )
        with u2:
            s_pct = st.number_input("Derajat Ketelitian / s (%)", min_value=1.0, max_value=25.0, value=5.0, step=0.5)
            s_val = s_pct / 100.0
            auto_revisi = st.checkbox("Otomatis buang data di luar BKA/BKB (Revisi Data)")

        st.markdown("#### C. Faktor Penyesuaian (*Westinghouse*)")
        skill_dict = {
            "Superskill (A1) [+0.15]": 0.15, "Superskill (A2) [+0.13]": 0.13,
            "Excellent (B1) [+0.11]": 0.11, "Excellent (B2) [+0.08]": 0.08,
            "Good (C1) [+0.06]": 0.06, "Good (C2) [+0.03]": 0.03,
            "Average (D) [0.00]": 0.00,
            "Fair (E1) [-0.05]": -0.05, "Fair (E2) [-0.10]": -0.10,
            "Poor (F1) [-0.16]": -0.16, "Poor (F2) [-0.22]": -0.22
        }
        effort_dict = {
            "Excessive (A1) [+0.13]": 0.13, "Excessive (A2) [+0.12]": 0.12,
            "Excellent (B1) [+0.10]": 0.10, "Excellent (B2) [+0.08]": 0.08,
            "Good (C1) [+0.05]": 0.05, "Good (C2) [+0.02]": 0.02,
            "Average (D) [0.00]": 0.00,
            "Fair (E1) [-0.04]": -0.04, "Fair (E2) [-0.08]": -0.08,
            "Poor (F1) [-0.12]": -0.12, "Poor (F2) [-0.17]": -0.17
        }
        cond_dict = {
            "Ideal (A) [+0.06]": 0.06, "Excellent (B) [+0.04]": 0.04,
            "Good (C) [+0.02]": 0.02, "Average (D) [0.00]": 0.00,
            "Fair (E) [-0.03]": -0.03, "Poor (F) [-0.07]": -0.07
        }
        cons_dict = {
            "Perfect (A) [+0.04]": 0.04, "Excellent (B) [+0.03]": 0.03,
            "Good (C) [+0.01]": 0.01, "Average (D) [0.00]": 0.00,
            "Fair (E) [-0.02]": -0.02, "Poor (F) [-0.04]": -0.04
        }

        c1, c2 = st.columns(2)
        with c1:
            s_w = skill_dict[st.selectbox("Keterampilan (Skill)", list(skill_dict.keys()), index=6)]
            e_w = effort_dict[st.selectbox("Usaha (Effort)", list(effort_dict.keys()), index=6)]
        with c2:
            cd_w = cond_dict[st.selectbox("Kondisi Kerja (Condition)", list(cond_dict.keys()), index=3)]
            cs_w = cons_dict[st.selectbox("Konsistensi (Consistency)", list(cons_dict.keys()), index=3)]

        st.markdown("#### D. Kelonggaran (*Allowance*)")
        allowance_pct = st.slider("Total Persentase Allowance (%)", min_value=0.0, max_value=50.0, value=15.0, step=0.5)

    with col_hasil:
        try:
            data_awal = [float(x.strip()) for x in data_raw.split(",") if x.strip() != ""]
            
            if len(data_awal) < 2:
                st.warning("Masukkan minimal 2 data pengamatan untuk menghitung standar deviasi.")
            else:
                def hitung_statistik(data_arr):
                    n = len(data_arr)
                    rata2 = sum(data_arr) / n
                    pembagi = (n - 1) if pembagi_std == "Sampel (N - 1)" else n
                    variansi = sum((x - rata2) ** 2 for x in data_arr) / pembagi
                    std_dev = math.sqrt(variansi)
                    bka_val = rata2 + (k_val * std_dev)
                    bkb_val = rata2 - (k_val * std_dev)
                    
                    sum_x = sum(data_arr)
                    sum_x2 = sum(x ** 2 for x in data_arr)
                    pembilang_n = (k_val / s_val) * math.sqrt(max((n * sum_x2) - (sum_x ** 2), 0))
                    n_aksen = (pembilang_n / sum_x) ** 2 if sum_x > 0 else 0
                    return n, rata2, std_dev, bka_val, bkb_val, n_aksen

                n_data, ws, std_dev, bka, bkb, n_aksen = hitung_statistik(data_awal)
                outliers = [x for x in data_awal if x > bka or x < bkb]
                data_aktif = data_awal

                if auto_revisi and len(outliers) > 0:
                    data_aktif = [x for x in data_awal if bkb <= x <= bka]
                    if len(data_aktif) >= 2:
                        st.info(f"🔄 **Revisi Data Aktif:** Menghapus {len(outliers)} data ekstrem ({outliers}) dan menghitung ulang batas kontrol.")
                        n_data, ws, std_dev, bka, bkb, n_aksen = hitung_statistik(data_aktif)
                        outliers = [x for x in data_aktif if x > bka or x < bkb]

                p = 1.0 + (s_w + e_w + cd_w + cs_w)
                wn = ws * p
                wb = wn * (1 + (allowance_pct / 100))
                output_std = 3600 / wb if wb > 0 else 0

                st.markdown("#### 📊 1. Hasil Waktu Kerja & Output Standar")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Waktu Siklus (Ws)", f"{ws:.2f} dtk")
                m2.metric("Waktu Normal (Wn)", f"{wn:.2f} dtk", f"p = {p:.2f}")
                m3.metric("Waktu Baku (Wb)", f"{wb:.2f} dtk", f"Allow. {allowance_pct}%")
                m4.metric("Output Standar", f"{output_std:.1f} unit/jam")

                st.markdown("#### 📈 2. Hasil Uji Keseragaman & Kecukupan Data")
                u_col1, u_col2 = st.columns(2)
                status_seragam = "SERAGAM" if len(outliers) == 0 else "TIDAK SERAGAM"
                status_cukup = "CUKUP (N' <= N)" if n_aksen <= n_data else "BELUM CUKUP (N' > N)"

                with u_col1:
                    if len(outliers) == 0:
                        st.success(f"**Uji Keseragaman: SERAGAM**\n\nSeluruh {n_data} data berada di dalam rentang BKB ({bkb:.2f}) dan BKA ({bka:.2f}).")
                    else:
                        st.error(f"**Uji Keseragaman: TIDAK SERAGAM**\n\nTerdapat {len(outliers)} data di luar batas kontrol: **{outliers}**.")
                
                with u_col2:
                    if n_aksen <= n_data:
                        st.success(f"**Uji Kecukupan: DATA CUKUP (N' ≤ N)**\n\nNilai **N' = {n_aksen:.2f}** (dibulatkan {math.ceil(n_aksen)} data), sedangkan **N = {n_data}**.")
                    else:
                        kurang = math.ceil(n_aksen) - n_data
                        st.warning(f"**Uji Kecukupan: BELUM CUKUP (N' > N)**\n\nNilai **N' = {n_aksen:.2f}** (N = {n_data}). Kurang minimal **{kurang} data** lagi.")

                # --- GRAFIK PETA KONTROL ---
                st.markdown("#### 📉 3. Grafik Peta Kontrol Keseragaman Data")
                df_chart = pd.DataFrame({
                    "Pengamatan Ke": list(range(1, n_data + 1)),
                    "Waktu (detik)": data_aktif,
                    "Kuadrat Waktu (x²)": [round(x ** 2, 4) for x in data_aktif],
                    "BKA": [round(bka, 3)] * n_data,
                    "Rata-rata (Ws)": [round(ws, 3)] * n_data,
                    "BKB": [round(bkb, 3)] * n_data,
                    "Status": ["Normal" if bkb <= x <= bka else "Outlier (Di Luar Batas)" for x in data_aktif]
                })

                base = alt.Chart(df_chart).encode(x=alt.X("Pengamatan Ke:O", title="Pengamatan Ke-"))
                line_data = base.mark_line(color="#3b82f6", strokeWidth=2).encode(
                    y=alt.Y("Waktu (detik):Q", scale=alt.Scale(zero=False), title="Waktu (Detik)")
                )
                points_data = base.mark_circle(size=90).encode(
                    y="Waktu (detik):Q",
                    color=alt.Color("Status:N", scale=alt.Scale(domain=["Normal", "Outlier (Di Luar Batas)"], range=["#2563eb", "#dc2626"])),
                    tooltip=["Pengamatan Ke", "Waktu (detik)", "Status", "BKA", "Rata-rata (Ws)", "BKB"]
                )
                rule_bka = alt.Chart(df_chart).mark_rule(color="#dc2626", strokeDash=[6, 4], size=2).encode(y="mean(BKA):Q")
                rule_ws = alt.Chart(df_chart).mark_rule(color="#16a34a", strokeDash=[3, 3], size=2).encode(y="mean(Rata-rata (Ws)):Q")
                rule_bkb = alt.Chart(df_chart).mark_rule(color="#dc2626", strokeDash=[6, 4], size=2).encode(y="mean(BKB):Q")

                chart_final = (line_data + points_data + rule_bka + rule_ws + rule_bkb).properties(height=280)
                st.altair_chart(chart_final, use_container_width=True)

                # --- TABEL RINGKASAN & UNDUH EXCEL ---
                df_summary = pd.DataFrame({
                    "Parameter": [
                        "Jumlah Pengamatan Aktif (N)",
                        "Total Waktu Pengamatan (Σx)",
                        "Total Kuadrat Waktu (Σx²)",
                        "Waktu Siklus Rata-rata (Ws)",
                        "Standar Deviasi (σ)",
                        "Batas Kontrol Atas (BKA)",
                        "Batas Kontrol Bawah (BKB)",
                        "Status Uji Keseragaman",
                        "Jumlah Pengamatan Minimum (N')",
                        "Status Uji Kecukupan",
                        "Faktor Penyesuaian Westinghouse (p)",
                        "Waktu Normal (Wn)",
                        "Allowance (%)",
                        "Waktu Baku (Wb)",
                        "Kapasitas Output Standar (unit/jam)"
                    ],
                    "Nilai": [
                        n_data,
                        round(sum(data_aktif), 4),
                        round(sum(x**2 for x in data_aktif), 4),
                        round(ws, 4),
                        round(std_dev, 4),
                        round(bka, 4),
                        round(bkb, 4),
                        status_seragam,
                        round(n_aksen, 4),
                        status_cukup,
                        round(p, 2),
                        round(wn, 4),
                        allowance_pct,
                        round(wb, 4),
                        round(output_std, 2)
                    ]
                })

                # Membuat file Excel di dalam memori (BytesIO)
                excel_buffer_1 = io.BytesIO()
                with pd.ExcelWriter(excel_buffer_1, engine="openpyxl") as writer:
                    df_summary.to_excel(writer, sheet_name="Ringkasan_Perhitungan", index=False)
                    df_chart.to_excel(writer, sheet_name="Data_Pengamatan", index=False)

                st.download_button(
                    label="📥 Unduh Laporan Waktu Baku & Uji Data (.xlsx)",
                    data=excel_buffer_1.getvalue(),
                    file_name="Laporan_Waktu_Baku_APK.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

                with st.expander("📋 Lihat Tabel Ringkasan Parameter Lengkap"):
                    st.dataframe(df_summary, use_container_width=True, hide_index=True)

        except ValueError:
            st.error("Pastikan data pengamatan hanya berisi angka dan dipisahkan dengan tanda koma (,).")


# =====================================================================
# TAB 2: SKORING POSTUR KERJA RULA (MATRIKS TABEL A, B, C RESMI)
# =====================================================================
with tab2:
    st.subheader("Penilaian Postur Kerja RULA (Rapid Upper Limb Assessment)")
    st.caption("Menggunakan Matriks Lookup Tabel A, Tabel B, dan Tabel C Resmi (McAtamney & Corlett, 1993)")

    col_ra, col_rb, col_rres = st.columns([1.1, 1.1, 1])

    with col_ra:
        st.markdown("#### Grup A: Lengan & Pergelangan Tangan")
        ua_base = st.selectbox("1. Posisi Lengan Atas (Upper Arm)", [
            (1, "1 : Sudut -20° s/d 20° (Netral)"),
            (2, "2 : Ekstensi >20° atau Fleksi 20°-45°"),
            (3, "3 : Fleksi 45°-90°"),
            (4, "4 : Fleksi >90°")
        ], format_func=lambda x: x[1], key="rula_ua")[0]
        ua_sh = 1 if st.checkbox("Bahu terangkat (+1)", key="rula_ua_sh") else 0
        ua_ab = 1 if st.checkbox("Lengan atas abduksi / menjauhi tubuh (+1)", key="rula_ua_ab") else 0
        ua_sp = -1 if st.checkbox("Lengan ditopang / bersandar (-1)", key="rula_ua_sp") else 0
        rula_ua = max(1, min(ua_base + ua_sh + ua_ab + ua_sp, 6))

        la_base = st.selectbox("2. Posisi Lengan Bawah (Lower Arm)", [
            (1, "1 : Fleksi 60° - 100°"),
            (2, "2 : Fleksi <60° atau >100°")
        ], format_func=lambda x: x[1], key="rula_la")[0]
        la_mid = 1 if st.checkbox("Bekerja melewati garis tengah / keluar sisi tubuh (+1)", key="rula_la_mid") else 0
        rula_la = max(1, min(la_base + la_mid, 3))

        wr_base = st.selectbox("3. Posisi Pergelangan Tangan (Wrist)", [
            (1, "1 : Posisi Netral (0°)"),
            (2, "2 : Fleksi / Ekstensi 0° - 15°"),
            (3, "3 : Fleksi / Ekstensi > 15°")
        ], format_func=lambda x: x[1], key="rula_wr")[0]
        wr_dev = 1 if st.checkbox("Deviasi radial / ulnar (belok ke samping) (+1)", key="rula_wr_dev") else 0
        rula_wr = max(1, min(wr_base + wr_dev, 4))

        rula_wt = st.selectbox("4. Putaran Pergelangan (Wrist Twist)", [
            (1, "1 : Berputar di rentang tengah (Mid-range)"),
            (2, "2 : Berputar di dekat / batas akhir (End-range)")
        ], format_func=lambda x: x[1], key="rula_wt")[0]

        st.markdown("**Otot & Beban Grup A:**")
        rula_muscle_a = 1 if st.checkbox("Postur Grup A statis >1 menit atau repetitif >4x/menit (+1)", key="rula_ma") else 0
        rula_force_a = st.selectbox("Beban / Gaya Grup A (Force/Load)", [
            (0, "0 : Beban < 2 kg (intermiten)"),
            (1, "1 : Beban 2 - 10 kg (intermiten)"),
            (2, "2 : Beban 2 - 10 kg (statis / repetitif)"),
            (3, "3 : Beban > 10 kg atau beban kejut")
        ], format_func=lambda x: x[1], key="rula_fa")[0]

    with col_rb:
        st.markdown("#### Grup B: Leher, Punggung & Kaki")
        nk_base = st.selectbox("5. Posisi Leher (Neck)", [
            (1, "1 : Fleksi 0° - 10°"),
            (2, "2 : Fleksi 10° - 20°"),
            (3, "3 : Fleksi > 20°"),
            (4, "4 : Ekstensi (Mendongak)")
        ], format_func=lambda x: x[1], key="rula_nk")[0]
        nk_tw = 1 if st.checkbox("Leher terputar / menoleh (+1)", key="rula_nk_tw") else 0
        nk_sb = 1 if st.checkbox("Leher miring ke samping (+1)", key="rula_nk_sb") else 0
        rula_nk = max(1, min(nk_base + nk_tw + nk_sb, 6))

        tr_base = st.selectbox("6. Posisi Punggung (Trunk)", [
            (1, "1 : Duduk tegak & ditopang baik (0°)"),
            (2, "2 : Fleksi (Membungkuk) 0° - 20°"),
            (3, "3 : Fleksi 20° - 60°"),
            (4, "4 : Fleksi > 60°")
        ], format_func=lambda x: x[1], key="rula_tr")[0]
        tr_tw = 1 if st.checkbox("Punggung terputar (+1)", key="rula_tr_tw") else 0
        tr_sb = 1 if st.checkbox("Punggung miring ke samping (+1)", key="rula_tr_sb") else 0
        rula_tr = max(1, min(tr_base + tr_tw + tr_sb, 6))

        rula_legs = st.selectbox("7. Posisi Kaki (Legs)", [
            (1, "1 : Kaki tertopang seimbang / duduk"),
            (2, "2 : Kaki tidak tertopang / tumpuan 1 kaki")
        ], format_func=lambda x: x[1], key="rula_legs")[0]

        st.markdown("**Otot & Beban Grup B:**")
        rula_muscle_b = 1 if st.checkbox("Postur Grup B statis >1 menit atau repetitif >4x/menit (+1)", key="rula_mb") else 0
        rula_force_b = st.selectbox("Beban / Gaya Grup B (Force/Load)", [
            (0, "0 : Beban < 2 kg (intermiten)"),
            (1, "1 : Beban 2 - 10 kg (intermiten)"),
            (2, "2 : Beban 2 - 10 kg (statis / repetitif)"),
            (3, "3 : Beban > 10 kg atau beban kejut")
        ], format_func=lambda x: x[1], key="rula_fb")[0]

    with col_rres:
        st.markdown("#### 🎯 Hasil Matriks RULA")
        # Lookup Tabel A, B, C
        score_table_a = RULA_TABLE_A[rula_ua - 1][rula_la - 1][rula_wr - 1][rula_wt - 1]
        score_c = score_table_a + rula_muscle_a + rula_force_a

        score_table_b = RULA_TABLE_B[rula_nk - 1][rula_tr - 1][rula_legs - 1]
        score_d = score_table_b + rula_muscle_b + rula_force_b

        idx_c = min(score_c, 8) - 1
        idx_d = min(score_d, 7) - 1
        rula_grand = RULA_TABLE_C[idx_c][idx_d]

        r1, r2, r3 = st.columns(3)
        r1.metric("Skor C (Grup A)", score_c, f"Tabel A = {score_table_a}")
        r2.metric("Skor D (Grup B)", score_d, f"Tabel B = {score_table_b}")
        r3.metric("Skor Akhir RULA", f"{rula_grand} / 7")

        if rula_grand in [1, 2]:
            rula_kat = "Action Level 1 (Risiko Rendah - Dapat Diterima)"
            st.success(f"**{rula_kat}**\n\nPostur kerja dapat diterima jika tidak dipertahankan dalam waktu lama.")
        elif rula_grand in [3, 4]:
            rula_kat = "Action Level 2 (Risiko Sedang - Perlu Investigasi)"
            st.warning(f"**{rula_kat}**\n\nDiperlukan investigasi lebih lanjut dan perubahan posisi kerja mungkin dibutuhkan.")
        elif rula_grand in [5, 6]:
            rula_kat = "Action Level 3 (Risiko Tinggi - Segera Perbaiki)"
            st.error(f"**{rula_kat}**\n\nInvestigasi dan perubahan desain stasiun kerja harus segera dilakukan dalam waktu dekat.")
        else:
            rula_kat = "Action Level 4 (Risiko Sangat Tinggi - Perbaiki Sekarang!)"
            st.error(f"**{rula_kat}**\n\nKondisi kritis! Perbaikan postur dan stasiun kerja harus dilakukan SEKARANG JUGA.")

        df_rula = pd.DataFrame({
            "Komponen Evaluasi RULA": [
                "Skor Lengan Atas (Upper Arm)", "Skor Lengan Bawah (Lower Arm)",
                "Skor Pergelangan Tangan (Wrist)", "Skor Putaran Pergelangan (Wrist Twist)",
                "Skor Postur Tabel A", "Skor Otot & Beban Grup A", "Skor C (Total Grup A)",
                "Skor Leher (Neck)", "Skor Punggung (Trunk)", "Skor Kaki (Legs)",
                "Skor Postur Tabel B", "Skor Otot & Beban Grup B", "Skor D (Total Grup B)",
                "Skor Akhir RULA (Tabel C)", "Kategori Action Level"
            ],
            "Nilai / Skor": [
                rula_ua, rula_la, rula_wr, rula_wt,
                score_table_a, (rula_muscle_a + rula_force_a), score_c,
                rula_nk, rula_tr, rula_legs,
                score_table_b, (rula_muscle_b + rula_force_b), score_d,
                rula_grand, rula_kat
            ]
        })
        st.dataframe(df_rula, use_container_width=True, hide_index=True, height=280)

        excel_buffer_rula = io.BytesIO()
        with pd.ExcelWriter(excel_buffer_rula, engine="openpyxl") as writer:
            df_rula.to_excel(writer, sheet_name="Hasil_Skoring_RULA", index=False)

        st.download_button(
            label="📥 Unduh Laporan RULA (.xlsx)",
            data=excel_buffer_rula.getvalue(),
            file_name="Laporan_Ergonomi_RULA.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


# =====================================================================
# TAB 3: SKORING POSTUR KERJA REBA (MATRIKS TABEL A, B, C RESMI)
# =====================================================================
with tab3:
    st.subheader("Penilaian Postur Kerja REBA (Rapid Entire Body Assessment)")
    st.caption("Menggunakan Matriks Lookup Tabel A, Tabel B, dan Tabel C Resmi (Hignett & McAtamney, 2000)")

    col_eba, col_ebb, col_ebres = st.columns([1.1, 1.1, 1])

    with col_eba:
        st.markdown("#### Grup A: Punggung, Leher & Kaki")
        eb_tr_base = st.selectbox("1. Posisi Punggung (Trunk)", [
            (1, "1 : Tegak / Netral (0°)"),
            (2, "2 : Fleksi / Ekstensi 0° - 20°"),
            (3, "3 : Fleksi 20° - 60° atau Ekstensi > 20°"),
            (4, "4 : Fleksi > 60°")
        ], format_func=lambda x: x[1], key="reba_tr")[0]
        eb_tr_mod = 1 if st.checkbox("Punggung terputar atau miring ke samping (+1)", key="reba_tr_mod") else 0
        reba_tr = max(1, min(eb_tr_base + eb_tr_mod, 5))

        eb_nk_base = st.selectbox("2. Posisi Leher (Neck)", [
            (1, "1 : Fleksi 0° - 20°"),
            (2, "2 : Fleksi > 20° atau Ekstensi (Mendongak)")
        ], format_func=lambda x: x[1], key="reba_nk")[0]
        eb_nk_mod = 1 if st.checkbox("Leher terputar atau miring ke samping (+1)", key="reba_nk_mod") else 0
        reba_nk = max(1, min(eb_nk_base + eb_nk_mod, 3))

        eb_leg_base = st.selectbox("3. Posisi Kaki (Legs)", [
            (1, "1 : Tumpuan 2 kaki seimbang / jalan / duduk"),
            (2, "2 : Tumpuan 1 kaki / postur tidak stabil")
        ], format_func=lambda x: x[1], key="reba_leg")[0]
        eb_leg_knee = st.selectbox("Tekukan Lutut (Knee Flexion)", [
            (0, "0 : Lutut lurus (< 30°)"),
            (1, "+1 : Lutut menekuk 30° - 60°"),
            (2, "+2 : Lutut menekuk > 60°")
        ], format_func=lambda x: x[1], key="reba_knee")[0]
        reba_legs = max(1, min(eb_leg_base + eb_leg_knee, 4))

        reba_load = st.selectbox("4. Beban / Gaya (Load / Force)", [
            (0, "0 : Beban < 5 kg"),
            (1, "1 : Beban 5 - 10 kg"),
            (2, "2 : Beban > 10 kg")
        ], format_func=lambda x: x[1], key="reba_load")[0]
        reba_shock = 1 if st.checkbox("Ada beban kejut / pengerahan gaya mendadak (+1)", key="reba_shock") else 0
        reba_total_load = reba_load + reba_shock

    with col_ebb:
        st.markdown("#### Grup B: Lengan Atas, Lengan Bawah & Pergelangan")
        eb_ua_base = st.selectbox("5. Posisi Lengan Atas (Upper Arm)", [
            (1, "1 : Fleksi / Ekstensi -20° s/d 20°"),
            (2, "2 : Ekstensi >20° atau Fleksi 20° - 45°"),
            (3, "3 : Fleksi 45° - 90°"),
            (4, "4 : Fleksi > 90°")
        ], format_func=lambda x: x[1], key="reba_ua")[0]
        eb_ua_sh = 1 if st.checkbox("Bahu terangkat (+1)", key="reba_ua_sh") else 0
        eb_ua_ab = 1 if st.checkbox("Lengan abduksi / diputar (+1)", key="reba_ua_ab") else 0
        eb_ua_sp = -1 if st.checkbox("Lengan ditopang / bersandar (-1)", key="reba_ua_sp") else 0
        reba_ua = max(1, min(eb_ua_base + eb_ua_sh + eb_ua_ab + eb_ua_sp, 6))

        reba_la = st.selectbox("6. Posisi Lengan Bawah (Lower Arm)", [
            (1, "1 : Fleksi 60° - 100°"),
            (2, "2 : Fleksi < 60° atau > 100°")
        ], format_func=lambda x: x[1], key="reba_la")[0]

        eb_wr_base = st.selectbox("7. Posisi Pergelangan Tangan (Wrist)", [
            (1, "1 : Fleksi / Ekstensi 0° - 15°"),
            (2, "2 : Fleksi / Ekstensi > 15°")
        ], format_func=lambda x: x[1], key="reba_wr")[0]
        eb_wr_mod = 1 if st.checkbox("Pergelangan tangan terputar / deviasi (+1)", key="reba_wr_mod") else 0
        reba_wr = max(1, min(eb_wr_base + eb_wr_mod, 3))

        reba_coupling = st.selectbox("8. Pegangan (Coupling Score)", [
            (0, "0 : Good (Pegangan pas dan kuat)"),
            (1, "1 : Fair (Pegangan masih bisa diterima)"),
            (2, "2 : Poor (Pegangan sulit / tidak nyaman)"),
            (3, "3 : Unacceptable (Tidak ada pegangan / tidak aman)")
        ], format_func=lambda x: x[1], key="reba_coup")[0]

        st.markdown("**9. Skor Aktivitas (Activity Score):**")
        act1 = 1 if st.checkbox("1 atau lebih bagian tubuh statis > 1 menit (+1)", key="reba_act1") else 0
        act2 = 1 if st.checkbox("Gerakan berulang > 4x per menit (+1)", key="reba_act2") else 0
        act3 = 1 if st.checkbox("Perubahan postur besar secara cepat / tidak stabil (+1)", key="reba_act3") else 0
        reba_activity = act1 + act2 + act3

    with col_ebres:
        st.markdown("#### 🎯 Hasil Matriks REBA")
        # Lookup Tabel A, B, C REBA
        eb_table_a = REBA_TABLE_A[reba_tr - 1][reba_nk - 1][reba_legs - 1]
        reba_score_a = min(eb_table_a + reba_total_load, 12)

        eb_table_b = REBA_TABLE_B[reba_ua - 1][reba_la - 1][reba_wr - 1]
        reba_score_b = min(eb_table_b + reba_coupling, 12)

        reba_score_c = REBA_TABLE_C[reba_score_a - 1][reba_score_b - 1]
        reba_final = reba_score_c + reba_activity

        eb1, eb2, eb3 = st.columns(3)
        eb1.metric("Skor A (Grup A)", reba_score_a, f"Tabel A = {eb_table_a}")
        eb2.metric("Skor B (Grup B)", reba_score_b, f"Tabel B = {eb_table_b}")
        eb3.metric("Skor Akhir REBA", f"{reba_final} / 15", f"Tabel C = {reba_score_c}")

        if reba_final == 1:
            reba_kat = "Action Level 0 (Risiko Sangat Rendah - Tidak Perlu Tindakan)"
            st.success(f"**{reba_kat}**\n\nPostur kerja aman dan tidak memerlukan tindakan perbaikan.")
        elif reba_final in [2, 3]:
            reba_kat = "Action Level 1 (Risiko Rendah - Mungkin Perlu Perbaikan)"
            st.info(f"**{reba_kat}**\n\nRisiko rendah, perubahan postur mungkin diperlukan ke depannya.")
        elif reba_final in [4, 5, 6, 7]:
            reba_kat = "Action Level 2 (Risiko Sedang - Perlu Tindakan)"
            st.warning(f"**{reba_kat}**\n\nPerlu investigasi lebih lanjut dan tindakan perbaikan postur kerja.")
        elif reba_final in [8, 9, 10]:
            reba_kat = "Action Level 3 (Risiko Tinggi - Segera Perbaiki)"
            st.error(f"**{reba_kat}**\n\nRisiko cedera tinggi! Perlu tindakan perbaikan sesegera mungkin.")
        else:
            reba_kat = "Action Level 4 (Risiko Sangat Tinggi - Perbaiki Saat Ini Juga!)"
            st.error(f"**{reba_kat}**\n\nKondisi berbahaya! Tindakan perbaikan mutlak dilakukan SAAT INI JUGA.")

        df_reba = pd.DataFrame({
            "Komponen Evaluasi REBA": [
                "Skor Punggung (Trunk)", "Skor Leher (Neck)", "Skor Kaki (Legs)",
                "Skor Postur Tabel A", "Skor Beban / Force", "Skor A (Total Grup A)",
                "Skor Lengan Atas (Upper Arm)", "Skor Lengan Bawah (Lower Arm)", "Skor Pergelangan (Wrist)",
                "Skor Postur Tabel B", "Skor Pegangan (Coupling)", "Skor B (Total Grup B)",
                "Skor Tabel C", "Skor Aktivitas (Activity)", "Skor Akhir REBA", "Kategori Action Level"
            ],
            "Nilai / Skor": [
                reba_tr, reba_nk, reba_legs,
                eb_table_a, reba_total_load, reba_score_a,
                reba_ua, reba_la, reba_wr,
                eb_table_b, reba_coupling, reba_score_b,
                reba_score_c, reba_activity, reba_final, reba_kat
            ]
        })
        st.dataframe(df_reba, use_container_width=True, hide_index=True, height=280)

        excel_buffer_reba = io.BytesIO()
        with pd.ExcelWriter(excel_buffer_reba, engine="openpyxl") as writer:
            df_reba.to_excel(writer, sheet_name="Hasil_Skoring_REBA", index=False)

        st.download_button(
            label="📥 Unduh Laporan REBA (.xlsx)",
            data=excel_buffer_reba.getvalue(),
            file_name="Laporan_Ergonomi_REBA.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        