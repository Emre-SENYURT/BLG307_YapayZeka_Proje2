import streamlit as st
import pandas as pd
import time
from streamlit_folium import st_folium # Harita için gerekli

# Kendi modüllerimiz
from data.coordinates import sehir_koordinatlari
from core.distance_matrix import mesafe_matrisi_olustur
from core.aco_algo import run_aco
from visual.plotting import harita_ciz, grafik_ciz

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Uşak Arıza Rota Optimizasyonu",
    page_icon="⚡",
    layout="wide"
)

# --- BAŞLIK VE AÇIKLAMA ---
st.title("⚡ Uşak Elektrik Arıza Müdahale Rotası")
st.markdown("""
**Proje Konusu:** Uşak ilindeki 15 farklı mahallede oluşan elektrik arızalarına müdahale etmek için
tek bir teknik ekibin izlemesi gereken **en kısa rotanın** Karınca Kolonisi Algoritması (ACO) ile bulunması.
* **Yöntem:** Google Maps API (Gerçek Sürüş Mesafesi) + ACO
""")

# --- HAFIZA AYARI (SESSION STATE) ---
# Sayfa yenilense bile hesaplama yapıldığını unutma
if 'hesaplandi' not in st.session_state:
    st.session_state.hesaplandi = False

# --- YAN MENÜ (PARAMETRELER) ---
st.sidebar.header("🛠️ Algoritma Ayarları")

karinca_sayisi = st.sidebar.slider("🐜 Karınca Sayısı", 5, 50, 20)
iterasyon_sayisi = st.sidebar.slider("🔄 İterasyon Sayısı", 10, 100, 30)
alpha = st.sidebar.slider("Feromon Önemi (Alpha)", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Mesafe Önemi (Beta)", 0.1, 5.0, 2.0)
buharlasma = st.sidebar.slider("Buharlaşma Oranı", 0.0, 1.0, 0.5)

# Butona basılınca hafızayı 'True' yap
if st.sidebar.button("🚀 ROTAYI HESAPLA", type="primary"):
    st.session_state.hesaplandi = True

# --- ANA EKRAN DÜZENİ ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📍 Arıza Noktaları (Mahalleler)")
    df = pd.DataFrame.from_dict(sehir_koordinatlari, orient='index', columns=['Enlem', 'Boylam'])
    st.dataframe(df, height=400)

with col2:
    st.subheader("🗺️ Sonuç ve Harita")
    
    # Butona basılmışsa (veya hafızada varsa) çalıştır
    if st.session_state.hesaplandi:
        # 1. Mesafe Matrisini Oluştur
        with st.status("Veriler işleniyor...", expanded=True) as status:
            mesafe_matrisi, isimler = mesafe_matrisi_olustur(sehir_koordinatlari)
            status.write("✅ Mesafe matrisi hazır.")
            
            # 2. Algoritmayı Çalıştır
            st.write("🐜 Karıncalar en kısa yolu arıyor...")
            progress_bar = st.progress(0)
            start_time = time.time()
            
            en_iyi_yol_idx, en_kisa_mesafe, iterasyon_verileri = run_aco(
                mesafe_matrisi, 
                karinca_sayisi, 
                iterasyon_sayisi, 
                alpha, 
                beta, 
                buharlasma,
                progress_bar
            )
            
            end_time = time.time()
            status.update(label="İşlem Tamamlandı!", state="complete", expanded=False)
        
        # --- SONUÇLARI GÖSTER ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Toplam Mesafe", f"{en_kisa_mesafe:.2f} km")
        c2.metric("Süre", f"{end_time - start_time:.2f} saniye")
        c3.metric("İyileştirme Oranı", f"%{((iterasyon_verileri[0]-en_kisa_mesafe)/iterasyon_verileri[0])*100:.1f}")

        # En iyi rotayı isim olarak yazdır
        rota_isimleri = [isimler[i] for i in en_iyi_yol_idx]
        st.success(f"**Önerilen Rota:** {' ➝ '.join(rota_isimleri)}")

        # Harita ve Grafikleri Çiz
        tab1, tab2 = st.tabs(["Harita Gösterimi (Folium)", "Yakınsama Grafiği"])
        
        with tab1:
            # Haritayı çizdir
            harita = harita_ciz(en_iyi_yol_idx, sehir_koordinatlari, isimler)
            # Folium haritasını Streamlit içinde göster
            st_folium(harita, width=700, height=500, returned_objects=[])
        
        with tab2:
            fig_graph = grafik_ciz(iterasyon_verileri)
            st.pyplot(fig_graph)

    else:
        st.info("Algoritmayı başlatmak için sol taraftaki 'ROTAYI HESAPLA' butonuna basın.")