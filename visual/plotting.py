import folium
from streamlit_folium import st_folium

def harita_ciz(yol, koordinatlar, isimler):
    """En kısa rotayı Gerçek Harita (Folium) üzerinde çizer."""
    
    # 1. Haritanın merkezini bul (Ortalama Enlem/Boylam)
    lats = [koordinatlar[isim][0] for isim in isimler]
    lons = [koordinatlar[isim][1] for isim in isimler]
    merkez_lat = sum(lats) / len(lats)
    merkez_lon = sum(lons) / len(lons)

    # 2. Haritayı oluştur (Uşak Merkezli)
    m = folium.Map(location=[merkez_lat, merkez_lon], zoom_start=14)

    # 3. Noktaları (Marker) ekle
    for i, isim in enumerate(isimler):
        coord = koordinatlar[isim]
        # Başlangıç noktası farklı renk olsun
        if i == 0: 
            icon = folium.Icon(color="green", icon="home", prefix='fa')
        else:
            icon = folium.Icon(color="red", icon="map-marker", prefix='fa')
            
        folium.Marker(
            location=coord,
            popup=isim,
            tooltip=isim,
            icon=icon
        ).add_to(m)

    # 4. Rotayı Çiz (Çizgi Çek)
    rota_coords = []
    for idx in yol:
        isim = isimler[idx]
        rota_coords.append(koordinatlar[isim])
    
    # Çizgiyi haritaya ekle
    folium.PolyLine(
        rota_coords,
        color="blue",
        weight=3,
        opacity=0.8
    ).add_to(m)

    return m

# Grafik çizim fonksiyonu aynı kalabilir (Matplotlib ile devam)
import matplotlib.pyplot as plt
def grafik_ciz(iterasyon_verileri):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(iterasyon_verileri, color='purple', linewidth=2, marker='o', markersize=4)
    ax.set_title("Optimizasyon Süreci (Yakınsama Grafiği)", fontsize=14)
    ax.set_xlabel("İterasyon Sayısı")
    ax.set_ylabel("Toplam Mesafe (km)")
    ax.grid(True)
    return fig