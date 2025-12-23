# 🐜 Karınca Kolonisi Algoritması ile En Kısa Yol Optimizasyonu
### Yapay Zeka Sistemleri | Proje Ödevi 2

Bu proje, **Gezgin Satıcı Problemi (TSP)** senaryosu üzerinden, Uşak ilindeki 15 farklı mahalleye en kısa sürede ulaşması gereken bir elektrik arıza ekibinin rotasını optimize etmek için geliştirilmiştir.

Çözüm yöntemi olarak doğadan ilham alan **Karınca Kolonisi Algoritması (Ant Colony Optimization - ACO)** kullanılmıştır. Projede kuş uçuşu mesafeler yerine **Google Maps API** ile alınan gerçek sürüş mesafeleri (Driving Distance) esas alınmıştır.

---

## 📌 Proje Senaryosu (Senaryo 2: Uşak Elektrik Arıza)
**Senaryo:** Elektrik firması, Uşak merkezde 15 farklı mahalleden aynı anda arıza bildirimi almıştır.
**Görev:** Tek bir teknik ekibin Merkez Şube'den çıkıp, tüm arızalı noktalara (mahallere) uğrayıp tekrar merkeze dönmesini sağlayacak **en kısa rotayı** bulmak.

### 🎯 Amaç
* Toplam seyahat mesafesini minimize etmek.
* Gerçek yol verileriyle (Google Maps) uygulanabilir bir rota çıkarmak.
* Streamlit arayüzü ile parametrelerin (karınca sayısı, feromon vb.) etkisini canlı gözlemlemek.

---

## 🧠 Kullanılan Algoritma: Karınca Kolonisi (ACO)

Bu projede, gerçek karıncaların yiyecek ararken en kısa yolu bulma davranışlarını taklit eden **Karınca Kolonisi Optimizasyonu** kullanılmıştır. Algoritmanın temel mekanizması **"Feromon İzi"** mantığına dayanır.

Algoritma adımları ve kullanılan formüller şu şekildedir:

### 1. Olasılıksal Seçim (Karınca Nasıl Karar Verir?)
Bir karınca $i$ şehrinden $j$ şehrine gitme kararını verirken iki faktöre bakar:
1.  **Feromon Miktarı ($\tau$):** Daha önce o yoldan geçen karıncaların bıraktığı iz. (Yolun popülaritesi).
2.  **Görünürlük/Çekicilik ($\eta$):** Yolun kısalığı. Genellikle $1 / Mesafe$ olarak hesaplanır. (Yolun fiziksel avantajı).

**Seçim Formülü:**
Karınca bir sonraki şehri rastgele seçmez, aşağıdaki olasılık formülüne göre **Rulet Tekerleği Seçimi** yapar:

$$P_{ij} = \frac{(\tau_{ij})^\alpha \cdot (\eta_{ij})^\beta}{\sum (\tau_{ik})^\alpha \cdot (\eta_{ik})^\beta}$$

* **Alpha ($\alpha$):** Feromonun (tecrübenin) önem katsayısı.
* **Beta ($\beta$):** Mesafenin (sezgisel bilginin) önem katsayısı.

### 2. Feromon Güncelleme
Tüm karıncalar turu tamamladığında yollar üzerindeki feromon miktarları güncellenir.
* **Buharlaşma:** Feromonlar zamanla uçar. Bu, algoritmanın yerel minimumlara (yanlış çözümlere) takılmasını engeller.
* **Yeni Feromon Bırakma:** Kısa yolu bulan karıncalar, geçtikleri yollara daha fazla feromon bırakır.

**Güncelleme Formülü:**
$$\tau_{ij}(yeni) = (1 - \rho) \cdot \tau_{ij}(eski) + \sum \Delta \tau_{k}$$

* **$\rho$ (Rho):** Buharlaşma oranı (0-1 arası).
* **$\Delta \tau$:** Karıncanın bıraktığı feromon ($Q / ToplamMesafe$). Yol ne kadar kısaysa, bırakılan iz o kadar güçlüdür.

---

## 🛠️ Teknik Altyapı ve Kütüphaneler

Bu projede aşağıdaki teknolojiler entegre edilmiştir:

* **Google Maps Distance Matrix API:** Şehirler arası mesafeler kuş uçuşu (Haversine) değil, trafik kurallarına uygun araç sürüş mesafesi olarak çekilmiştir.
* **Streamlit:** Kullanıcı dostu web arayüzü için kullanılmıştır.
* **Matplotlib:** Rota haritası ve yakınsama grafiklerinin çizimi için kullanılmıştır.
* **Pandas & Numpy:** Veri manipülasyonu ve matris işlemleri için kullanılmıştır.

---

## 📂 Dosya Yapısı

Proje, modüler ve geliştirilebilir bir yapıda tasarlanmıştır:

| Klasör/Dosya | Açıklama |
|---|---|
| `core/aco_algo.py` | **Algoritmanın Beyni.** Olasılık hesabı, rulet seçimi ve feromon güncelleme fonksiyonlarını içerir. |
| `core/distance_matrix.py` | Google Maps API ile bağlantı kuran ve mesafe matrisini oluşturan modül. (API yoksa Haversine devreye girer). |
| `data/coordinates.py` | Uşak ilindeki 15 mahalle ve merkez şubenin koordinat veritabanı. |
| `visual/plotting.py` | Harita üzerinde rotayı çizen ve iterasyon grafiğini oluşturan görselleştirme modülü. |
| `main.py` | Uygulamanın ana giriş noktası. Streamlit arayüz kodlarını içerir. |
| `.streamlit/secrets.toml` | API Anahtarlarının güvenli bir şekilde saklandığı konfigürasyon dosyası. |

---

## 🚀 Kurulum ve Çalıştırma

1.  Bu repoyu bilgisayarınıza indirin.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uygulamayı başlatın:
    ```bash
    streamlit run main.py
    ```
4.  Tarayıcınızda açılan arayüzden **Karınca Sayısı** ve **İterasyon** değerlerini seçip "ROTAYI HESAPLA" butonuna basın.

---

## 👤 Öğrenci Bilgileri

* **Adı Soyadı:** Emre ŞENYURT
* **Okul No:** 2312705012
* **Ders:** BLG 307 - Yapay Zeka Sistemleri
* **Proje:** Proje-2 (Karınca Kolonisi Optimizasyonu)