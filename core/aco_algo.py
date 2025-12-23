import numpy as np
import random
from core.distance_matrix import hesapla_cekicilik

def olasilik_hesapla(mevcut, ziyaret_edilmemisler, feromon, cekicilik, alpha, beta):
    """Karıncanın bir sonraki şehre gitme olasılığını hesaplar."""
    toplam = 0
    olasiliklar = {}
    
    for j in ziyaret_edilmemisler:
        # Feromon (geçmiş tecrübe) ^ alpha * Çekicilik (yakınlık) ^ beta
        deger = (feromon[mevcut][j] ** alpha) * (cekicilik[mevcut][j] ** beta)
        olasiliklar[j] = deger
        toplam += deger

    # Olasılıkları normalize et (0-1 arasına çek)
    for j in olasiliklar:
        olasiliklar[j] /= toplam if toplam > 0 else 1

    return olasiliklar

def rulet_tekerlegi_secimi(olasilik_dict):
    """Olasılıklara göre rastgele bir sonraki şehri seçer."""
    r = random.random()
    toplam = 0
    for sehir, olasilik in olasilik_dict.items():
        toplam += olasilik
        if r <= toplam:
            return sehir
    # Matematiksel yuvarlama hatası olursa sonuncuyu döndür
    return list(olasilik_dict.keys())[-1]

def karinca_gezi(baslangic, mesafe, feromon, alpha, beta):
    """Bir karıncanın tüm şehirleri dolaştığı fonksiyon."""
    n = len(mesafe)
    yol = [baslangic]
    toplam_uzunluk = 0
    cekicilik = hesapla_cekicilik(mesafe)

    while len(yol) < n:
        mevcut = yol[-1]
        ziyaret_edilmemisler = list(set(range(n)) - set(yol))
        
        olasiliklar = olasilik_hesapla(mevcut, ziyaret_edilmemisler, feromon, cekicilik, alpha, beta)
        secilen = rulet_tekerlegi_secimi(olasiliklar)
        
        yol.append(secilen)
        toplam_uzunluk += mesafe[mevcut][secilen]

    # Başlangıç noktasına dönüş (Tur tamamlama)
    toplam_uzunluk += mesafe[yol[-1]][yol[0]]
    yol.append(yol[0])
    
    return yol, toplam_uzunluk

def feromon_guncelle(feromon, yollar, buharlasma_orani, Q=1.0):
    """Buharlaşma ve yeni feromon bırakma işlemi."""
    yeni_feromon = (1 - buharlasma_orani) * feromon

    for yol, uzunluk in yollar:
        for i in range(len(yol) - 1):
            a, b = yol[i], yol[i + 1]
            katki = Q / uzunluk if uzunluk > 0 else 0
            yeni_feromon[a][b] += katki
            yeni_feromon[b][a] += katki # Simetrik (gidiş-dönüş aynı yol)

    return yeni_feromon

def run_aco(mesafe, karinca_sayisi, iterasyon_sayisi, alpha, beta, buharlasma_orani, progress_bar=None):
    """Ana Algoritma Döngüsü"""
    feromon = np.ones_like(mesafe) * 0.1
    en_iyi_yol = None
    en_kisa_mesafe = float("inf")
    iterasyon_en_iyiler = []

    for it in range(iterasyon_sayisi):
        yollar = []
        
        # Her karınca tur atar
        for _ in range(karinca_sayisi):
            # Her zaman 0. indisten (Merkez Şube) başla
            yol, uzunluk = karinca_gezi(0, mesafe, feromon, alpha, beta)
            yollar.append((yol, uzunluk))
            
            if uzunluk < en_kisa_mesafe:
                en_kisa_mesafe = uzunluk
                en_iyi_yol = yol
        
        # Feromonları güncelle
        feromon = feromon_guncelle(feromon, yollar, buharlasma_orani)
        iterasyon_en_iyiler.append(en_kisa_mesafe)
        
        # Streamlit ilerleme çubuğunu güncelle (varsa)
        if progress_bar:
            progress_bar.progress((it + 1) / iterasyon_sayisi, text=f"İterasyon {it+1}/{iterasyon_sayisi} - En İyi: {en_kisa_mesafe:.2f} km")

    return en_iyi_yol, en_kisa_mesafe, iterasyon_en_iyiler