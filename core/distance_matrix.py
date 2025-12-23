import numpy as np
import googlemaps
import streamlit as st
from math import radians, sin, cos, sqrt, atan2

def haversine(coord1, coord2):
    """Yedek Plan: Kuş Uçuşu Mesafe Hesaplama"""
    R = 6371  # Dünya yarıçapı (km)
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def mesafe_matrisi_olustur(koordinatlar):
    """
    Google Maps API varsa gerçek sürüş mesafesini, yoksa kuş uçuşunu hesaplar.
    """
    isimler = list(koordinatlar.keys())
    n = len(isimler)
    matris = np.zeros((n, n))
    
    # Streamlit secrets içinden API Key'i almaya çalış
    api_key = None
    gmaps = None
    
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
            gmaps = googlemaps.Client(key=api_key)
            # Bağlantı testi yapalım (Ufak bir hack)
            print("✅ API Key bulundu, Google Maps servisine bağlanılıyor...")
    except Exception as e:
        print(f"⚠️ API Key okunamadı: {e}")

    # İlerleme çubuğu (Terminalde görmek için)
    print("Mesafe matrisi hesaplanıyor...")

    for i in range(n):
        for j in range(n):
            if i == j:
                matris[i][j] = np.inf # Kendisine gitmesin
            else:
                coord_i = koordinatlar[isimler[i]]
                coord_j = koordinatlar[isimler[j]]
                
                basari = False
                if gmaps:
                    try:
                        # Google Maps'ten Sürüş Mesafesi İste
                        # origins ve destinations formatı: (enlem, boylam)
                        result = gmaps.distance_matrix(origins=coord_i, destinations=coord_j, mode="driving")
                        
                        if result['rows'][0]['elements'][0]['status'] == 'OK':
                            # Metreyi kilometreye çevir
                            mesafe_km = result['rows'][0]['elements'][0]['distance']['value'] / 1000.0
                            matris[i][j] = mesafe_km
                            basari = True
                    except Exception as e:
                        # Hata olursa (kota biterse vs) sessizce kuş uçuşuna geç
                        pass
                
                if not basari:
                    # API yoksa veya hata verdiyse Haversine kullan
                    matris[i][j] = haversine(coord_i, coord_j)
    
    print("✅ Mesafe matrisi hazır!")
    return matris, isimler

def hesapla_cekicilik(mesafe):
    cekicilik = np.zeros_like(mesafe)
    with np.errstate(divide='ignore'):
        cekicilik = 1 / mesafe
        cekicilik[mesafe == np.inf] = 0
    return cekicilik